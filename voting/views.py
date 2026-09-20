from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import BulkStudentUploadForm, StudentIDForm, VotingForm
from .models import Student, Vote
from .services import (
    build_attendance,
    build_results_data,
    build_standings,
    find_voter,
    get_current_election,
    get_vote_errors,
    import_students_from_csv,
    record_vote,
    validate_ballot,
)

SESSION_STUDENT = "voting_student_id"
SESSION_BALLOT = "voting_ballot"


def _is_htmx(request):
    """True for explicit htmx swaps; boosted navigation still expects full pages."""
    return request.headers.get("HX-Request") == "true" and request.headers.get("HX-Boosted") != "true"


def _partial(request, template, context, retarget=None):
    """Render an htmx fragment, optionally overriding the swap target."""
    response = render(request, template, context)
    if retarget:
        response["HX-Retarget"] = retarget
    return response


def _student_from_request(request):
    student_pk = request.session.get(SESSION_STUDENT)
    if not student_pk:
        return None
    return Student.objects.filter(pk=student_pk).first()


def _clear_vote_session(request):
    request.session.pop(SESSION_STUDENT, None)
    request.session.pop(SESSION_BALLOT, None)


def _ballot_initial(ballot):
    """Map the stored ballot to per-field initial values for VotingForm."""
    return {
        f"position_{position_id}": str(candidate_id)
        for position_id, candidate_id in (ballot or {}).items()
    }


def home(request):
    return render(request, "voting/home.html", {"election": get_current_election()})


def vote(request):
    htmx = _is_htmx(request)
    student = _student_from_request(request)

    if request.method == "POST":
        if "student_id" in request.POST:
            return _handle_student_id(request, htmx=htmx)
        return _handle_ballot(request, student, htmx=htmx)

    election = get_current_election()
    ballot = request.session.get(SESSION_BALLOT)

    if request.GET.get("success"):
        _clear_vote_session(request)
        if htmx:
            return _partial(request, "partials/_vote_success.html", {}, retarget="#vote-modal-root")
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
        errors = get_vote_errors(election, student)
        selections, ballot_errors = validate_ballot(ballot)
        if errors or ballot_errors:
            if htmx:
                _clear_vote_session(request)
                return _partial(
                    request,
                    "partials/_vote_entry.html",
                    {"form": StudentIDForm(), "error": " ".join(errors + ballot_errors)},
                )
            _clear_vote_session(request)
            messages.error(request, " ".join(errors + ballot_errors))
            return redirect("voting:vote")
        if htmx:
            return _partial(
                request,
                "partials/_vote_confirm.html",
                {"student": student, "selections": selections},
                retarget="#vote-modal-root",
            )
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

    if htmx:
        if student is None:
            return _partial(request, "partials/_vote_entry.html", {"form": form})
        return _partial(request, "partials/_vote_ballot.html", {"form": form, "student": student})

    return render(
        request,
        "voting/vote.html",
        {"form": form, "student": student, "election": election},
    )


def _handle_student_id(request, htmx=False):
    form = StudentIDForm(request.POST)
    election = get_current_election()
    error = None

    if form.is_valid():
        student, error = find_voter(form.cleaned_data["student_id"], election)
        if student is not None:
            request.session[SESSION_STUDENT] = student.pk
            if htmx:
                return _partial(
                    request,
                    "partials/_vote_ballot.html",
                    {"form": VotingForm(), "student": student},
                )
            return redirect("voting:vote")

    if htmx:
        return _partial(
            request,
            "partials/_vote_entry.html",
            {"form": form, "error": error},
        )

    return render(
        request,
        "voting/vote.html",
        {"form": form, "student": None, "election": election, "error": error},
    )


