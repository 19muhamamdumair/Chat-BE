# chat/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Conversation, Message

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

class ConversationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['status']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.file:
            file_url = instance.file.url
            if file_url.startswith("https//"):
                file_url = file_url.replace("https//", "https://")
            rep['file'] = file_url
        else:
            rep['file'] = None
        print(f"Serialized File URL: {rep['file']}")
        return rep
    
