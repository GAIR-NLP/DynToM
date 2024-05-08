"""
Player, NPC, Agent
1. Player -> Agent (A)
2. Player -> NPC (A)
3. NPC -> Player (B)
4. NPC -> Agent (C)
5. Agent -> NPC (C)
6. Agent -> Player (B)
7. NPC -> NPC (C)

A. Unity -> Python
B. Python -> Unity 
C. Python -> Python 
          -> Unity
"""

from WebSocket.Client import WebSocketClient 
from Tick.Tick import Tick
import json
import asyncio
from pymongo import MongoClient
import os

class HandleChat:
    """
    1. Receive chat message from Unity
    2. Save all chat happened in sandbox
    3. Send chat message to Unity
    """
    
    def __init__(self):
        self.client = WebSocketClient()
        self.mongo_client = MongoClient(os.getenv("IP_ADDRESS"), 27017)
        self.db = self.mongo_client['chat_db']
        self.collection = self.db['chat_history']
        self.tick = Tick()

    def set_npc_manager(self, npc_manager):
        self.npc_manager = npc_manager

    async def send_chat_to_unity(self, from_uid, to_uid, content): # Python -> Unity
        command = json.dumps({"command": "RegisterChat", "from_uid": from_uid, "to_uid": to_uid, "content": content})
        asyncio.create_task(self.client.send_commands([command]))
        self.save_chat(from_uid, to_uid, content)
        
    async def send_chat_to_npc(self, from_uid, to_uid, content): # Python -> Python
        command = json.dumps({"command": "RegisterChat", "from_uid": from_uid, "to_uid": to_uid, "content": content})
        print("test test")
        asyncio.create_task(self.client.send_commands([command]))
        print("test test test")
        self.save_chat(from_uid, to_uid, content)
        asyncio.create_task(self.distribute_chat(from_uid, to_uid, content))
    

    async def receive_message_from_unity(self, message): # Unity -> Python
        from_uid = message.get("from_uid")
        to_uid = message.get("to_uid")
        content = message.get("content")
        # print("receive_message_from_unity 1")
        self.save_chat(from_uid, to_uid, content)
        # print("receive_message_from_unity 2")
        asyncio.create_task(self.distribute_chat(from_uid, to_uid, content))
        
    def save_chat(self, from_uid, to_uid, content): 
        """
        Generate a hash uid for each chat session (accroding to time, from_uid, to_uid)
        If uid exists, update the chat session
        If uid not exists, save the chat session
        """
        chat = {
            "from_uid": from_uid,
            "to_uid": to_uid,
            "content": content,
            "time": self.tick.get_time()
        }
        self.collection.insert_one(chat)
    
    def get_chats(self, from_uid=None, to_uid=None,start_time=None, end_time=None):
        query = {}
        if from_uid is not None:
            query['from_uid'] = from_uid
        if to_uid is not None:
            query['to_uid'] = to_uid
        if start_time is not None or end_time is not None:
            query['time'] = {}
            if start_time is not None:
                query['time']['$gte'] = start_time
            if end_time is not None:
                query['time']['$lte'] = end_time
        return list(self.collection.find(query))
       
    async def distribute_chat(self, from_uid, to_uid, content):
        # print("HandleChat: Distribute chat\n\n\n\n\n")
        await self.npc_manager.distribute_chat(from_uid, to_uid, content)