import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    users = {}  # Keep track of users in each room

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Extract username from the query string
        self.username = self.scope['query_string'].decode().split('=')[-1]
        
        # Ensure room exists in users dictionary
        if self.room_group_name not in self.users:
            self.users[self.room_group_name] = set()

        # Add user to room
        self.users[self.room_group_name].add(self.username)
        logger.info(f"{self.username} connected to {self.room_name}")

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send updated user list to everyone
        await self.update_user_list()

    async def disconnect(self, close_code):
        # Remove user from the list
        if self.username in self.users.get(self.room_group_name, set()):
            self.users[self.room_group_name].remove(self.username)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"{self.username} disconnected from {self.room_name}")

        # Send updated user list
        await self.update_user_list()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Broadcast message to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': username
        }))

    async def update_user_list(self):
        """Send the updated list of users in the room."""
        user_list = list(self.users.get(self.room_group_name, []))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': user_list
            }
        )

    async def user_list(self, event):
        """Send updated user list to the WebSocket client."""
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))
