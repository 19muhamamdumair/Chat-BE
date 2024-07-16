from channels.routing import ProtocolTypeRouter, URLRouter
# import app.routing
# import os
from django.core.asgi import get_asgi_application
from django.urls import re_path
from chat.consumers import TextRoomConsumer
from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')


websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', TextRoomConsumer.as_asgi()),
]
# the websocket will open at 127.0.0.1:8000/ws/<room_name>
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})

wsgi_application = get_wsgi_application()
