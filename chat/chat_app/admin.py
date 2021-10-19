from django.contrib import admin

__author__ = 'jens'

from chat.chat_app import models


class MessageAdmin(admin.TabularInline):
    model = models.Message


class ParticipationAdmin(admin.TabularInline):
    model = models.Participation
    can_delete = False


class ConversationAdmin(admin.ModelAdmin):
    inlines = (ParticipationAdmin, MessageAdmin)


admin.site.register(models.Conversation, ConversationAdmin)
