import csv
import io
import time

from django.contrib import messages
from django.db import IntegrityError, OperationalError, transaction
from django.db.models import Exists, Max, OuterRef
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import BulkStudentUploadForm, StudentIDForm, VotingForm
from .models import Candidate, Election, Position, Student, Vote

SESSION_STUDENT = "voting_student_id"
SESSION_BALLOT = "voting_ballot"


def get_current_election():
    """The MVP runs a single election; use the most recently created one."""
    return Election.objects.order_by("-id").first()


def _checks(election, student):
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


def _student_from_request(request):
    student_pk = request.session.get(SESSION_STUDENT)
    if not student_pk:
        return None
    return Student.objects.filter(pk=student_pk).first()


def _clear_vote_session(request):
    request.session.pop(SESSION_STUDENT, None)
    request.session.pop(SESSION_BALLOT, None)


def _build_selections(ballot):
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


def _ballot_initial(ballot):
    """Map the stored ballot to per-field initial values for VotingForm."""
    return {
        f"position_{position_id}": str(candidate_id)
        for position_id, candidate_id in (ballot or {}).items()
    }


def home(request):
    return render(request, "voting/home.html", {"election": get_current_election()})


def vote(request):
    student = _student_from_request(request)

    if request.method == "POST":
        if "student_id" in request.POST:
            return _handle_student_id(request)
        return _handle_ballot(request, student)

    election = get_current_election()
    ballot = request.session.get(SESSION_BALLOT)

    if request.GET.get("success"):
        _clear_vote_session(request)
        return render(
            request,
            "voting/vote.html",
            {
                "form": StudentIDForm(),
                "student": None,
                "election": election,
                "show_success": True,
            },
        )

    if request.GET.get("confirm"):
        errors = _checks(election, student)
        selections, ballot_errors = _build_selections(ballot)
        if errors or ballot_errors:
            _clear_vote_session(request)
            messages.error(request, " ".join(errors + ballot_errors))
            return redirect("voting:vote")
        return render(
            request,
            "voting/vote.html",
            {
                "form": VotingForm(initial=_ballot_initial(ballot)),
                "student": student,
                "election": election,
                "show_confirm": True,
                "selections": selections,
            },
        )

    if student is None:
        form = StudentIDForm()
    else:
        form = VotingForm(initial=_ballot_initial(ballot))
    return render(
        request,
        "voting/vote.html",
        {"form": form, "student": student, "election": election},
    )


def _handle_student_id(request):
    form = StudentIDForm(request.POST)
    election = get_current_election()
    error = None

    if form.is_valid():
        student_id = form.cleaned_data["student_id"]
        student = Student.objects.filter(student_id=student_id).first()
        if student is None:
            error = "No student was found with that ID. Please check and try again."
        elif not student.is_active:
            error = "This student account is inactive and cannot vote."
        elif election is None or not election.is_open:
            error = "The election is currently closed."
        elif Vote.objects.filter(student=student).exists():
            error = "You have already voted in this election. Thank you."
        else:
            request.session[SESSION_STUDENT] = student.pk
            return redirect("voting:vote")

    return render(
        request,
        "voting/vote.html",
        {"form": form, "student": None, "election": election, "error": error},
    )


def _handle_ballot(request, student):
    if student is None:
        return redirect("voting:vote")

    election = get_current_election()
    errors = _checks(election, student)
    if errors:
        _clear_vote_session(request)
        messages.error(request, " ".join(errors))
        return redirect("voting:vote")

    form = VotingForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "voting/vote.html",
            {"form": form, "student": student, "election": election},
        )

    ballot = {}
    for name, value in form.cleaned_data.items():
        if name.startswith("position_") and value:
            ballot[int(name.removeprefix("position_"))] = int(value)
    request.session[SESSION_BALLOT] = ballot
    return redirect(f"{reverse('voting:vote')}?confirm=1")


def confirm_vote(request):
    student = _student_from_request(request)
    ballot = request.session.get(SESSION_BALLOT)
    if student is None or not ballot:
        return redirect("voting:vote")

    election = get_current_election()
    errors = _checks(election, student)
    selections, ballot_errors = _build_selections(ballot)

    if request.method == "POST":
        if errors or ballot_errors:
            _clear_vote_session(request)
            messages.error(request, " ".join(errors + ballot_errors))
            return redirect("voting:vote")

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
                break
            except IntegrityError:
                _clear_vote_session(request)
                messages.error(
                    request, "Your vote could not be recorded. You may have already voted."
                )
                return redirect("voting:vote")
            except OperationalError:
                if attempt < max_attempts - 1:
                    time.sleep(0.1 * (attempt + 1))
                    continue
                messages.error(
                    request, "The server is busy. Please try again in a few seconds."
                )
                return redirect("voting:vote")

        _clear_vote_session(request)
        return redirect(f"{reverse('voting:vote')}?success=1")

    if errors or ballot_errors:
        _clear_vote_session(request)
        messages.error(request, " ".join(errors + ballot_errors))
        return redirect("voting:vote")

    return redirect(f"{reverse('voting:vote')}?confirm=1")


def success(request):
    return redirect(f"{reverse('voting:vote')}?success=1")


def results(request):
    election = get_current_election()
    locked = election is None or election.is_open

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

    return render(request, "voting/results.html", {"results": results_data, "locked": locked})


def _bulk_upload_students(csv_file):
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


def dashboard(request):
    election = get_current_election()
    eligible = Student.objects.filter(is_active=True).count()
    total_votes = Vote.objects.count()
    voters = Vote.objects.values("student").distinct().count()
    turnout = round((voters / eligible) * 100, 1) if eligible else 0.0

    import_result = None
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponseForbidden("Only the site admin can upload students.")
        bulk_form = BulkStudentUploadForm(request.POST, request.FILES)
        if bulk_form.is_valid():
            import_result = _bulk_upload_students(bulk_form.cleaned_data["csv_file"])
    else:
        bulk_form = BulkStudentUploadForm()

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

    recent_votes = (
        Vote.objects.select_related("student", "position", "candidate__student")
        .order_by("-created_at")[:8]
    )

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
    voted_count = sum(1 for a in attendance if a["has_voted"])

    return render(
        request,
        "voting/dashboard.html",
        {
            "election": election,
            "eligible": eligible,
            "voters": voters,
            "total_votes": total_votes,
            "turnout": turnout,
            "standings": standings,
            "recent_votes": recent_votes,
            "bulk_form": bulk_form,
            "import_result": import_result,
            "attendance": attendance,
            "voted_count": voted_count,
            "not_voted_count": eligible - voted_count,
        },
    )