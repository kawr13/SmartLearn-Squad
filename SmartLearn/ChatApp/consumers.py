import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from ChatApp.models import Message, Chat
from django.contrib.auth import get_user_model
from icecream import ic

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, chat_id):

        messages = Message.objects.filter(chat=chat_id).order_by('timestamp')
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def new_message(self, data):
        chat = Chat.objects.get(id=data['chat_id'])
        author = data['from']
        author_user = User.objects.get(username=author)
        message = Message.objects.create(chat=chat, author=author_user, content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }

    def connect(self):
        """
        Вызывается при установлении WebSocket-соединения.
        """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # Добавляет соединение к группе
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        self.fetch_messages(self.chat_id)

    def disconnect(self, close_code):
        """
        Вызывается при разрыве WebSocket-соединения.
        """
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        """
        Метод receive вызывается при получении сообщения через WebSocket.
        Он извлекает текстовое сообщение из text_data и отправляет его в группу каналов для распространения среди всех участников комнаты.
        """
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def send_message(self, message):
        async_to_sync(self.send(text_data=json.dumps(message)))
    # Receive message from room group

    def chat_message(self, event):
        message = event["message"]
        async_to_sync(self.send(text_data=json.dumps(message)))
