"""Compatibility entrypoint for hosts that launch gunicorn with a bare `app`
module (e.g. Render's auto-detected Python start command)."""

from prefect_voting.wsgi import application

app = application