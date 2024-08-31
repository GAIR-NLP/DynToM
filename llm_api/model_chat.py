"""
class to load model for chat    
"""

from abc import abstractmethod
import os
import json
import unicodedata
import transformers
import torch

from openai import OpenAI

from llm_api.config import gpu_id
from llm_api.prompt import load_system_prompt
from llm_api.config import model_save_folder
from util.logger import inference_logger


os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
openai_api_key = "sk-ADDDrNcyH9zVWKzE375d0cC03fFa4139A2AeCbA2E070Aa1a"
openai_base_url = "https://lonlie.plus7.plus/v1"
# doubao_base_url = "https://ark.cn-beijing.volces.com/api/v3"
# doubao_api_key = "19235e27-489a-45fb-a4fa-a7c4169f0abf"


def convert_to_json(content, model_name):
    """convert content to json format"""
    content = content.strip("```json")
    content = content.strip("```")

    # turn str to dict object
    try:
        content = json.loads(content)
        inference_logger.info("model: %s, answers number: %s", model_name, len(content))
    except json.JSONDecodeError:
        inference_logger.error("model: %s, json decode error")
        inference_logger.info(content)

    return content


class Chat:
    """base class for chat model"""

    def __init__(self, model_name, model_save_path):
        self.model_name = model_name
        self.chat_history = []
        self.model_save_path = model_save_path

        self.require_prompt = """answer the question, and response in JSON format:{[question_id]:[a, b, c or d], [question_id]:a, b, c or d, ...}. for example: {"1":"a","2":"b","3":"c"}"""

        self.init_model()

    def init_prompt_and_chat(
        self,
        script_number: int,
        information_type="level1",
    ):
        """set system prompt for model"""
        self.sysytem_prompt = load_system_prompt(
            script_number,
            information_type=information_type,
        )
        self.chat_history = [{"role": "system", "content": self.sysytem_prompt}]

    @abstractmethod
    def init_model(self):
        """
        init model: use model_name to load model
        """
        raise NotImplementedError

    @abstractmethod
    def chat(self):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError


class Llama38BInstruct(Chat):
    """Llama 3 8B chat model"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Meta-Llama-3-8B-Instruct"
        super().__init__(
            model_name="Meta-Llama-3-8B-Instruct", model_save_path=full_model_path
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


class Llama370BInstruct(Chat):
    """Llama 3 70B chat model"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Meta-Llama-3-70B-Instruct"
        super().__init__(
            model_name="Meta-Llama-3-70B-Instruct", model_save_path=full_model_path
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


class Mistra7BInstructV03(Chat):
    """mistralai/Mistral-7B-Instruct-v0.3"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Mistral-7B-Instruct-v0.3"
        super().__init__(
            model_name="Mistral-7B-Instruct-v0.3", model_save_path=full_model_path
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


class Mistra87BInstructV01(Chat):
    """mistralai/Mixtral-8x7B-Instruct-v0.1"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/Mixtral-8x7B-Instruct-v0.1"
        super().__init__(
            model_name="Mixtral-8x7B-Instruct-v0.1", model_save_path=full_model_path
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


class QWen27BInstruct(Chat):
    """Qwen/Qwen2-7B-Instruct"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/models--Qwen--Qwen2-7B-Instruct/snapshots/41c66b0be1c3081f13defc6bdf946c2ef240d6a6"
        super().__init__(
            model_name="Qwen2-7B-Instruct", model_save_path=full_model_path
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


class QWen272BInstruct(Chat):
    """Qwen/Qwen2-72B-Instruct"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/models--Qwen--Qwen2-72B-Instruct/snapshots/1af63c698f59c4235668ec9c1395468cb7cd7e79"
        super().__init__(
            model_name="Qwen2-72B-Instruct", model_save_path=full_model_path
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


class DeepSeekV2LiteChat(Chat):
    """DeepSeek-V2-Lite-Chat"""

    def __init__(self):
        full_model_path = f"{model_save_folder}/models--deepseek-ai--DeepSeek-V2-Lite-Chat/snapshots/85864749cd611b4353ce1decdb286193298f64c7"
        super().__init__(
            model_name="DeepSeek-V2-Lite-Chat", model_save_path=full_model_path
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


class GPT4Turbo(Chat):
    """GPT-4"""

    def __init__(self, model_name="gpt-4-turbo-2024-04-09", model_save_path=None):
        super().__init__(
            model_name=model_name,
            model_save_path=model_save_path,
        )

    def init_model(self):
        """init model"""
        self.model = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

    def chat(self):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": self.require_prompt}
        self.chat_history.append(message)

        completion = self.model.chat.completions.create(
            messages=self.chat_history,
            model=self.model_name,
            temperature=0.0,
        )

        inference_logger.info(
            "model: %s, finished reason: %s",
            self.model_name,
            completion.choices[0].finish_reason,
        )

        message = completion.choices[0].message
        content = unicodedata.normalize("NFKC", message.content)

        return convert_to_json(content, self.model_name)

    def save_chat(self, text):
        """save chat history into file

        Args:
            text (_type_): user input content
        """
        pass


class GPT4O(GPT4Turbo):
    """GPT-4-Omega"""

    def __init__(self, model_name="gpt-4o-2024-05-13", model_save_path=None):
        super().__init__(model_name=model_name, model_save_path=model_save_path)


class GPT3Point5(Chat):
    """GPT-3.5"""

    def __init__(self):
        full_model_path = None
        super().__init__(
            model_name="gpt-3.5-turbo-0125", model_save_path=full_model_path
        )

    def init_model(self):
        """init model"""
        self.model = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

    def chat(self):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """

        message = {"role": "user", "content": self.require_prompt}
        self.chat_history.append(message)

        completion = self.model.chat.completions.create(
            messages=self.chat_history,
            model=self.model_name,
            temperature=0.0,
        )

        message = completion.choices[0].message
        content = unicodedata.normalize("NFKC", message.content)

        inference_logger.info(
            "model: %s, finished reason: %s",
            self.model_name,
            completion.choices[0].finish_reason,
        )

        return convert_to_json(content, self.model_name)


if __name__ == "__main__":
    pass
