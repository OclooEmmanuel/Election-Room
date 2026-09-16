#!/usr/bin/env bash
# Render build script: install deps, run migrations, collect static files.
set -o errexit

python -m pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput