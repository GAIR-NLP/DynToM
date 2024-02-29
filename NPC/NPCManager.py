import asyncio
from NPC.NPC import NPC
from NPC.Agent import Agent

class NPCManager:
    def __init__(self):
        self.npcs = {1: Agent(1, {"name": "Ethan", "age": 18, "description": "A year1 student at PolyU."})}
        
    def register_npc(self, uid, info):
        self.npcs[uid] = NPC(uid, info)
        
    def set_handle_chat(self, handle_chat):
        for uid in self.npcs:
            self.npcs[uid].set_handle_chat(handle_chat)

    async def distribute_chat(self, from_uid, to_uid, content):
        if to_uid in self.npcs:
            npc = self.npcs[to_uid]
            asyncio.create_task(npc.receive_chat(from_uid, to_uid, content))
    
    