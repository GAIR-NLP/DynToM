from fastapi import FastAPI
import socketio
import asyncio
from dotenv import load_dotenv
from Map.Position import Position
from Chat.HandleChat import HandleChat
from NPC.NPCManager import NPCManager
from Tick.Tick import Tick
import json

sio = socketio.AsyncServer(async_mode='asgi')
app = FastAPI()
app = socketio.ASGIApp(sio, app)

users = set()

get_pos = Position()
npc_manager = NPCManager()
handle_chat = HandleChat()
tick = Tick()
npc_manager.set_handle_chat(handle_chat)
handle_chat.set_npc_manager(npc_manager)

@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)
    users.add(sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)
    users.remove(sid)

@sio.event
async def message(sid, data):
    print(f"Received '{data}'")
    await sio.emit('message', data, skip_sid=sid)
    try:
        message = json.loads(data)
        if "action" in message:
            action = message['action']
            if action == "SendPos":
                get_pos.update_pos(message)
            elif action == "SendChat":
                asyncio.create_task(handle_chat.receive_message_from_unity(message))
            elif action == "SendTime":
                tick.update_time(message)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)