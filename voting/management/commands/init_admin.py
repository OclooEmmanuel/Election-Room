import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create/keep a superuser for production from ADMIN_* env vars. "
        "No-op when ADMIN_USERNAME is not set or the user already exists."
    )

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', '')
        password = os.environ.get('ADMIN_PASSWORD', '')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

        if not username or not password:
            self.stdout.write('ADMIN_USERNAME/ADMIN_PASSWORD not set - skipping superuser creation.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists - nothing to do.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))