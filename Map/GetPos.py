from WebSocket.client import WebSocketClient
import json

class GetPos:
    def __init__(self, uid):
        self.uid = uid
        self.client = WebSocketClient()

    def get_pos(self):
        command = json.dumps({"action": "GetPos", "uid": self.uid})
        self.client.run_forever([command])