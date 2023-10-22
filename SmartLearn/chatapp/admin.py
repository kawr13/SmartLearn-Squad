from django.contrib import admin

from chatapp.models import Message, Chat


# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)