"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.utils.timezone import now
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

if now().day == 1:
    print('Running scheduled cleanup images command...')
    call_command('cleanup_images')

application = get_wsgi_application()
