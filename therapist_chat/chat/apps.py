# chat/apps.py

from django.apps import AppConfig
import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
