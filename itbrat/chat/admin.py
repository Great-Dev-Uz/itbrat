from django.contrib import admin
from chat.models import Conversation, ChatMessage, Feedback, Question

admin.site.register(Conversation)
admin.site.register(ChatMessage)

class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = [
        'name', 'email', 'create_at'
    ]
    list_display = ['id', 'name', 'email', 'create_at']
    search_fields = ['name', 'email']
    list_filter = ['name', 'email', 'create_at']

admin.site.register(Feedback,  FeedbackAdmin)


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'text'
    ]
    list_display = ['id', 'text', 'create_at']
    search_fields = ['text']
    list_filter = ['text', 'create_at']

admin.site.register(Question,  QuestionAdmin)