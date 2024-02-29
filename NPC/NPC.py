from Chat.gpt35 import GPT35Caller
import asyncio
import json
import importlib

class NPC:
    def __init__(self, uid, info = None):
        self.uid = uid
        if (info == None):
            with open(f"./Information/{uid}.json", "r") as f:
                info = json.load(f)
        self.info = info 
        self.on_moving = False
        self.on_chatting = False
        self.on_working = False
        
    def set_handle_chat(self, handle_chat):
        self.handle_chat = handle_chat
        
    def get_time(self):
        # Return Day and Time
        pass
    
    async def receive_chat(self, from_uid, to_uid, content):
        print(f"Received message from {from_uid} to {to_uid}: {content}")
        if (from_uid == 0 and self.uid == 1):
            response = await GPT35Caller().ask(content)
            print("Response from Agent: ", response)
            asyncio.create_task(self.handle_chat.send_chat_to_unity(to_uid, from_uid, response))
        self.react('receive_chat')
        
    def execute_action(self, action, parameters):
        folder_name, file_name, class_name, method_name = action.split('.')
        module = importlib.import_module(f'{folder_name}.{file_name}')
        class_ = getattr(module, class_name)
        if class_name:
            instance = class_()
            method = getattr(instance, method_name)
        else:
            method = getattr(module, method_name)
        if callable(method):
            method(**parameters)
        else:
            call_method = getattr(method, '__call__')
            call_method(**parameters)
    
    def start(self):
        current_time = self.get_time()
        for schedule in self.info['schedule']:
            if schedule['condition']['start_time'] == current_time:
                self.execute(schedule['action'], schedule['parameters'])

    def react(self, trigger):
        for reaction in self.info['reaction']:
            if reaction['trigger'] == trigger:
                self.execute(reaction['action'], reaction['parameters'])

    