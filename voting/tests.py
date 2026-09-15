from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, OperationalError, transaction
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from voting.admin import CandidateForm

from .models import Candidate, Election, Position, Student, Vote

POSITION_NAMES = [
    "Head Prefect",
    "Head Boy",
    "Head Girl",
    "Sanitation Prefect",
    "Student Chaplain",
    "Sports/Entertainment Prefect",
]


class VotingTestCase(TestCase):
    def setUp(self):
        self.election = Election.objects.create(
            name="2026 JHS Prefect Election", is_open=True
        )
        self.positions = {
            name: Position.objects.get_or_create(name=name)[0]
            for name in POSITION_NAMES
        }
        self.voter = self._make_student("JHS-100", "Ama Voter", active=True)
        self.candidates = {}
        for position in self.positions.values():
            student = self._make_student(
                f"CAN-{position.pk}", f"Candidate for {position.name}", active=True
            )
            self.candidates[position.pk] = Candidate.objects.create(
                student=student, position=position
            )

    def _make_student(self, student_id, name, active=True, gender="M"):
        return Student.objects.create(
            student_id=student_id,
            full_name=name,
            gender=gender,
            class_level="Form 3",
            is_active=active,
        )

    def _valid_ballot(self):
        return {
            f"position_{position_pk}": candidate.pk
            for position_pk, candidate in self.candidates.items()
        }

    def _identify(self, student_id):
        return self.client.post(reverse("voting:vote"), {"student_id": student_id})

    def test_active_student_can_access_voting(self):
        response = self.client.get(reverse("voting:vote"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student ID")

        self.client.post(reverse("voting:vote"), {"student_id": self.voter.student_id})
        response = self.client.get(reverse("voting:vote"))
        self.assertEqual(response.status_code, 200)
        for name in POSITION_NAMES:
            self.assertContains(response, name)
        self.assertContains(response, self.voter.full_name)

    def test_inactive_student_cannot_vote(self):
        inactive = self._make_student("JHS-200", "Inactive Student", active=False)
        response = self._identify(inactive.student_id)
        self.assertContains(response, "inactive")

    def test_unknown_student_id_is_rejected(self):
        response = self._identify("GHOST-999")
        self.assertContains(response, "No student was found")

    def test_blank_student_id_is_handled_gracefully(self):
        response = self.client.post(reverse("voting:vote"), {"student_id": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

        response = self.client.post(reverse("voting:vote"), {"student_id": "   "})
        self.assertEqual(response.status_code, 200)

    def test_closed_election_prevents_voting(self):
        self.election.is_open = False
        self.election.save()
        response = self._identify(self.voter.student_id)
        self.assertContains(response, "closed")

    def test_student_must_select_a_candidate_for_every_position(self):
        self._identify(self.voter.student_id)
        ballot = self._valid_ballot()
        first_key = next(iter(ballot))
        del ballot[first_key]

        response = self.client.post(reverse("voting:vote"), ballot)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_student_can_submit_a_valid_vote(self):
        self._identify(self.voter.student_id)
        response = self.client.post(reverse("voting:vote"), self._valid_ballot())
        self.assertRedirects(response, reverse("voting:vote") + "?confirm=1")

        response = self.client.get(reverse("voting:vote") + "?confirm=1")
        self.assertContains(response, "Confirm your choices")
        self.assertContains(response, self.voter.full_name)

        response = self.client.post(reverse("voting:vote_confirm"), {})
        self.assertRedirects(response, reverse("voting:vote") + "?success=1")

        self.assertEqual(Vote.objects.count(), 6)
        self.assertEqual(Vote.objects.filter(student=self.voter).count(), 6)

        response = self.client.get(reverse("voting:vote") + "?success=1")
        self.assertContains(response, "Vote Submitted Successfully")

    def test_student_cannot_vote_twice_for_the_same_position(self):
        Vote.objects.create(
            student=self.voter,
            position=self.candidates[1].position,
            candidate=self.candidates[1],
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(
                    student=self.voter,
                    position=self.candidates[1].position,
                    candidate=self.candidates[1],
                )
        self.assertEqual(Vote.objects.filter(student=self.voter).count(), 1)

        # An already-voted student is refused at identification.
        response = self._identify(self.voter.student_id)
        self.assertContains(response, "already voted")
        self.assertNotIn("voting_student_id", self.client.session)

        # The confirm endpoint also refuses when votes already exist.
        session = self.client.session
        session["voting_student_id"] = self.voter.pk
        session["voting_ballot"] = {
            position_pk: candidate.pk
            for position_pk, candidate in self.candidates.items()
        }
        session.save()
        response = self.client.post(reverse("voting:vote_confirm"), {}, follow=True)
        self.assertContains(response, "already voted")
        self.assertEqual(Vote.objects.filter(student=self.voter).count(), 1)

    def test_student_cannot_stand_for_two_positions(self):
        Candidate.objects.create(
            student=self.voter, position=self.positions["Head Prefect"]
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Candidate.objects.create(
                    student=self.voter,
                    position=self.positions["Head Boy"],
                )

    def test_candidate_must_belong_to_the_selected_position(self):
        self._identify(self.voter.student_id)
        ballot = self._valid_ballot()
        position_id = next(iter(ballot))
        other_key = [k for k in ballot if k != position_id][0]
        ballot[other_key] = ballot[position_id]

        response = self.client.post(reverse("voting:vote"), ballot)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice")

    def test_results_count_votes_correctly(self):
        self.election.is_open = False
        self.election.save()
        Vote.objects.create(
            student=self.voter,
            position=self.candidates[1].position,
            candidate=self.candidates[1],
        )
        response = self.client.get(reverse("voting:results"))
        self.assertContains(response, self.candidates[1].student.full_name)
        self.assertContains(response, "Total votes: 1")

    def test_results_are_locked_while_election_is_open(self):
        response = self.client.get(reverse("voting:results"))
        self.assertContains(response, "Results are not available yet")
        self.assertNotContains(response, "Winner:")
        self.assertEqual(response.context["locked"], True)

    def test_winner_is_calculated_correctly(self):
        self.election.is_open = False
        self.election.save()
        head_prefect = self.positions["Head Prefect"]
        strong = Candidate.objects.create(
            student=self._make_student("CAN-STRONG", "Strong Candidate"),
            position=head_prefect,
        )
        weak = Candidate.objects.create(
            student=self._make_student("CAN-WEAK", "Weak Candidate"),
            position=head_prefect,
        )
        for index in range(3):
            voter = self._make_student(f"VOTER-{index}", f"Voter {index}")
            Vote.objects.create(
                student=voter, position=head_prefect, candidate=strong
            )
            Vote.objects.create(
                student=voter,
                position=self.positions["Head Boy"],
                candidate=self.candidates[self.positions["Head Boy"].pk],
            )
        Vote.objects.create(
            student=self._make_student("VOTER-FINAL", "Final Voter"),
            position=head_prefect,
            candidate=weak,
        )

        response = self.client.get(reverse("voting:results"))
        for group in response.context["results"]:
            if group["position"] == head_prefect:
                self.assertEqual(group["winner"]["candidate"], strong)
                self.assertEqual(group["winner"]["count"], 3)

    def test_transaction_saves_all_or_nothing(self):
        # A student with existing votes cannot start a new ballot at all.
        Vote.objects.create(
            student=self.voter,
            position=self.candidates[1].position,
            candidate=self.candidates[1],
        )
        response = self._identify(self.voter.student_id)
        self.assertContains(response, "already voted")
        self.assertNotIn("voting_student_id", self.client.session)
        self.assertNotIn("voting_ballot", self.client.session)
        self.assertEqual(Vote.objects.filter(student=self.voter).count(), 1)


class ConcurrentVotingTests(TransactionTestCase):
    """Verifies the vote-recording atomicity under a simultaneous write race."""

    def setUp(self):
        self.voter = Student.objects.create(
            student_id="JHS-RACE", full_name="Race Voter", gender="M"
        )
        self.position = Position.objects.get_or_create(name="Head Prefect")[0]
        self.candidate = Candidate.objects.create(
            student=Student.objects.create(
                student_id="RACE-CAN", full_name="Race Candidate", gender="M"
            ),
            position=self.position,
        )

    def test_concurrent_duplicate_votes_persist_exactly_one(self):
        import threading

        barrier = threading.Barrier(2)
        outcomes = []

        def worker():
            barrier.wait()
            try:
                with transaction.atomic():
                    Vote.objects.create(
                        student=self.voter,
                        position=self.position,
                        candidate=self.candidate,
                    )
                outcomes.append("ok")
            except (IntegrityError, OperationalError):
                outcomes.append("dup")

        threads = [threading.Thread(target=worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(outcomes), 2)
        self.assertEqual(
            Vote.objects.filter(student=self.voter, position=self.position).count(), 1
        )


class DashboardBulkUploadTests(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_superuser(
            username="root", email="root@example.com", password="pw"
        )
        self.client.force_login(self.staff_user)

    def _upload(self, content, filename="students.csv"):
        return self.client.post(
            reverse("voting:dashboard"),
            {
                "csv_file": SimpleUploadedFile(
                    filename,
                    content.encode("utf-8"),
                    content_type="text/csv",
                )
            },
        )

    def test_upload_requires_staff(self):
        self.client.logout()
        response = self.client.get(reverse("voting:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_upload_panel_hidden_for_non_superuser_staff(self):
        staff = get_user_model().objects.create_user(
            username="dept-staff", password="pw", is_staff=True
        )
        self.client.force_login(staff)
        response = self.client.get(reverse("voting:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Bulk upload students")

        upload = SimpleUploadedFile(
            "students.csv", b"NEW-020,Blocked Staff,M\n", content_type="text/csv"
        )
        post = self.client.post(reverse("voting:dashboard"), {"csv_file": upload})
        self.assertEqual(post.status_code, 403)
        self.assertEqual(
            Student.objects.filter(student_id="NEW-020").count(), 0
        )

    def test_import_creates_students(self):
        response = self._upload(
            "student_id,full_name,gender,class_level\n"
            "NEW-001,Kofi Mensah,M,Form 1\n"
            "NEW-002,Ama Boateng,F,Form 2\n"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2 added")
        kofi = Student.objects.get(student_id="NEW-001")
        self.assertEqual(kofi.full_name, "Kofi Mensah")
        self.assertEqual(kofi.gender, "M")
        self.assertEqual(kofi.class_level, "Form 1")
        self.assertTrue(Student.objects.filter(student_id="NEW-002").exists())

    def test_import_without_header_row(self):
        response = self._upload("NEW-003,Yaw Dapaah,M,Form 3\n")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.filter(student_id="NEW-003").count(), 1)

    def test_import_accepts_missing_gender(self):
        response = self._upload(
            "NEW-006,Kofi Solo\n"
            "NEW-007,Ama Duo,F,Form 1\n"
        )
        self.assertContains(response, "2 added")
        self.assertEqual(Student.objects.get(student_id="NEW-006").gender, "")
        self.assertEqual(Student.objects.get(student_id="NEW-007").gender, "F")

    def test_import_skips_existing_ids(self):
        Student.objects.create(student_id="NEW-001", full_name="Old", gender="M")
        response = self._upload("NEW-001,Dup,M,Form 1\n")
        self.assertContains(response, "0 added")
        self.assertContains(response, "1 skipped")
        self.assertEqual(Student.objects.filter(student_id="NEW-001").count(), 1)

    def test_import_reports_invalid_rows(self):
        response = self._upload(
            "NEW-004,Bad Gender,X,Form 1\n"
            "NEW-005\n"
        )
        self.assertContains(response, "0 added")
        self.assertContains(response, "2 errors")
        self.assertContains(response, "Gender must be M or F")
        self.assertEqual(Student.objects.filter(student_id="NEW-004").count(), 0)
        self.assertEqual(Student.objects.filter(student_id="NEW-005").count(), 0)

    def test_import_mixes_valid_invalid_and_duplicates(self):
        Student.objects.create(student_id="NEW-010", full_name="Existing", gender="F")
        response = self._upload(
            "NEW-010,Dup,F,Form 1\n"
            "NEW-011,Good Student,M,Form 1\n"
            "NEW-012,Bad Gender,X,Form 2\n"
        )
        self.assertContains(response, "1 added")
        self.assertContains(response, "1 skipped")
        self.assertContains(response, "1 errors")
        self.assertEqual(Student.objects.filter(student_id="NEW-011").count(), 1)

    def test_non_csv_file_is_rejected(self):
        response = self.client.post(
            reverse("voting:dashboard"),
            {
                "csv_file": SimpleUploadedFile(
                    "students.txt", b"NEW-X", content_type="text/plain"
                )
            },
        )
        self.assertEqual(Student.objects.filter(student_id__startswith="NEW").count(), 0)
        self.assertContains(response, "Please upload a .csv file")

    def test_dashboard_lists_voters_and_non_voters(self):
        position = Position.objects.get_or_create(name="Head Prefect")[0]
        candidate = Candidate.objects.create(
            student=Student.objects.create(
                student_id="ROLE-CAN", full_name="Role Candidate", gender="M"
            ),
            position=position,
        )
        voted1 = Student.objects.create(
            student_id="ROLE-A", full_name="Ama Voted", gender="F"
        )
        voted2 = Student.objects.create(
            student_id="ROLE-B", full_name="Kofi Voted", gender="M"
        )
        pending = Student.objects.create(
            student_id="ROLE-C", full_name="Yaw Pending", gender="M"
        )
        Vote.objects.create(student=voted1, position=position, candidate=candidate)
        Vote.objects.create(student=voted2, position=position, candidate=candidate)

        response = self.client.get(reverse("voting:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["eligible"], 4)
        self.assertEqual(response.context["voted_count"], 2)
        self.assertEqual(response.context["not_voted_count"], 2)

        body = response.content.decode()
        for name in ("Ama Voted", "Kofi Voted", "Yaw Pending"):
            self.assertIn(name, body)
        self.assertIn("Voting attendance", body)
        self.assertIn('data-voted="voted"', body)
        self.assertIn('data-voted="pending"', body)

    def test_attendance_requires_staff(self):
        self.client.logout()
        response = self.client.get(reverse("voting:dashboard"))
        self.assertEqual(response.status_code, 302)


class CandidatePhotoTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id="PHOTO-CAN", full_name="Photo Candidate", gender="M"
        )
        self.position = Position.objects.get_or_create(name="Head Prefect")[0]

    def test_candidate_photo_upload(self):
        image = SimpleUploadedFile(
            "candidate.jpg",
            b"fake-image-bytes",
            content_type="image/jpeg",
        )
        candidate = Candidate(
            student=self.student, position=self.position, photo=image
        )
        candidate.save()
        self.assertTrue(candidate.photo.name.startswith("candidates/"))
        self.assertTrue(candidate.photo.url.startswith("/media/candidates/"))
        candidate.photo.delete(False)

    def test_admin_form_requires_photo(self):
        form = CandidateForm(
            data={"student": self.student.pk, "position": self.position.pk},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("photo", form.errors)

    def test_vote_page_shows_candidate_photo(self):
        election = Election.objects.create(name="Election", is_open=True)
        voter = Student.objects.create(
            student_id="PHOTO-VOTER",
            full_name="Photo Voter",
            gender="M",
            is_active=True,
        )
        candidate = Candidate.objects.create(
            student=self.student,
            position=self.position,
            photo=SimpleUploadedFile(
                "candidate.jpg", b"fake-image", content_type="image/jpeg"
            ),
        )
        response = self.client.post(
            reverse("voting:vote"),
            {"student_id": voter.student_id},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('class="card-photo"', body)
        self.assertIn(candidate.photo.url, body)
        self.assertIn('class="candidate-grid"', body)
        self.assertIn('class="candidate-input"', body)
        candidate.photo.delete(False)