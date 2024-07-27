# therapist_chat/asgi.py

"""
ASGI config for therapist_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')
import django
from channels.routing import get_default_application

django.setup()

application = get_default_application()