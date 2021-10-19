from django.urls import path, include
from rest_framework import routers

from chat.chat_app import views

router = routers.SimpleRouter()
router.register(r'conversation', views.ConversationViewSet, 'conversation')
router.register(r'message', views.MessageViewSet, 'message')
router.register(r'participation', views.ParticipationViewSet, 'participation')

urlpatterns = router.urls
