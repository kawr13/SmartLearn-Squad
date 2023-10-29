from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.author.username


class Chat(models.Model):
    name_chat = models.CharField(max_length=100, verbose_name="Название")
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Dialog'),
        (CHAT, 'Chat')
    )

    type = models.CharField(
        'Тип',
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name="Участник", related_name='chats')



