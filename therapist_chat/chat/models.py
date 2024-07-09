# chat/models.py

from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    therapist = models.ForeignKey(User, related_name='therapist_conversations', on_delete=models.CASCADE)
    parent = models.ForeignKey(User, related_name='parent_conversations', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='active')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
