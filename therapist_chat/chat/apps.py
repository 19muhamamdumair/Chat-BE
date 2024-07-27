# chat/apps.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
