from django.core.management.base import BaseCommand

from voting.models import Candidate, Election, Position, Student

# (student_id, full_name, gender, class_level, position) — each student
# stands for exactly ONE position.
DEMO_STUDENTS = [
    ("JHS-001", "Ama Mensah", "F", "Form 3", "Head Girl"),
    ("JHS-002", "Kofi Asante", "M", "Form 3", "Head Prefect"),
    ("JHS-003", "Efua Owusu", "F", "Form 3", "Student Chaplain"),
    ("JHS-004", "Yaw Boateng", "M", "Form 3", "Head Boy"),
    ("JHS-005", "Akosua Addo", "F", "Form 2", "Sanitation Prefect"),
    ("JHS-006", "Kwame Osei", "M", "Form 2", "Head Prefect"),
    ("JHS-007", "Abena Frimpong", "F", "Form 2", "Head Girl"),
    ("JHS-008", "Kojo Antwi", "M", "Form 2", "Sports/Entertainment Prefect"),
    ("JHS-009", "Akua Sarpong", "F", "Form 1", "Student Chaplain"),
    ("JHS-010", "Adjei Nkrumah", "M", "Form 1", "Head Boy"),
    # A few students who are not candidates, just voters
    ("JHS-011", "Mawusi Agbeko", "F", "Form 1", ""),
    ("JHS-012", "Nii Armahtey", "M", "Form 2", ""),
]


class Command(BaseCommand):
    help = "Create a demo election, students, and candidates for the JHS prefect vote."

    def handle(self, *args, **options):
        election, _ = Election.objects.get_or_create(
            defaults={"name": "2026 JHS Prefect Election", "is_open": True},
        )

        by_name = {p.name: p for p in Position.objects.all()}
        created_students = 0
        created_candidates = 0

        for student_id, full_name, gender, class_level, position_name in DEMO_STUDENTS:
            student, was_created = Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    "full_name": full_name,
                    "gender": gender,
                    "class_level": class_level,
                    "is_active": True,
                },
            )
            if was_created:
                created_students += 1

            if not position_name:
                continue

            position = by_name[position_name]
            _, candidate_created = Candidate.objects.update_or_create(
                student=student,
                defaults={"position": position},
            )
            if candidate_created:
                created_candidates += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Election ready: {election.name} "
                f"(is_open={election.is_open}). "
                f"Created {created_students} students, "
                f"{created_candidates} candidates."
            )
        )