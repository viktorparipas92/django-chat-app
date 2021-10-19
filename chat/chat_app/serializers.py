from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from chat.chat_app import models


class ConversationSerializer(ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())

    class Meta:
        model = models.Conversation
        fields = (
            'participants',
        )


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
