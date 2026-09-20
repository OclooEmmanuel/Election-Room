"""Business logic for the voting module, kept separate from the views."""

import csv
import io
import time

from django.db import IntegrityError, OperationalError, transaction

from .models import Candidate, Election, Position, Student, Vote


def get_current_election():
    """The MVP runs a single election; use the most recently created one."""
    return Election.objects.order_by("-id").first()


def find_voter(student_id, election):
    """Look up a voter by student ID and validate eligibility for an election.

    Returns ``(student, None)`` when the student is eligible to vote, or
    ``(None, error_message)`` otherwise.
    """
    student = Student.objects.filter(student_id=student_id).first()
    if student is None:
        return None, "No student was found with that ID. Please check and try again."
    if not student.is_active:
        return None, "This student account is inactive and cannot vote."
    if election is None or not election.is_open:
        return None, "The election is currently closed."
    if Vote.objects.filter(student=student).exists():
        return None, "You have already voted in this election. Thank you."
    return student, None


def get_vote_errors(election, student):
    """Return a list of errors preventing the given student from voting."""
    errors = []
    if election is None:
        errors.append("There is no election set up yet.")
    elif not election.is_open:
        errors.append("The election is currently closed.")
    if student is None:
        errors.append("Unknown student.")
    elif not student.is_active:
        errors.append("This student account is inactive.")
    elif Vote.objects.filter(student=student).exists():
        errors.append("You have already voted in this election.")
    return errors


def validate_ballot(ballot):
    """Turn the stored ballot dict into position/candidate pairs, validating each."""
    selections = []
    errors = []
    for raw_position_id, raw_candidate_id in (ballot or {}).items():
        position_id = int(raw_position_id)
        candidate_id = int(raw_candidate_id)
        position = Position.objects.filter(pk=position_id).first()
        candidate = Candidate.objects.filter(pk=candidate_id).first()
        if position is None or candidate is None:
            errors.append("A selection on your ballot is no longer valid.")
            continue
        if candidate.position_id != position_id:
            errors.append("A selected candidate no longer matches their position.")
            continue
        selections.append({"position": position, "candidate": candidate})
    if len(selections) != Position.objects.count():
        errors.append("You must choose a candidate for every position.")
    return selections, errors


def record_vote(student, selections):
    """Persist one vote per selection for a student.

    Retries on transient database errors. Returns ``None`` on success or an
    error message string when the vote could not be recorded.
    """
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            with transaction.atomic():
                if Vote.objects.filter(student=student).exists():
                    raise IntegrityError("already voted")
                for item in selections:
                    Vote.objects.create(
                        student=student,
                        position=item["position"],
                        candidate=item["candidate"],
                    )
            return None
        except IntegrityError:
            return "Your vote could not be recorded. You may have already voted."
        except OperationalError:
            if attempt < max_attempts - 1:
                time.sleep(0.1 * (attempt + 1))
                continue
            return "The server is busy. Please try again in a few seconds."
    return "The server is busy. Please try again in a few seconds."


def import_students_from_csv(csv_file):
    """Parse and bulk-create students from an uploaded CSV file."""
    text = csv_file.read().decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))

    if rows and any(
        cell.strip().lower() in ("student_id", "full_name") for cell in rows[0]
    ):
        rows = rows[1:]

    to_create = []
    seen_ids = set()
    duplicates = []
    error_rows = []

    for row in rows:
        if not any(cell.strip() for cell in row):
            continue
        if len(row) < 2:
            error_rows.append((row, "Expected at least 2 columns: student_id, full_name."))
            continue
        student_id = row[0].strip()
        full_name = row[1].strip()
        gender_raw = row[2].strip().upper() if len(row) > 2 else ""
        class_level = row[3].strip() if len(row) > 3 else ""

        if not student_id or not full_name:
            error_rows.append((row, "student_id and full_name are required."))
            continue
        if gender_raw and gender_raw not in ("M", "F"):
            error_rows.append((row, "Gender must be M or F."))
            continue
        if student_id in seen_ids or Student.objects.filter(student_id=student_id).exists():
            duplicates.append((row, "Student ID already exists."))
            continue

        seen_ids.add(student_id)
        to_create.append(
            Student(
                student_id=student_id,
                full_name=full_name,
                gender=gender_raw,
                class_level=class_level,
            )
        )

    if to_create:
        Student.objects.bulk_create(to_create)

    return {
        "created": len(to_create),
        "skipped": len(duplicates),
        "errors": len(error_rows),
        "duplicates": duplicates[:10],
        "error_details": error_rows[:10],
    }


def build_results_data():
    """Build per-position results with sorted candidates, winner and ties."""
    results_data = []
    for position in Position.objects.prefetch_related("candidates").all():
        candidates = [
            {
                "candidate": candidate,
                "count": Vote.objects.filter(candidate=candidate).count(),
            }
            for candidate in position.candidates.all()
        ]
        candidates.sort(key=lambda c: c["count"], reverse=True)

        winner = candidates[0] if candidates else None
        tied = []
        if winner and winner["count"] > 0:
            tied = [
                c
                for c in candidates[1:]
                if c["count"] == winner["count"] and c["candidate"].pk != winner["candidate"].pk
            ]

        results_data.append(
            {
                "position": position,
                "candidates": candidates,
                "winner": winner,
                "tied": tied,
                "total": sum(c["count"] for c in candidates),
            }
        )
    return results_data


def build_standings():
    """Build per-position standings with leader detection for the dashboard."""
    standings = []
    for position in Position.objects.all():
        candidate_counts = {}
        for vote in Vote.objects.filter(position=position).values("candidate"):
            candidate_counts[vote["candidate"]] = candidate_counts.get(vote["candidate"], 0) + 1

        candidates = []
        for candidate in position.candidates.select_related("student"):
            candidates.append(
                {"candidate": candidate, "count": candidate_counts.get(candidate.pk, 0)}
            )
        candidates.sort(key=lambda c: c["count"], reverse=True)

        leader = candidates[0] if candidates and candidates[0]["count"] > 0 else None
        standings.append(
            {
                "position": position,
                "candidates": candidates,
                "leader": leader,
                "total": max(c["count"] for c in candidates) if candidates else 0,
            }
        )
    return standings


def build_attendance():
    """Build the voting-attendance list for active students."""
    attendance = []
    for s in Student.objects.filter(is_active=True).order_by("student_id"):
        has_voted = Vote.objects.filter(student=s).exists()
        voted_at = (
            Vote.objects.filter(student=s)
            .values_list("created_at", flat=True)
            .order_by("-created_at")
            .first()
        )
        attendance.append({"student": s, "has_voted": has_voted, "voted_at": voted_at})
    return attendance