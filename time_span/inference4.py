import json

from tqdm import tqdm

from time_span.model_chat import *
#from time_span.statistic import calculate_accuracy
from util import logger
from util.logger import inference_logger
# from analysis.analysis_question import influence_mapping, time_stage_analysis
# from synthesize_data.process_data import answer_unmber_mapping


transformation = {
    "belief": {
        "type_d_why_1": "1-2",
        "type_d_why_2": "2-3",
        "type_d_why_3": "3-4",
        
        
        "type_d_whether_1": "1-2",
        "type_d_whether_2": "2-3",
        "type_d_whether_3": "3-4",
        
    },
    "emotion": {
        "type_d_why_7": "1-2",
        "type_d_why_8": "2-3",
        "type_d_why_9": "3-4",
        
        
        "type_d_whether_7": "1-2",
        "type_d_whether_8": "2-3",
        "type_d_whether_9": "3-4",
        
    },
    "intention": {
        "type_d_why_13": "1-2",
        "type_d_why_14": "2-3",
        "type_d_why_15": "3-4",
        
        
        "type_d_whether_13": "1-2",
        "type_d_whether_14": "2-3",
        "type_d_whether_15": "3-4",
        
    },
    "action": {
        "type_d_why_19": "1-2",
        "type_d_why_20": "2-3",
        "type_d_why_21": "3-4",
        
        
        "type_d_whether_19": "1-2",
        "type_d_whether_20": "2-3",
        "type_d_whether_21": "3-4",
        
    },
}

model_name_2_class = {
    "gpt-4-turbo-2024-04-09": GPT4Turbo, # done
    # "gpt-3.5-turbo-0125": GPT3Point5, # done
    "gpt-4o-2024-05-13":GPT4O, # done
    
}

def find_pre_(script_id,q_id):
    return ""
    # if q_id not in influence_mapping:
    #     return ""
    # path = f"synthesize_data/script/data/trial{script_id}/question_new.json"
    # with open(path, "r", encoding="UTF-8") as f:
    #     data = json.load(f)
    
    # pre_=influence_mapping[q_id]
    # pre_1=pre_[0]
    # pre_2=pre_[1]
    
    # pre_1_question=data[pre_1]["question"]
    # answer_id= answer_unmber_mapping[data[pre_1]["true answer"]]
    # answer=data[pre_1]["options"][answer_id][2:]
    # pre_1=pre_1_question+" answer: "+answer
    
    # pre_2_question=data[pre_2]["question"]
    # answer_id= answer_unmber_mapping[data[pre_2]["true answer"]]
    # answer=data[pre_2]["options"][answer_id][2:]
    # pre_2=pre_2_question+" answer: "+answer
    
    # return pre_1+"\n"+pre_2
    
    
    

def store_answer(
    answers,
    script_id: int,
    q_id,
    model_name: str,
    information_type,
):
    """store the answers to the database for the given script_id"""

    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    # print(len(answers))
    if not os.path.exists(path):
        with open(path, "w", encoding="UTF-8") as f:
            json.dump({}, f, indent=4)
    
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
    
    if len(answers) == 0:
        data[q_id] = answers
    else:
        data[q_id] = answers[0].lower()
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
    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)
        if q_id in data:
            return
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
    for script_ids in [range(1150,1160)]:
        
        models = ["gpt-4o-2024-05-13"]
    
        levels = ["level2"]
        
        for script_id in tqdm(script_ids):
            path=f"synthesize_data/script/data/trial{script_id}/question_new.json"
            
            q_ids=[q for mental in transformation for q in transformation[mental]]
            for q_id in q_ids:
                pre_=find_pre_(script_id,q_id)
                main(models, [script_id], levels,q_id,pre_)

    
    
    
    
    