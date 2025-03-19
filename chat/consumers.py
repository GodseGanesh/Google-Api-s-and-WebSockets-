import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Message, ChatRoom


logger = logging.getLogger(__name__)



class ChatConsumer(AsyncWebsocketConsumer):
    users = {}  
    user_rooms = {}  

    async def connect(self):
        """Handle new WebSocket connections"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.username = user.username  

        if self.room_group_name not in self.users:
            self.users[self.room_group_name] = set()
        if self.username not in self.user_rooms:
            self.user_rooms[self.username] = set()

        self.users[self.room_group_name].add(self.username)
        self.user_rooms[self.username].add(self.room_name)

        logger.info(f"{self.username} joined {self.room_name}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send past messages when user joins
        await self.send_past_messages()

        # Send updated user list & room list
        await self.update_user_list()
        await self.send_user_rooms()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnections"""
        if self.username in self.users.get(self.room_group_name, set()):
            self.users[self.room_group_name].remove(self.username)

        if self.username in self.user_rooms:
            self.user_rooms[self.username].discard(self.room_name)
            if not self.user_rooms[self.username]:  
                del self.user_rooms[self.username]

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"{self.username} left {self.room_name}")

        await self.update_user_list()
        await self.send_user_rooms()

    async def receive(self, text_data):
        """Handle incoming messages and broadcast them"""
        data = json.loads(text_data)
        message = data["message"]
        timestamp = timezone.now().isoformat()

        await self.save_message(self.scope["user"], self.room_name, message, timestamp)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.username,
                "timestamp": timestamp
            }
        )

    async def chat_message(self, event):
        """Send chat message to WebSocket clients"""
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"]
        }))
    
    async def user_list(self, event):
        """Send updated user list to WebSocket clients"""
        await self.send(text_data=json.dumps({
            "type": "user_list",
            "users": event["users"]
        }))


    async def update_user_list(self):
        """Send updated list of users in the room"""
        user_list = list(self.users.get(self.room_group_name, []))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list",
                "users": user_list
            }
        )

    async def send_user_rooms(self):
        """Send the list of rooms the user has joined"""
        user_rooms = list(self.user_rooms.get(self.username, []))
        await self.send(text_data=json.dumps({
            "type": "user_rooms",
            "rooms": user_rooms
        }))

    @database_sync_to_async
    def save_message(self, user, room_name, message, timestamp):
        """Save a chat message to the database"""
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        Message.objects.create(user=user, room=room, content=message, timestamp=timestamp)

    @database_sync_to_async
    def get_past_messages(self):
        """Fetch past messages from the database"""
        room, created = ChatRoom.objects.get_or_create(name=self.room_name)
        return list(Message.objects.filter(room=room).order_by("timestamp").values("user__username", "content"))

    async def send_past_messages(self):
        """Send past messages when a user joins"""
        past_messages = await self.get_past_messages()
        await self.send(text_data=json.dumps({
            "type": "past_messages",
            "messages": past_messages
        }))
