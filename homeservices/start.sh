#!/usr/bin/env bash

set -e

echo ">>> Running migrations..."
python manage.py migrate --noinput

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput

echo ">>> Seeding database (admin, services, providers)..."
python seed_db.py

echo ">>> Starting server..."
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}