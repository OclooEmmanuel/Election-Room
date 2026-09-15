# JHS Prefect Voting System - AI Agent Project Brief

## 1. Project Overview

Build a small and simple web-based voting system for a Junior High School (JHS) prefect election in Ghana.

The application will use Django and should focus on a clean, understandable MVP. Avoid unnecessary complexity.

The system allows a school administrator to:

- Manage students
- Manage election positions
- Manage candidates
- Open or close the election
- View voting results

Students should be able to:

- Enter their student ID
- View eligible candidates
- Vote once for each available position
- Confirm their choices
- Receive a successful voting confirmation

---

## 2. Main Election Positions

The election has exactly these positions:

1. Head Prefect
2. Head Boy
3. Head Girl
4. Sanitation Prefect
5. Student Chaplain
6. Sports/Entertainment Prefect

Do not add additional positions unless explicitly requested.

---

## 3. Project Goal

Create a minimal, reliable voting system that can be used for a school prefect election.

The primary goal is correctness and simplicity, not a large feature set.

The system should be easy for a junior Django developer to understand, maintain, and extend.

---

## 4. Technology Stack

Use:

- Python
- Django
- SQLite for development
- Django Templates
- HTML5
- CSS
- Bootstrap or simple custom CSS

Do not introduce React, Vue, Django REST Framework, WebSockets, or other unnecessary technologies for the MVP.

Django Admin should be used for administration instead of building a custom admin dashboard.

---

## 5. Django Structure

Use one Django application:

```text
prefect_voting/
├── manage.py
├── prefect_voting/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── voting/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── tests.py
    └── templates/
        └── voting/
            ├── home.html
            ├── vote.html
            ├── confirm_vote.html
            ├── success.html
            └── results.html
```

Keep the project structure simple.

---

## 6. Core Data Models

Use five core models.

### Election

Fields:

- id
- name
- is_open

Purpose:

Controls whether voting is currently available.

Example:

```text
2026 JHS Prefect Election
is_open = True
```

When `is_open` is false, students must not be allowed to vote.

---

### Position

Fields:

- id
- name

Stores the six election positions.

The position names should be exactly:

```text
Head Prefect
Head Boy
Head Girl
Sanitation Prefect
Student Chaplain
Sports/Entertainment Prefect
```

---

### Student

Fields:

- id
- student_id
- full_name
- gender
- class_level
- is_active

Requirements:

- `student_id` must be unique.
- `is_active` determines whether the student is eligible to vote.
- Gender should be simple and should not create unnecessary complexity.

---

### Candidate

Fields:

- id
- student
- position
- manifesto (optional)
- photo (optional)

A candidate must be an existing student.

A candidate belongs to one position.

Do not create a separate person model.

---

### Vote

Fields:

- id
- student
- position
- candidate
- created_at

Important rule:

A student can vote only once for a particular position.

Enforce this at the database level with a unique constraint on:

```text
student + position
```

Do not rely only on frontend validation.

---

## 7. Voting Flow

The student voting process should be simple.

### Step 1: Enter Student ID

Page:

```text
/vote/
```

Display:

```text
Student ID
[____________]

[Continue]
```

The system checks:

- Student exists
- Student is active
- Election is open

If any check fails, show a clear error.

---

### Step 2: Voting Page

Display all six positions.

For each position, display the candidates belonging to that position.

Example:

```text
Head Boy

( ) Candidate A
( ) Candidate B
( ) Candidate C
```

The student selects one candidate for each position.

All six positions should be required.

---

### Step 3: Confirmation

Before saving the votes, display the student's selections.

Example:

```text
Head Prefect: Candidate A
Head Boy: Candidate B
Head Girl: Candidate C
Sanitation Prefect: Candidate A
Student Chaplain: Candidate B
Sports/Entertainment Prefect: Candidate C

[Confirm Vote]
```

The student must confirm before votes are saved.

---

### Step 4: Save Votes

After confirmation:

- Save one Vote record for each position.
- Ensure duplicate voting cannot occur.
- Do not allow partial or invalid votes.
- Show a success page after successful submission.

