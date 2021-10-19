from django.contrib.auth.models import User
from django.db import models


def user_can_read(self, user):
    return True


def user_can_update(self, user):
    return self == user


def user_can_delete(self, user):
    return user.is_staff


def user_can_create(self, user):
    return user.is_staff


User.can_read = user_can_read
User.can_update = user_can_update
User.can_delete = user_can_delete
User.can_create = user_can_create


class Conversation(models.Model):
    participants = models.ManyToManyField(User, blank=True, through='Participation', related_name='conversations')

    def can_read(self, user):
        return user in self.participants.all()

    def can_update(self, user):
        return False

    def can_delete(self, user):
        return False

    def can_create(self, user):
        return user in self.participants.all()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)

    created_date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)

    def can_read(self, user):
        return user in self.conversation.participants.all()

    def can_update(self, user):
        return False

    def can_delete(self, user):
        return self.sender == user

    def can_create(self, user):
        return self.sender == user and user in self.conversation.participants.all()


class Participation(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='participations', on_delete=models.CASCADE)
    participant = models.ForeignKey(User, related_name='conversation_participations', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('conversation', 'participant'),)

    def can_read(self, user):
        return self.participant == user

    def can_update(self, user):
        return False

    def can_delete(self, user):
        return False

    def can_create(self, user):
        return self.participant == user

