from django.db import models


class Election(models.Model):
    """Controls whether voting is currently available."""

    name = models.CharField(max_length=100)
    is_open = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Position(models.Model):
    """One of the six fixed election positions."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Student(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]

    student_id = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default="")
    class_level = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


class Candidate(models.Model):
    """An eligible student running for one position."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="candidates"
    )
    manifesto = models.TextField(blank=True)
    photo = models.ImageField(upload_to="candidates/", blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["student"], name="unique_candidate_per_student"
            ),
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.position.name}"


class Vote(models.Model):
    """A single vote: one student, one position, one candidate."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "position"], name="unique_vote_per_student_position"
            ),
        ]

    def __str__(self):
        return f"{self.student.student_id} -> {self.position.name}"
