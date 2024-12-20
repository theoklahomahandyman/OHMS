#!/bin/sh

set -e

# Collect static files
python manage.py collectstatic --noinput

# Create and apply latest database migrations
python3 manage.py makemigrations
python3 manage.py migrate

uwsgi --socket :8000 --master --enable-threads --module main.wsgi
