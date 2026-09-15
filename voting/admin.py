from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils.html import format_html

from .models import Candidate, Election, Position, Student, Vote


class CandidateForm(forms.ModelForm):
    """Require a photo on every candidate."""

    class Meta:
        model = Candidate
        fields = "__all__"

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if not photo:
            raise ValidationError("Every candidate must have a photo.")
        return photo


@admin.action(description="Open selected elections")
def open_elections(modeladmin, request, queryset):
    queryset.update(is_open=True)


@admin.action(description="Close selected elections")
def close_elections(modeladmin, request, queryset):
    queryset.update(is_open=False)


@admin.action(description="Activate selected students")
def activate_students(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Deactivate selected students")
def deactivate_students(modeladmin, request, queryset):
    queryset.update(is_active=False)


class CandidateInline(admin.TabularInline):
    model = Candidate
    form = CandidateForm
    fields = ("student", "photo", "manifesto")
    extra = 0
    show_change_link = True
    verbose_name_plural = "Candidates"


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_open", "id")
    list_editable = ("is_open",)
    list_filter = ("is_open",)
    search_fields = ("name",)
    actions = (open_elections, close_elections)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)
    inlines = (CandidateInline,)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "full_name", "gender", "class_level", "is_active")
    list_editable = ("is_active",)
    search_fields = ("student_id", "full_name")
    list_filter = ("gender", "is_active", "class_level")
    ordering = ("student_id",)
    list_per_page = 50
    actions = (activate_students, deactivate_students)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    form = CandidateForm
    list_display = ("student", "position", "student_id", "photo_thumb", "vote_count")
    search_fields = ("student__full_name", "student__student_id", "position__name")
    list_filter = ("position",)
    list_select_related = ("student", "position")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(vote_count=Count("vote"))

    @admin.display(description="Votes", ordering="vote_count")
    def vote_count(self, obj):
        return obj.vote_count

    @admin.display(description="Student ID")
    def student_id(self, obj):
        return obj.student.student_id

    @admin.display(description="Photo")
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img class="photo-thumb" src="{}">', obj.photo.url)
        return "—"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("student", "position", "candidate", "created_at")
    search_fields = ("student__student_id", "student__full_name", "candidate__student__full_name")
    list_filter = ("position", "created_at")
    list_select_related = ("student", "position", "candidate")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 50


admin.site.site_header = "JHS Prefect Voting Admin"
admin.site.site_title = "JHS Prefect Voting"
admin.site.index_title = "Election Management"