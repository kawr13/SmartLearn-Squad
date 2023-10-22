from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import MessageSerializer
# Create your views here.


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


def chat_messages(request):
    return render(request, 'chat.html')


def chat_view(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    participants = chat.participants.all()
    messages = Message.objects.filter(chat=chat)
    return render(request, 'chat.html', {'participants': participants, 'messages': messages})