---

### Step 5: Success Page

Display a simple message:

```text
Vote Submitted Successfully

Thank you for voting.
Your vote has been recorded.
```

Do not display the student's choices after submission unless explicitly requested.

---

## 8. Voting Rules

These rules are mandatory.

### Rule 1

Only active students can vote.

### Rule 2

Voting is allowed only when an election is open.

### Rule 3

A student must select exactly one candidate for each position.

### Rule 4

A candidate must belong to the position being voted for.

### Rule 5

A student cannot vote twice for the same position.

### Rule 6

Use Django CSRF protection.

### Rule 7

Voting validation must happen on the server.

Do not trust JavaScript or HTML validation alone.

---

## 9. Administration

Use Django Admin.

The administrator should be able to manage:

- Elections
- Positions
- Students
- Candidates
- Votes

The administrator should not need a custom dashboard for the MVP.

Register the models in `admin.py` and make the admin interface reasonably usable with:

- `list_display`
- `search_fields`
- `list_filter`
- sensible ordering

---

## 10. Results

Create:

```text
/results/
```

The results page should group results by position.

Example:

```text
HEAD BOY

Candidate A       87 votes
Candidate B       64 votes
Candidate C       31 votes

Winner: Candidate A
```

Do not store vote totals directly on the Candidate model.

Calculate totals from the Vote records.

The results page should show:

- Candidate name
- Position
- Vote count
- Winner

For the MVP, results can be publicly viewable.

If this is later considered inappropriate for the school's use, add authentication or an admin-only results page.

---

## 11. Suggested URLs

Use simple URLs:

```text
/                   Home
/vote/              Start voting
/vote/confirm/      Confirm vote
/vote/success/      Voting success
/results/           Election results
/admin/             Django Admin
```

Adjust the exact URL structure if Django best practices require it.

---

## 12. Security Requirements

Keep security simple but correct.

Must include:

- Django CSRF protection
- Server-side validation
- Database uniqueness constraint for duplicate voting
- Active-student validation
- Election-open validation
- Candidate-position validation

Do not implement advanced authentication for students in the MVP.

Students identify themselves using their unique student ID.

The administrator uses Django's built-in authentication and admin system.

---

## 13. Important Transaction Requirement

When saving a student's six votes, use a database transaction.

The operation should either:

- save all required votes successfully

or:

- save none of them.

Do not allow a situation where five votes are saved and the sixth fails.

Use Django's transaction tools such as:

```python
from django.db import transaction
```

---

## 14. UI Requirements

Keep the UI simple and school-friendly.

Recommended style:

- Clean white background
- School-friendly colors
- Clear headings
- Large buttons
- Mobile-friendly layout
- Simple forms
- Clear validation messages

Do not spend excessive time on animations or complicated UI.

The application should work well on phones because students may use mobile devices.

---

## 15. MVP Exclusions

Do NOT implement these unless explicitly requested:

- Student accounts
- Student passwords
- Email verification
- Password reset
- SMS
- Payments
- Online registration
- Multiple schools
- Multiple elections running simultaneously
- REST API
- React
- Vue
- WebSockets
- Live vote updates
- Blockchain
- Complex analytics
- Advanced reporting
- Automated emails
- Complex role-based permissions
- Custom administrator dashboard

The goal is a small MVP.

---

## 16. Development Plan

Build the application in small stages.

### Sprint 1: Project Setup

Tasks:

- Create Django project
- Create `voting` app
- Configure templates
- Configure static files
- Configure SQLite
- Create Git repository
- Run initial migrations

Deliverable:

A working empty Django project.

---

### Sprint 2: Models

Tasks:

- Create Election model
- Create Position model
- Create Student model
- Create Candidate model
- Create Vote model
- Add relationships
- Add database constraints
- Create migrations
- Apply migrations

Deliverable:

Working database structure.

---

### Sprint 3: Django Admin

Tasks:

- Register all models
- Configure admin list displays
- Add search fields
- Add useful filters
- Create initial positions
- Create test students
- Create test candidates
- Create an election

