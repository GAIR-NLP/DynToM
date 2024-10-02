import json

from tqdm import tqdm

from CoT_case_study.model_chat import *
#from time_span.statistic import calculate_accuracy
from util import logger
from util.logger import inference_logger
from analysis.analysis_question import influence_mapping
from synthesize_data.process_data import answer_unmber_mapping
os.environ["CUDA_VISIBLE_DEVICES"]="4,5,6,7"


model_name_2_class = {
    "gpt-4-turbo-2024-04-09": GPT4Turbo, # done
    # "gpt-3.5-turbo-0125": GPT3Point5, # done
    "gpt-4o-2024-05-13":GPT4O, # done
    "Meta-Llama-3.1-70B-Instruct": Llama370BInstruct,
    
}

def find_pre_(script_id,q_id):
    return ""
    

def store_answer(
    answers,
    script_id: int,
    q_id,
    model_name: str,
    information_type,
):
    path = f"synthesize_data/script/data/trial{script_id}/question_new.json"
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    full_answer=data[q_id]
    """store the answers to the database for the given script_id"""
    folder=f"CoT_case_study/data/trial{script_id}/{information_type}_answer_{model_name}/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = f"CoT_case_study/data/trial{script_id}/{information_type}_answer_{model_name}/{q_id}.json"
    # print(len(answers))
    data={
        "answer":answers,
        "full_answer":full_answer
    }
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def run_inference(
    q_id,
    pre_,
    model_name,
    script_id: int,
    information_type,
):
    """run inference to get answers for the questions

    Args:
        model_name (_type_): _description_
    """
    #path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    chat_model: Chat = model_name_2_class[model_name]()
    for script_id in [script_id]:
        chat_model.init_prompt_and_chat(
            q_id,pre_,
            script_id,
            information_type=information_type,
        )
        response = chat_model.chat()
        store_answer(
            response,
            script_id,
            q_id,
            model_name,
            information_type=information_type,
        )


def main(model_names, scripts, levels,q_id,pre_):
    """main function to run the inference

    Args:
        model_names (_type_): models to run inference
        scripts (_type_): the scripts to run inference
        levels (_type_): the information type: level1 or level2
    """
    for script in scripts:
        for model_name in model_names:
            for level in levels:

                inference_logger.info(
                    "-----Running inference for model %s on script %s for information level %s",
                    model_name,
                    script,
                    level,
                )
                run_inference(
                    q_id,pre_,
                    model_name,
                    script,
                    information_type=level,
                )

                # inference_logger.info(
                #     "Calculate accuray for model %s on script %s for information level %s",
                #     model_name,
                #     script,
                #     level,
                # )
                # calculate_accuracy(
                #     script,
                #     model_name=model_name,
                #     information_type=level,
                # )

                inference_logger.info(
                    "-----end inference for model %s on script %s for information level %s",
                    model_name,
                    script,
                    level,
                )


if __name__ == "__main__":    
    for script_ids in [[1210]]:
        
        models = ["gpt-4o-2024-05-13"]
    
        levels = ["level1CoT","level1"]
        
        for script_id in script_ids:
            path=f"synthesize_data/script/data/trial{script_id}/question_new.json"
            with open(path, "r", encoding="UTF-8") as f:
                data = json.load(f)
            q_ids=list(data.keys())
            for q_id in q_ids:
                pre_=find_pre_(script_id,q_id)
                main(models, [script_id], levels,q_id,pre_)

    
    
    
    
    