def _handle_ballot(request, student, htmx=False):
    if student is None:
        if htmx:
            return _partial(request, "partials/_vote_entry.html", {"form": StudentIDForm()})
        return redirect("voting:vote")

    election = get_current_election()
    errors = get_vote_errors(election, student)
    if errors:
        if htmx:
            _clear_vote_session(request)
            return _partial(
                request,
                "partials/_vote_entry.html",
                {"form": StudentIDForm(), "error": " ".join(errors)},
            )
        _clear_vote_session(request)
        messages.error(request, " ".join(errors))
        return redirect("voting:vote")

    form = VotingForm(request.POST)
    if not form.is_valid():
        if htmx:
            return _partial(
                request,
                "partials/_vote_ballot.html",
                {"form": form, "student": student},
            )
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

    if htmx:
        selections, _ = validate_ballot(ballot)
        return _partial(
            request,
            "partials/_vote_confirm.html",
            {"student": student, "selections": selections},
            retarget="#vote-modal-root",
        )

    return redirect(f"{reverse('voting:vote')}?confirm=1")


def confirm_vote(request):
    htmx = _is_htmx(request)
    student = _student_from_request(request)
    ballot = request.session.get(SESSION_BALLOT)
    if student is None or not ballot:
        if htmx:
            return _partial(request, "partials/_vote_entry.html", {"form": StudentIDForm()})
        return redirect("voting:vote")

    election = get_current_election()
    errors = get_vote_errors(election, student)
    selections, ballot_errors = validate_ballot(ballot)

    if errors or ballot_errors:
        if htmx:
            _clear_vote_session(request)
            return _partial(
                request,
                "partials/_vote_entry.html",
                {"form": StudentIDForm(), "error": " ".join(errors + ballot_errors)},
                retarget="#step-root",
            )
        _clear_vote_session(request)
        messages.error(request, " ".join(errors + ballot_errors))
        return redirect("voting:vote")

    if request.method == "POST":
        vote_error = record_vote(student, selections)
        if vote_error:
            if htmx:
                _clear_vote_session(request)
                return _partial(
                    request,
                    "partials/_vote_entry.html",
                    {"form": StudentIDForm(), "error": vote_error},
                    retarget="#step-root",
                )
            _clear_vote_session(request)
            messages.error(request, vote_error)
            return redirect("voting:vote")

        _clear_vote_session(request)
        if htmx:
            return _partial(
                request,
                "partials/_vote_success.html",
                {},
                retarget="#vote-modal-root",
            )
        return redirect(f"{reverse('voting:vote')}?success=1")

    if htmx:
        return _partial(
            request,
            "partials/_vote_confirm.html",
            {"student": student, "selections": selections},
            retarget="#vote-modal-root",
        )

    return redirect(f"{reverse('voting:vote')}?confirm=1")


def success(request):
    return redirect(f"{reverse('voting:vote')}?success=1")


def results(request):
    election = get_current_election()
    locked = election is None or election.is_open
    results_data = build_results_data()
    return render(request, "voting/results.html", {"results": results_data, "locked": locked})


def results_partial(request):
    election = get_current_election()
    locked = election is None or election.is_open
    results_data = build_results_data()
    return render(request, "partials/_results_groups.html", {"results": results_data, "locked": locked})


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
            import_result = import_students_from_csv(bulk_form.cleaned_data["csv_file"])
        if _is_htmx(request):
            return render(
                request,
                "partials/_bulk_upload.html",
                {"bulk_form": bulk_form, "import_result": import_result},
            )
    else:
        bulk_form = BulkStudentUploadForm()

    standings = build_standings()
    recent_votes = (
        Vote.objects.select_related("student", "position", "candidate__student")
        .order_by("-created_at")[:8]
    )
    attendance = build_attendance()
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


def dashboard_standings(request):
    standings = build_standings()
    return render(request, "partials/_standings.html", {"standings": standings})


def dashboard_stats(request):
    eligible = Student.objects.filter(is_active=True).count()
    total_votes = Vote.objects.count()
    voters = Vote.objects.values("student").distinct().count()
    turnout = round((voters / eligible) * 100, 1) if eligible else 0.0
    return render(
        request,
        "partials/_stats.html",
        {
            "eligible": eligible,
            "voters": voters,
            "total_votes": total_votes,
            "turnout": turnout,
        },
    )