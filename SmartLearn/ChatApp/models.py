from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username