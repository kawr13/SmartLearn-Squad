from django.urls import path
from .views import MessageList, MessageDetail, chat_messages

app_name = 'chatapp'
#
#
#
urlpatterns = [
    path('messages/', MessageList.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message_detail'),
    path('chatapp/messages/', chat_messages, name='chat_messages'),
    path('chatapp/messages/<int:chat_id>/', chat_messages, name='chat_messages'),
]
