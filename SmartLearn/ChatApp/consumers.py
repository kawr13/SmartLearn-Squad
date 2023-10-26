import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from ChatApp.models import Message


class ChatConsumer(WebsocketConsumer):
    # def fetch_messages(self, data):
    #     messages = Message.objects.all().order_by("-timestamp")[10]
    #     content = {
    #         "command": "messages",
    #         "messages":
    #     }
    #     self.send_message(content)
    #
    # def new_message(self, data):
    #     author = data["author"]
    #     content = data["content"]
    #     Message.objects.create(author=author, content=content)


    # commands = {
    #     "fetch_messages": fetch_messages
    #     "new_message": new_message
    # }
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))