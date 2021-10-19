from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from chat.chat_app import models


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = models.Conversation
        exclude = ()


class MessageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        exclude = ()


class ParticipationSerializer(ModelSerializer):
    class Meta:
        model = models.Participation
        exclude = ()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ()
