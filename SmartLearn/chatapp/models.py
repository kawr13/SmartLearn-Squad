from ProfileApp.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    content = models.TextField()
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    quontity = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chat')