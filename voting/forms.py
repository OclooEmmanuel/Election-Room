from django import forms

from .models import Candidate, Position


class CandidateCardSelect(forms.RadioSelect):
    """Radio that renders each candidate as a clickable photo card."""

    template_name = "voting/widgets/candidate_card.html"
    option_template_name = "voting/widgets/candidate_card_option.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        candidates_by_pk = getattr(self, "candidates_by_pk", {})
        for group, options, _index in context["widget"]["optgroups"]:
            for option in options:
                try:
                    candidate = candidates_by_pk.get(int(option["value"]))
                except (TypeError, ValueError):
                    candidate = None
                if candidate is None:
                    continue
                option["photo_url"] = (
                    candidate.photo.url if candidate.photo else ""
                )
                option["label"] = candidate.student.full_name
        return context


class StudentIDForm(forms.Form):
    """Step 1: identify the student with their unique student ID."""

    student_id = forms.CharField(
        label="Student ID",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. JHS-001", "autofocus": True}
        ),
    )


class BulkStudentUploadForm(forms.Form):
    """Bulk-create students from a CSV file upload."""

    csv_file = forms.FileField(
        label="Students CSV",
        help_text="Columns: student_id, full_name, gender (M/F, optional), class_level (optional). Header row optional.",
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get("csv_file")
        if csv_file and not csv_file.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a .csv file.")
        return csv_file


class VotingForm(forms.Form):
    """One radio choice per position; built dynamically from the positions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        positions = Position.objects.all()
        for position in positions:
            candidates = (
                Candidate.objects.filter(position=position).select_related("student")
            )
            choices = [
                (candidate.pk, candidate.student.full_name) for candidate in candidates
            ]
            widget = CandidateCardSelect()
            widget.candidates_by_pk = {candidate.pk: candidate for candidate in candidates}
            self.fields[f"position_{position.pk}"] = forms.ChoiceField(
                label=position.name,
                choices=choices,
                widget=widget,
                required=True,
            )

    def clean(self):
        cleaned_data = super().clean()
        for name, value in self.cleaned_data.items():
            if not name.startswith("position_"):
                continue
            position_id = int(name.removeprefix("position_"))
            if not value:
                self.add_error(name, "Please select a candidate for this position.")
                continue
            try:
                candidate = Candidate.objects.get(pk=int(value))
            except (Candidate.DoesNotExist, ValueError, TypeError):
                self.add_error(name, "Invalid candidate selected.")
                continue
            if candidate.position_id != position_id:
                self.add_error(
                    name, "The selected candidate is not standing for this position."
                )
        return cleaned_data