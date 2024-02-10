import asyncio
import websockets
import json

async def send_message():
    uri = 'ws://localhost:8000/ws/hola_mundo/'
    async with websockets.connect(uri) as websocket:
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.run(send_message())