Deliverable:

Administrator can configure an election from Django Admin.

---

### Sprint 4: Voting

Tasks:

- Create student ID form
- Validate student
- Check election status
- Display candidates
- Process selections
- Create confirmation page
- Save votes
- Use database transaction
- Create success page

Deliverable:

A student can successfully vote.

---

### Sprint 5: Validation and Security

Tasks:

- Test duplicate voting
- Test inactive students
- Test nonexistent students
- Test closed election
- Test invalid candidates
- Test missing selections
- Test CSRF protection
- Test database constraints
- Test transaction behavior

Deliverable:

Reliable voting system.

---

### Sprint 6: Results

Tasks:

- Count votes
- Group results by position
- Determine winners
- Create results page
- Test result calculations

Deliverable:

Working election results.

---

## 17. Testing Requirements

At minimum, write Django tests for:

1. Active student can access voting.
2. Inactive student cannot vote.
3. Unknown student ID is rejected.
4. Closed election prevents voting.
5. Student must select candidates for all positions.
6. Student can submit a valid vote.
7. Student cannot vote twice for the same position.
8. Candidate must belong to the selected position.
9. Results count votes correctly.
10. Winner is calculated correctly.

Tests should focus on business rules rather than superficial implementation details.

---

## 18. Development Rules for the AI Agent

The AI agent must follow these rules.

### Rule A: Keep It Simple

Do not add features that were not requested.

If a simpler Django solution exists, prefer it.

### Rule B: Teach, Don't Hide

The project is intended to help a junior Django developer learn.

When implementing a feature:

1. Explain what needs to be done.
2. Explain why.
3. Break it into small tasks.
4. Let the developer implement where appropriate.
5. Review their implementation.
6. Suggest improvements.

Do not automatically generate the entire project unless explicitly requested.

### Rule C: Prefer Django Built-ins

Use Django's built-in functionality whenever practical.

Examples:

- Django Admin
- Django Forms
- Django ORM
- Django authentication for administrators
- Django validation
- Django transactions
- Django test framework

Avoid unnecessary third-party packages.

### Rule D: Use Function-Based Views

Prefer function-based views for this project unless there is a strong reason to use class-based views.

### Rule E: Avoid Premature Architecture

Do not create:

- service layers
- repositories
- unnecessary utility packages
- complex design patterns
- multiple Django apps

unless the project actually needs them.

### Rule F: Protect Voting Integrity

Voting rules are more important than UI.

Always validate voting actions on the server and enforce important constraints in the database.

---

## 19. Definition of Done

The MVP is complete when:

- The administrator can create an election.
- The administrator can add students.
- The administrator can add candidates.
- Candidates can be assigned to positions.
- The administrator can open and close the election.
- An active student can enter their student ID.
- The student can select one candidate for each of the six positions.
- The student can review their selections.
- The student can submit their vote.
- Six valid Vote records are created.
- The student cannot vote again for the same positions.
- Invalid students cannot vote.
- Voting is blocked when the election is closed.
- Results can be viewed.
- Vote totals are correct.
- Winners are correctly determined.
- Basic Django tests pass.
- The application works on a mobile-sized screen.

---

## 20. Future Features

These are intentionally postponed.

Possible future improvements:

- Student login/PIN
- Admin dashboard
- Election start/end dates
- Multiple elections
- Multiple schools
- CSV student import
- Printable results
- PDF result reports
- Election statistics
- Audit logs
- Better authentication
- DRF API
- HTMX enhancements
- Deployment to production
- PostgreSQL

Do not implement these during the MVP unless requirements change.

---

## 21. Final Architecture

The target architecture should remain approximately:

```text
                 Django
                    |
              voting app
                    |
       +------------+------------+
       |            |            |
    Students    Candidates   Positions
       |            |            |
       +------------+------------+
                    |
                  Votes
                    |
                 Results
```

The application should remain small enough for one developer to understand the entire codebase.

## Final Principle

Build the smallest useful voting system first.

Correct voting behavior is more important than advanced features or visual complexity.
