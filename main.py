import json
import websockets
import asyncio
import os
from dotenv import load_dotenv
from Map.Position import Position
from Chat.HandleChat import HandleChat
from NPC.NPCManager import NPCManager
from Tick.Tick import Tick

load_dotenv()

async def listen():
    connection = await websockets.connect(f"ws://{os.getenv('IP_ADDRESS')}:8000/ws")
    while True:
        message = await connection.recv()
        message = json.loads(message)
        if "action" in message:
            print(f"Received '{message}'")
            if message.get("action") == "SendPos":
                get_pos.update_pos(message)
            elif message.get("action") == "SendChat":
                await handle_chat.receive_message_from_unity(message)
            elif message.get("action") == "SendTime":
                tick.update_time(message)

get_pos = Position()
npc_manager = NPCManager()
handle_chat = HandleChat()
tick = Tick()
npc_manager.set_handle_chat(handle_chat)
handle_chat.set_npc_manager(npc_manager)

asyncio.run(listen())