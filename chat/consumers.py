import json
import logging
from channels.generic.websocket import WebsocketConsumer

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        logger.info("WebSocket connection attempt")
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'message',
            'value': 'connection has been created!'
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"message {message}")

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
