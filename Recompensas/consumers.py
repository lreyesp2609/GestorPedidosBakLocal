from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ReclamarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        points = data.get('points', 0)  # Obtiene los puntos del mensaje recibido
        await self.send(text_data="Recibido puntos: " + str(points))  # Envia de vuelta los puntos recibidos
