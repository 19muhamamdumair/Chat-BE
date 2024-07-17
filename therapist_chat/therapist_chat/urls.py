# therapist_chat/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from chat import views
from django.conf import settings
from django.conf.urls.static import static
from chat.consumers import TextRoomConsumer

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path(r'^api/sign_in/?$', views.sign_in, name='sign_in'),
    path('api/change_conversation_status/', views.change_conversation_status, name='change_conversation_status'),
    path('api/get_all_therapists/', views.get_all_therapists, name='get_all_therapists'),
    path('api/get_all_parents/', views.get_all_parents, name='get_all_parents'),
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', TextRoomConsumer.as_asgi()),
    path('api/message/', views.get_message_by_id, name='get_message_by_id'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
