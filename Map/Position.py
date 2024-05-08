from pymongo import MongoClient
from WebSocket.Client import WebSocketClient 
import json


class Position:
    def __init__(self):
        # self.client = WebSocketClient()
        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client['pos_db']
        self.collection = self.db['pos']
    
    def update_pos(self, message):
        uid, x, y = message.get("uid"), message.get("x"), message.get("y")
        pos = (int(x), int(y))
        self.collection.update_one({'uid': uid}, {'$set': {'pos': pos}}, upsert=True)
        
    async def get_pos(self, uid = None):
        if uid is not None:
            pos_list = self.collection.find_one({'uid': uid})
            if pos_list:
                return pos_list['pos'] 
            else:
                raise Exception(f"User with uid {uid} not found")
        else:
            pos_list = self.collection.find()
            return {item['uid']: item['pos'] for item in pos_list}