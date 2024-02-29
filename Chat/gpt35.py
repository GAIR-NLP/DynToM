import traceback
import Chat.openai_async as openai
import os

class GPT35Caller():
    def __init__(self) -> None:
        self.model = "gpt-3.5-turbo"
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    async def ask(self, prompt: str) -> str:
        cnt = 0
        result = "{}"
        while cnt < 3:
            try:
                request_body = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    'temperature' : 0.8
                }
                response = await openai.chat_complete(self.api_key, 50, request_body) 
                result = response.json()["choices"][0]["message"]["content"]
                return result
            except Exception as e:
                print(e)
                cnt += 1

        try:
            traceback.print_exc()
            print(response.json())
        except:
            pass
        __import__('remote_pdb').set_trace()

"""
import openai
import os

openai.api_base = "https://ai-yyds.com/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt, temperature=0.8):
    messages = [{"role": "user", "content": f"{prompt}"}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()
"""