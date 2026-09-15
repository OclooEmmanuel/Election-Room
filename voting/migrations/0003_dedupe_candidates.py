from django.db import migrations


def dedupe_candidates(apps, schema_editor):
    """Keep one candidate record per student (the earliest), delete the rest.

    A student may now stand for only one position, so any student currently
    linked to multiple Candidate records must be reduced to a single one.
    """
    Candidate = apps.get_model("voting", "Candidate")
    Student = apps.get_model("voting", "Student")

    for student in Student.objects.all():
        candidates = list(Candidate.objects.filter(student=student).order_by("id"))
        for duplicate in candidates[1:]:
            duplicate.delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0002_seed_positions"),
    ]

    operations = [
        migrations.RunPython(dedupe_candidates, noop),
    ]