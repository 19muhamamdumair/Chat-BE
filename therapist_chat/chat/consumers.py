# consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Conversation
from django.contrib.auth.models import User
import logging
import base64
import io
from django.core.files.base import ContentFile
logger = logging.getLogger(__name__)
import os
from django.db.models.fields.files import FieldFile


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')

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
        file = text_data_json['file']
        sender_id = text_data_json['sender']
        file_name = text_data_json['fileName']  # Ensure correct key here
        message_ID =text_data_json['message_ID']

        if file:
            file_info=self.base64_to_file(file, file_name)
            msg=self.save_message_to_db(conversation_id, content, file_info, sender_id)
        else:
            msg=self.save_message_to_db(conversation_id, content, file, sender_id)



        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'conversation':conversation_id,
                'content':content,
                'file':msg.file,
                'sender': sender_id,
                'fileName':file_name,
                'message_ID':msg.id
            }
        )

    def base64_to_file(self, base64_string, file_name):  
        format, imgstr = base64_string.split(';base64,')
        ext = format.split('/')[-1]
        
        if not file_name.lower().endswith(f".{ext}"):
            file_name = f"{file_name}.{ext}"
        
        decoded_file = base64.b64decode(imgstr)
        
        # Create a file-like object
        file_io = io.BytesIO(decoded_file)
        file = ContentFile(file_io.read(), name=file_name)

        return file

    
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
            return message

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
        message_ID=event['message_ID']

        if isinstance(event['file'], FieldFile):
            if event['file']:
                event['file'] = event['file'].url  # Convert to URL
            else:
                event['file'] = None  # Handle None values


        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'conversation': conversation,
            'content': content,
            'file': event['file'],
            'sender': sender,
            'fileName': file_name,
            'message_ID':message_ID
        }))
    
    