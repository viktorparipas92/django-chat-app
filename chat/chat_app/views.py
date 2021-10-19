from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet, ViewSet

from chat.chat_app import models, serializers


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class ConversationViewSet(ModelViewSet):
    serializer_class = serializers.ConversationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.conversations.all()
        else:
            return models.Conversation.objects.none()


class MessageViewSet(ModelViewSet):
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Message.objects.filter(conversation__participants=self.request.user)
        else:
            return models.Message.objects.none()


class ParticipationViewSet(ModelViewSet):
    serializer_class = serializers.ParticipationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Participation.objects.filter(participant=self.request.user)
        else:
            return models.Participation.objects.none()
