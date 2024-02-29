import asyncio
import websockets
import json
import os
from dotenv import load_dotenv



class WebSocketClient:
    def __init__(self, url=f"ws://{os.getenv('IP_ADDRESS')}:8000/ws"):
        load_dotenv()
        self.url = url

    async def on_error(self, error):
        print(f"Error: {error}")
        # Error Handling

    async def on_close(self):
        print("### closed ###")
        await self.connection.close()

    async def send_commands(self, commands):
        try:
            self.connection = await websockets.connect(self.url)
            for command in commands:
                await self.connection.send(command)
        except Exception as e:
            await self.on_error(e)
        finally:
            await self.on_close()