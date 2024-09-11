import json

from tqdm import tqdm

from llm_api.model_chat import *
from analysis.statistic import calculate_accuracy
from util import logger
from util.logger import inference_logger


model_name_2_class = {
    "Meta-Llama-3.1-8B-Instruct": Llama38BInstruct, # done
    "Meta-Llama-3.1-70B-Instruct": Llama370BInstruct,
    "Mistral-7B-Instruct-v0.3": Mistra7BInstructV03, #done
    "Mixtral-8x7B-Instruct-v0.1":Mistra87BInstructV01, #done
    "Qwen2-7B-Instruct": QWen27BInstruct, #done
    "Qwen2-72B-Instruct": QWen272BInstruct, #done
    "DeepSeek-V2-Lite-Chat": DeepSeekV2LiteChat, # done
    "gpt-4-turbo-2024-04-09": GPT4Turbo, # done
    # "gpt-3.5-turbo-0125": GPT3Point5, # done
    "gpt-4o-2024-05-13":GPT4O, # done
    "Yi-1.5-34B-Chat-16K":Yi34B,
    "Yi-1.5-9B-Chat-16K":Yi9B,
    "glm-4-9b-chat":GLM, # done
}


def store_answer(
    answers: dict,
    script_id: int,
    model_name: str,
    information_type="level1",
):
    """store the answers to the database for the given script_id"""

    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    # print(len(answers))
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(answers, f, indent=4)


def run_inference(
    model_name,
    script_id: int,
    information_type="level1",
):
    """run inference to get answers for the questions

    Args:
        model_name (_type_): _description_
    """
    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    if os.path.exists(path):
        inference_logger.info(
            "Answer for model %s on script %s for information level %s already exists",
            model_name,
            script_id,
            information_type,
        )
        return
    chat_model: Chat = model_name_2_class[model_name]()
    for script_id in [script_id]:
        chat_model.init_prompt_and_chat(
            script_id,
            information_type=information_type,
        )
        response = chat_model.chat()
        store_answer(
            response,
            script_id,
            model_name,
            information_type=information_type,
        )


def main(model_names, scripts, levels):
    """main function to run the inference

    Args:
        model_names (_type_): models to run inference
        scripts (_type_): the scripts to run inference
        levels (_type_): the information type: level1 or level2
    """
    for script in tqdm(scripts):
        for model_name in model_names:
            for level in levels:

                inference_logger.info(
                    "-----Running inference for model %s on script %s for information level %s",
                    model_name,
                    script,
                    level,
                )
                run_inference(
                    model_name,
                    script,
                    information_type=level,
                )

                inference_logger.info(
                    "Calculate accuray for model %s on script %s for information level %s",
                    model_name,
                    script,
                    level,
                )
                calculate_accuracy(
                    script,
                    model_name=model_name,
                    information_type=level,
                )

                inference_logger.info(
                    "-----end inference for model %s on script %s for information level %s",
                    model_name,
                    script,
                    level,
                )


if __name__ == "__main__":
    scrip_ids = range(559,560)
    
    models = ["gpt-4-turbo-2024-04-09", "gpt-4o-2024-05-13"]
    #models = [ "gpt-4o-2024-05-13"]
    
    # levels = ["level1", "level2"]
    # levels = ["level2"]
    levels = ["level1"]
    
    main(models, scrip_ids, levels)
