from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from chat.chat_app import models, serializers
from chat.framework import CreateModelMixInWithObjectPermissionCheck, ViewMixIn


class UserViewSet(CreateModelMixInWithObjectPermissionCheck, ViewMixIn, ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class ConversationViewSet(CreateModelMixInWithObjectPermissionCheck, ViewMixIn, ReadOnlyModelViewSet):
    serializer_class = serializers.ConversationSerializer

    def get_queryset(self):
        return self.request.user.conversations.all()


class MessageViewSet(
        CreateModelMixInWithObjectPermissionCheck,
        mixins.DestroyModelMixin,
        ViewMixIn,
        ReadOnlyModelViewSet
):
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        return models.Message.objects.filter(conversation__participants=self.request.user)


class ParticipationViewSet(CreateModelMixInWithObjectPermissionCheck, ViewMixIn, ReadOnlyModelViewSet):
    serializer_class = serializers.ParticipationSerializer

    def get_queryset(self):
        return models.Participation.objects.filter(participant=self.request.user)
