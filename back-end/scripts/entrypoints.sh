#!/bin/sh

set -e

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create and apply latest database migrations
echo "Applying database migrations"
python3 manage.py makemigrations
python3 manage.py migrate

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn main.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120
