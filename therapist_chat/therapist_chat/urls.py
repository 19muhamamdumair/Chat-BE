# therapist_chat/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
