from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    participants = models.ManyToManyField(User, blank=True, through='Participation', related_name='conversations')


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)

    created_date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)


class Participation(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='participations', on_delete=models.CASCADE)
    participant = models.ForeignKey(User, related_name='conversation_participations', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('conversation', 'participant'),)

