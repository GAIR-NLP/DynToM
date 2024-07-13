"""
class to load model for chat    
"""

from abc import abstractmethod
import os
import transformers
import torch
from openai import OpenAI
from llm_api.config import gpu_id
from llm_api.prompt import load_system_prompt
from llm_api.config import model_save_folder
import unicodedata

os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
openai_api_key ="sk-25KhYqJYbiU8HwHa1fF497E65b8c4506B671E2D24bCe4aC9"
openai_base_url = "https://lonlie.plus7.plus/v1"


class Chat:
    """base class for chat model"""

    def __init__(self, model_name, chat_save_path, model_save_path):
        self.model_name = model_name
        self.chat_save_path = chat_save_path
        self.chat_history = []
        self.model_save_path = model_save_path

        self.init_prompt_and_chat()
        self.init_model()

    def init_prompt_and_chat(self):
        """set system prompt for model"""
        self.sysytem_prompt = load_system_prompt()
        self.chat_history = [{"role": "system", "content": self.sysytem_prompt}]

    def clear_chat(self):
        """clear chat history"""
        self.init_prompt_and_chat()

    def print_chat(self):
        """print chat history"""
        for chat in self.chat_history:
            print(chat)

    @abstractmethod
    def init_model(self):
        """
        init model: use model_name to load model
        """
        raise NotImplementedError

    @abstractmethod
    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    @abstractmethod
    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        raise NotImplementedError


class Llama38BInstruct(Chat):
    """Llama 3 8B chat model"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Meta-Llama-3-8B-Instruct"
        super().__init__(
            model_name="Meta-Llama-3-8B-Instruct",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = transformers.pipeline(
            "text-generation",
            model=self.model_save_path,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        message = {"role": "user", "content": text}
        self.chat_history.append(message)
        terminators = [
            self.model.tokenizer.eos_token_id,
            self.model.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        outputs = self.model(
            self.chat_history,
            max_new_tokens=8192,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.01,
            top_p=0.9,
        )
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class Llama370BInstruct(Chat):
    """Llama 3 70B chat model"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Meta-Llama-3-70B-Instruct"
        super().__init__(
            model_name="Meta-Llama-3-70B-Instruct",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = transformers.pipeline(
            "text-generation",
            model=self.model_save_path,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        message = {"role": "user", "content": text}
        self.chat_history.append(message)
        terminators = [
            self.model.tokenizer.eos_token_id,
            self.model.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        outputs = self.model(
            self.chat_history,
            max_new_tokens=8192,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.01,
            top_p=0.9,
        )
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class Mistra7BInstructV03(Chat):
    """mistralai/Mistral-7B-Instruct-v0.3"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Mistral-7B-Instruct-v0.3"
        super().__init__(
            model_name="Mistral-7B-Instruct-v0.3",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = transformers.pipeline(
            "text-generation", model=self.model_save_path
        )

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        message = {"role": "user", "content": self.sysytem_prompt + "\n" + text}
        self.chat_history = [message]

        outputs = self.model(
            self.chat_history,
            temperature=0.0,
            max_new_tokens=8192,
        )
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class Mistra87BInstructV01(Chat):
    """mistralai/Mixtral-8x7B-Instruct-v0.1"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Mixtral-8x7B-Instruct-v0.1"
        super().__init__(
            model_name="Mixtral-8x7B-Instruct-v0.1",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = transformers.pipeline(
            "text-generation", model=self.model_save_path
        )

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        message = {"role": "user", "content": self.sysytem_prompt + "\n" + text}
        self.chat_history = [message]

        outputs = self.model(
            self.chat_history,
            temperature=0.0,
            max_new_tokens=8192,
        )
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class QWen27BInstruct(Chat):
    """Qwen/Qwen2-7B-Instruct"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/models--Qwen--Qwen2-7B-Instruct/snapshots/41c66b0be1c3081f13defc6bdf946c2ef240d6a6"
        super().__init__(
            model_name="Qwen2-7B-Instruct",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = transformers.pipeline(
            "text-generation",
            model=self.model_save_path,
            torch_dtype="auto",
            device_map="auto",
        )

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": text}
        self.chat_history.append(message)

        outputs = self.model(self.chat_history, max_new_tokens=8192, temperature=0.01)
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class QWen272BInstruct(Chat):
    """Qwen/Qwen2-72B-Instruct"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/models--Qwen--Qwen2-72B-Instruct/snapshots/1af63c698f59c4235668ec9c1395468cb7cd7e79"
        super().__init__(
            model_name="Qwen2-72B-Instruct",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = transformers.pipeline(
            "text-generation",
            model=self.model_save_path,
            torch_dtype="auto",
            device_map="auto",
        )

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": text}
        self.chat_history.append(message)

        outputs = self.model(self.chat_history, max_new_tokens=8192, temperature=0.01)
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class DeepSeekV2LiteChat(Chat):
    """DeepSeek-V2-Lite-Chat"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/models--deepseek-ai--DeepSeek-V2-Lite-Chat/snapshots/85864749cd611b4353ce1decdb286193298f64c7"
        super().__init__(
            model_name="DeepSeek-V2-Lite-Chat",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        pass

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": text}
        self.chat_history.append(message)

        pass
        return outputs

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class GPT4(Chat):
    """GPT-4"""

    def __init__(self):
        full_model_path = None
        super().__init__(
            model_name="gpt-4-turbo-2024-04-09",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": text}
        self.chat_history.append(message)

        completion = self.model.chat.completions.create(
            messages=self.chat_history,
            model=self.model_name,
        )

        message = completion.choices[0].message
        content = unicodedata.normalize("NFKC", message.content)

        return content

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class GPT3Point5(Chat):
    """GPT-3.5"""

    def __init__(self):
        full_model_path = None
        super().__init__(
            model_name="gpt-3.5-turbo-0125",
            model_save_path=full_model_path,
            chat_save_path=None,
        )

    def init_model(self):
        """init model"""
        self.model = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

    def chat(self, text):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": text}
        self.chat_history.append(message)

        completion = self.model.chat.completions.create(
            messages=self.chat_history,
            model=self.model_name,
        )

        message = completion.choices[0].message
        content = unicodedata.normalize("NFKC", message.content)

        return content

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass

if __name__=="__main__":
    model=GPT4()
    print(model.chat("what is the meaning of life?"))