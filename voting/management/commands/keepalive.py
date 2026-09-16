import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Ping the site root to keep Render's free web service warm."

    def handle(self, *args, **options):
        site_url = getattr(settings, "SITE_URL", "").strip().rstrip("/")
        if not site_url:
            self.stdout.write(
                self.style.WARNING("SITE_URL is not set; nothing to ping.")
            )
            return
        url = f"{site_url}/"
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                status = resp.getcode()
        except Exception as exc:
            raise CommandError(f"Keepalive ping to {url} failed: {exc}")
        self.stdout.write(self.style.SUCCESS(f"Pinged {url} -> HTTP {status}"))