"""
class to load model for chat    
"""

from abc import abstractmethod
from lib2to3.pytree import convert
import os
import json
import unicodedata
import transformers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# from vllm import LLM, SamplingParams
from vllm import LLM, SamplingParams
from openai import OpenAI

# from llm_api.config import gpu_id
from time_span.prompt import load_system_prompt
from util.logger import inference_logger, inference2_logger, inference3_logger


# os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
openai_api_key = "sk-fk6iqpaa2gEg02Zx476fD325EcFf4e778527469eEd3f4d4c"
openai_base_url = "https://api3.apifans.com/v1"
# doubao_base_url = "https://ark.cn-beijing.volces.com/api/v3"
# doubao_api_key = "19235e27-489a-45fb-a4fa-a7c4169f0abf"


class ConvertToJSON:
    """convert content to right json format"""

    def __init__(self, content, model_name, logger):
        self.content = content
        self.model_name = model_name
        self.logger = logger

    def gpt(self):
        """remove ```json from content

        Returns:
            _type_: _description_
        """
        if "```json" in self.content:
            self.logger.info("model: %s, content has ```json", self.model_name)
            self.content = self.content[self.content.find("```json") + 7 :]
            self.logger.info("model: %s, content after remove ```json", self.model_name)

        if "```" in self.content:
            self.logger.info("model: %s, content has ```", self.model_name)
            self.content = self.content[: self.content.find("```")]
            self.logger.info("model: %s, content after remove ```", self.model_name)

        return self.convert_to_json()

    def convert_qwen(self):
        """remove useless content"""
        self.content = self.content[self.content.find("{") :]
        self.content = self.content[: self.content.find("}") + 1]
        
        if self.content == "":
            self.logger.error("model: %s, content is empty", self.model_name)
            self.content = "{}"
            # print(self.content
        
        if "{" in self.content:
            self.content = self.content[:self.content.find("{",1)+2]
            if self.content[-1]!="\"":
                self.content=self.content+"\""
            self.content=self.content+"}"

        return self.convert_to_json()

    def convert_llama(self):
        """remove useless content

        Returns:
            _type_: _description_
        """
        self.content = self.content[self.content.find("{") :]
        self.content = self.content[: self.content.find("}") + 1]

        if self.content == "":
            self.logger.error("model: %s, content is empty", self.model_name)
            self.content = "{}"
            # print(self.content

        return self.convert_to_json()

    def convert_deepseek(self):
        """remove useless content

        Returns:
            _type_: _description_
        """
        self.content = self.content[self.content.find("{") :]
        self.content = self.content[: self.content.find("}") + 1]

        if self.content == "":
            self.logger.error("model: %s, content is empty", self.model_name)
            self.content = "{}"
            # print(self.content)

        return self.convert_to_json()

    def convert_mistra(self):
        """remove useless content

        Returns:
            _type_: _description_
        """

        self.content = self.content[self.content.find("{") :]
        self.content = self.content[: self.content.find("}") + 1]

        self.content = self.content.replace("\\", "")

        if self.content == "":
            self.logger.error("model: %s, content is empty", self.model_name)
            self.content = "{}"
            # print(self.content)

        content_dic = self.convert_to_json()
        keys = list(content_dic.keys())
        for key in keys:
            value = content_dic[key]
            # "b. Frustrated and betrayed -> Satisfied and happy -> Concerned and anxious -> Relieved and empathetic",
            if isinstance(value, str):
                content_dic[key] = value[0]

            # {"type_d_whether_1": "d. Yes, from Gary is making progress to Gary can manage on his own"},
            if isinstance(value, dict):
                if len(value) != 1:
                    content_dic.pop(key)
                # self.logger.info("model: %s, value is dict:", self.model_name)
                elif key != list(value.keys())[0]:
                    content_dic.pop(key)
                else:
                    self.logger.info(
                        "model: %s, key: %s, value: %s",
                        self.model_name,
                        key,
                        str(value),
                    )
                    content_dic[key] = value[list(value.keys())[0]][0]

        return content_dic

    def convert_yi(self):
        """remove useless content

        Returns:
            _type_: _description_
        """
        self.content = self.content[self.content.find("{") :]
        self.content = self.content[: self.content.find("}") + 1]

        if self.content == "":
            self.logger.error("model: %s, content is empty", self.model_name)
            self.content = "{}"
            # print(self.content

        return self.convert_to_json()
    
    def convert_glm(self):
        """remove useless content

        Returns:
            _type_: _description_
        """
        self.content = self.content[self.content.find("{") :]
        self.content = self.content[: self.content.find("}") + 1]

        if self.content == "":
            self.logger.error("model: %s, content is empty", self.model_name)
            self.content = "{}"
            # print(self.content

        return self.convert_to_json()
    
    def convert(self, model_name):
        """factory method, convert content to json format according to model name

        Args:
            model_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        if "llama" in model_name.lower():
            return self.convert_llama()

        if "mixtral" in model_name.lower():
            return self.convert_mistra()

        if "mistral" in model_name.lower():
            return self.convert_mistra()

        if "yi" in model_name.lower():
            return self.convert_yi()
        
        if "glm" in model_name.lower():
            return self.convert_glm()
        
        if "qwen" in model_name.lower():
            return self.convert_qwen()
        
        if "deepseek" in model_name.lower():
            return self.convert_deepseek()

    def convert_to_json(self):
        """turn str to dict object

        Args:
            logger (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            content = json.loads(self.content)
            self.logger.info(
                "model: %s, answers number: %s", self.model_name, len(content)
            )
        except json.JSONDecodeError:
            self.logger.error("model: %s, json decode error", self.model_name)
            self.logger.info("the wrong content:\n %s", str(self.content))
            # print(self.content)

        return content


def convert_to_json(content, model_name):
    """convert content to json format"""
    content = content.strip("```json")
    content = content.strip("```")

    if "```json" in content:
        inference_logger.info("model: %s, content has ```json", model_name)
        content = content[content.find("```json") + 7 :]
        inference_logger.info("model: %s, content after remove ```json", model_name)

    if "```" in content:
        inference_logger.info("model: %s, content has ```", model_name)
        content = content[: content.find("```")]
        inference_logger.info("model: %s, content after remove ```", model_name)


    return content


class Chat:
    """base class for chat model"""

    def __init__(self, model_name, model_save_path, gpus=1, logger=inference2_logger):
        self.model_name = model_name
        self.chat_history = []
        self.model_save_path = model_save_path

        self.gpus = gpus
        self.logger = logger

        self.init_model()

    def init_prompt_and_chat(
        self,
        q_id,
        pre_,
        script_number: int,
        information_type="level1",
    ):
        """set system prompt for model"""
        self.sysytem_prompt, questions = load_system_prompt(
            q_id,pre_,
            script_number,
            information_type=information_type,
        )
        self.chat_history = [{"role": "system", "content": self.sysytem_prompt}]
        
        self.require_prompt = """do not provide any other information, only answer the question with a, b, c, ...."""
        

    def init_model(self):
        """
        init model: use model_name to load model
        """
        self.model = LLM(
            model=self.model_save_path,
            tensor_parallel_size=self.gpus,
            trust_remote_code=True,
            gpu_memory_utilization=0.9,
        )
        self.sampling_params = SamplingParams(temperature=0.01, max_tokens=8192)

    def chat(self):
        """chat with model

        Args:
            text (_type_): user input content

        Raises:
            NotImplementedError: _description_
        """
        message = {"role": "user", "content": self.require_prompt}
        self.chat_history.append(message)

        outputs: list = self.model.chat(
            self.chat_history, sampling_params=self.sampling_params, use_tqdm=False
        )
        output = outputs[0].outputs[0].text

        self.logger.info("model: %s, finished", self.model_name)
        # print(outputs[0]["generated_text"])
        # print(outputs[0]["generated_text"][-1])
        convert = ConvertToJSON(output, self.model_name, self.logger)
        #return convert.convert(self.model_name)
        
        return output



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

        message = completion.choices[0].message
        content = unicodedata.normalize("NFKC", message.content)

        inference_logger.info(
            "model: %s, finished reason: %s",
            self.model_name,
            completion.choices[0].finish_reason,
        )

        #return convert_to_json(content, self.model_name)
        return content


class GPT4O(GPT4Turbo):
    """GPT-4-Omega"""

    def __init__(self, model_name="gpt-4o-2024-05-13", model_save_path=None):
        super().__init__(model_name=model_name, model_save_path=model_save_path)
    
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

        #return convert_to_json(content, self.model_name)
        return content


if __name__ == "__main__":
    pass
