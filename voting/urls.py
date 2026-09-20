from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views

app_name = "voting"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/stats/", views.home_stats, name="home_stats"),
    path("vote/", views.vote, name="vote"),
    path("vote/confirm/", views.confirm_vote, name="vote_confirm"),
    path("vote/success/", views.success, name="vote_success"),
    path("results/", views.results, name="results"),
    path("results/partial/", views.results_partial, name="results_partial"),
    path(
        "dashboard/",
        staff_member_required(views.dashboard),
        name="dashboard",
    ),
    path(
        "dashboard/standings/",
        staff_member_required(views.dashboard_standings),
        name="dashboard_standings",
    ),
    path(
        "dashboard/stats/",
        staff_member_required(views.dashboard_stats),
        name="dashboard_stats",
    ),
    path(
        "dashboard/polls/",
        staff_member_required(views.toggle_polls),
        name="toggle_polls",
    ),
    path(
        "dashboard/exports/voter-template/",
        staff_member_required(views.export_voter_template),
        name="export_voter_template",
    ),
    path(
        "dashboard/exports/votes/",
        staff_member_required(views.export_votes),
        name="export_votes",
    ),
]