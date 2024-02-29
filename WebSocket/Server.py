import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()

connected = set()

# mongod --config Config/Mongo.yaml
# subprocess.run(["mongod", "--config", "Config/Mongo.yaml"], check=True)

async def server(websocket, path):
    # server 函数是一个 WebSocket 服务器，它接收来自客户端的消息，并将消息发送给 main.py listen 客户端，和所有链接的 Unity 客户端
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        connected.remove(websocket)

start_server = websockets.serve(server, os.getenv('IP_ADDRESS'), 8000)

loop = asyncio.get_event_loop()

loop.run_until_complete(start_server)

loop.run_forever()