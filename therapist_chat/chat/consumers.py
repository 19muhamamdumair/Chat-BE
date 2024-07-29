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
        event_type = text_data_json['type']

        if event_type == 'request_conversation':
            self.handle_request_conversation(text_data_json)
        else:
            self.handle_chat_message(text_data_json)

    def handle_request_conversation(self, data):
        print("data===============",data)
        sender_id = data['senderId']
        receiver_id = data['receiverId']
        conversation_id = data['conversationId']
        username=data['username']


        # Send a notification to the therapist
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'conversation_request',
                'senderId': sender_id,
                'receiverId': receiver_id,
                'conversationId':conversation_id,
                'username':username
            }
        )

    def handle_chat_message(self, data):
        conversation_id = data['conversation']
        content = data['content']
        file = data['file']
        sender_id = data['sender']
        file_name = data['fileName']
        message_ID = data['message_ID']

        if file:
            file_info = self.base64_to_file(file, file_name)
            msg = self.save_message_to_db(conversation_id, content, file_info, sender_id)
        else:
            msg = self.save_message_to_db(conversation_id, content, file, sender_id)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'conversation': conversation_id,
                'content': content,
                'file': msg.file,
                'sender': sender_id,
                'fileName': file_name,
                'message_ID': msg.id
            }
        )

    def base64_to_file(self, base64_string, file_name):
        format, imgstr = base64_string.split(';base64,')
        ext = format.split('/')[-1]
        if not file_name.lower().endswith(f".{ext}"):
            file_name = f"{file_name}.{ext}"
        decoded_file = base64.b64decode(imgstr)
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
            raise

    def chat_message(self, event):
        conversation = event['conversation']
        content = event['content']
        file = event['file']
        sender = event['sender']
        file_name = event['fileName']
        message_ID = event['message_ID']

        if isinstance(event['file'], FieldFile):
            if event['file']:
                event['file'] = event['file'].url  # Convert to URL
            else:
                event['file'] = None  # Handle None values


        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'conversation': conversation,
            'content': content,
            'file': event['file'],
            'sender': sender,
            'fileName': file_name,
            'message_ID': message_ID
        }))

    def conversation_request(self, event):
        sender_id = event['senderId']
        receiver_id = event['receiverId']
        conversation_id = event['conversationId']
        username=event['username']
        self.send(text_data=json.dumps({
            'type': 'conversation_request',
            'senderId': sender_id,
            'receiverId': receiver_id,
            'conversationId':conversation_id,
            'username':username
        }))
