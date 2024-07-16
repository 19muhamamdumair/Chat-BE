from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application
from django.urls import re_path
from chat.consumers import TextRoomConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapist_chat.settings')

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', TextRoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # ASGI application
    "websocket": URLRouter(websocket_urlpatterns),
})

wsgi_application = get_wsgi_application()  # WSGI application