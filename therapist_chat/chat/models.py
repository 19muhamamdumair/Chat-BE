# chat/models.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')
# django.setup()
from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


class UserProfile(models.Model):
    USER_ROLES = (
        ('therapist', 'Therapist'),
        ('parent', 'Parent'),
    )
    class Meta:
        app_label = 'chat'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)

    def __str__(self):
        return self.user.username

class MediaStorage(S3Boto3Storage):
    file_overwrite = True

class Conversation(models.Model):
    STATUS_CHOICES = [
        (1, 'active'),
        (2, 'requested'),
        (3, 'inprogress'),
        (4, 'closed'),
    ]
    therapist = models.ForeignKey(User, related_name='therapist_conversations', on_delete=models.CASCADE)
    parent = models.ForeignKey(User, related_name='parent_conversations', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=4)  # Default to 'requested'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.therapist.username} - {self.parent.username} ({self.get_status_display()})'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=MediaStorage(), upload_to='chat_files/', null=True, blank=True)
