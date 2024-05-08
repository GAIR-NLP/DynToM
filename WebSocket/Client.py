import asyncio
from socketio import AsyncClient
import os
from dotenv import load_dotenv

load_dotenv()

class WebSocketClient:
    def __init__(self, url=f"http://{os.getenv('IP_ADDRESS')}:8000"):
        self.sio = AsyncClient()
        self.url = url
        
    async def start(self):
        await self.sio.connect(self.url)
        print("Connected to the server")

    async def on_error(self, error):
        print(f"Error: {error}")

    async def on_close(self):
        print("### closed ###")
        await self.sio.disconnect()

    async def send_commands(self, commands):
        print("Connecting...")
        await self.start()
        try:
            for command in commands:
                await self.sio.emit('message', command)
        except Exception as e:
            await self.on_error(e)
        # finally:
        #     await self.on_close()
            

            
            
