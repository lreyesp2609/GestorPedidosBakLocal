import json
from channels.generic.websocket import AsyncWebsocketConsumer

class HolaMundoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Hola, mundo'}))