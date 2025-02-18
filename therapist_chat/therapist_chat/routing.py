import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing

from django.urls import re_path
from chat.consumers import TextRoomConsumer





websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', TextRoomConsumer.as_asgi()),
]
# the websocket will open at 127.0.0.1:8000/ws/<room_name>
application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})