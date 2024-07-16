import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

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
        # print(text_data)
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        conversation=text_data_json['conversation']
        content=text_data_json['content']
        file=text_data_json['file']
        sender = text_data_json['sender']
        fileName =text_data_json['fileName']

        print("receive")
        # print(conversation,content,file,sender)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'conversation':conversation,
                'content':content,
                'file':file,
                'sender': sender,
                'fileName':fileName
            }
        )

    def chat_message(self, event):
        print("chat_message")
        # print(event)

        # Receive message from room group
        conversation=event['conversation']
        content=event['content']
        file=event['file']
        sender = event['sender']
        fileName =event['fileName']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'conversation':conversation,
                'content':content,
                'file':file,
                'sender': sender,
                'fileName':fileName
        }))