from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import MessageSerializer
from icecream import ic


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


def chat_messages(request):
    user = request.user
    # Пытаемся получить существующий чат между этими пользователями
    chat, created = Chat.objects.get_or_create(participants=user)

    # Если чата нет, создаем его
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(user)

    # Получаем сообщения в этом чате
    messages = Message.objects.filter(chat=chat)

    context = {
        'messages': messages,
        'user_id': user.id,
        'chat': chat,
    }

    return render(request, 'chat.html', context=context)




async def chat_view(request, chat_id):
    chat = await Chat.objects.get(id=chat_id)
    ic(chat)
    participants = await chat.participants.all()
    messages = await Message.objects.filter(chat=chat)
    return render(request, 'chat.html', {'participants': participants, 'messages': messages})


