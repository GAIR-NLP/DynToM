import websocket
import _thread
import time
import json

class WebSocketClient:
    def __init__(self, url = "ws://localhost:8000/ws"):
        self.url = url
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def on_message(self, ws, message):
        print(f"Received '{message}'")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            for command in self.commands:
                ws.send(command)
            ws.close()
        _thread.start_new_thread(run, ())

    def run_forever(self, commands):
        self.commands = commands
        self.ws.run_forever()