# consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Conversation, UserProfile
from django.contrib.auth.models import User
import logging

from django.db import transaction
logger = logging.getLogger(__name__)
class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        conversation_id = text_data_json['conversation']
        content = text_data_json['content']
        file = text_data_json.get('file')
        sender_id = text_data_json['sender']
        file_name = text_data_json.get('fileName')  # Ensure correct key here

        # Save message to database
        self.save_message_to_db(conversation_id, content, file, sender_id)

        # Send message back to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'conversation':conversation_id,
                'content':content,
                'file':file,
                'sender': sender_id,
                'fileName':file_name
            }
        )

    def save_message_to_db(self, conversation_id, content, file, sender_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            sender = User.objects.get(id=sender_id)

            message = Message(
                conversation=conversation,
                content=content,
                file=file,
                sender=sender
            )
            message.save()
            print(message)

        except (Conversation.DoesNotExist, User.DoesNotExist) as e:
            print(f"Error saving message to database: {e}")
            raise  # Optionally handle or log the error

    def chat_message(self, event):
        # Receive message from room group
        conversation = event['conversation']
        content = event['content']
        file = event['file']
        sender = event['sender']
        file_name = event['fileName']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'conversation': conversation,
            'content': content,
            'file': file,
            'sender': sender,
            'fileName': file_name
        }))
    
    