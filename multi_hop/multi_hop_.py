from lzma import PRESET_DEFAULT
import json
from math import e
from analysis .analysis_question import influence_mapping
from analysis.analysis_q_type import find_menta_q_type
from llm_api.inference import model_name_2_class


def load_answer_ground_truth(
    script_id: int, model_name: str, information_type="level1"
):
    """load the answer and ground truth for the given script_id

    Args:
        script_id (int): _description_
        model_name (str): _description_
        information_type (str, optional): _description_. Defaults to "level1".

    Returns:
        _type_: _description_
    """
    # load the answer
    path = f"multi_hop/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    answers = json.load(open(path, encoding="UTF-8"))

    # load the ground truth

    path = f"multi_hop/data/trial{script_id}/question_new.json"
    truth = json.load(open(path, encoding="UTF-8"))

    if "questions" in truth:
        truth = truth["questions"]

    truth_ = {}
    for key, value in truth.items():
        truth_[key] = value["true answer"]

    results = {}
    for q_id, answer in truth_.items():
        if q_id in answers:
            results[q_id] = answer == answers[q_id]
        else:
            results[q_id] = False

    return answers, truth_, results

def calculate_error(model, ids, information_level):
    mental_results={
        "belief": {
            "full_correct":0,
            "local_error":0,
            "full_error":0,
            "restoration error":0,
            "all":0,
        },
        "intention": {
            "full_correct":0,
            "local_error":0,
            "full_error":0,
            "restoration error":0,
            "all":0,
        },
        "action": {
            "full_correct":0,
            "local_error":0,
            "full_error":0,
            "restoration error":0,
            "all":0,
        },
        "emotion": {
            "full_correct":0,
            "local_error":0,
            "full_error":0,
            "restoration error":0,
            "all":0,
        },
        
    }
    q_type_results={
        "transformation": {
            "full_correct":0,
            "local_error":0,
            "full_error":0,
            "restoration error":0,
            "all":0,
        },
        "influence": {
            "full_correct":0,
            "local_error":0,
            "full_error":0,
            "restoration error":0,
            "all":0,
        },
    }
    e_results={
        "full_correct":0,
        "local_error":0,
        "full_error":0,
        "restoration error":0,
        "all":0,
    }
    for id in ids:
        _, _, result = load_answer_ground_truth(id, model, information_level)
        #print(result)

        for q_id, _ in result.items():
            q_type, mental_state = find_menta_q_type(q_id)
            
            
            
            if q_id not in influence_mapping:
                continue
                
            mental_results[mental_state]["all"]+=1
            q_type_results[q_type]["all"]+=1
            e_results["all"]+=1
            
            pre=influence_mapping[q_id]
            pre_1=pre[0]
            pre_2=pre[1]
            
            if result[q_id]==1:
                if result[pre_1]==1 and result[pre_2]==1:
                    mental_results[mental_state]["full_correct"]+=1
                    q_type_results[q_type]["full_correct"]+=1
                    e_results["full_correct"]+=1
                else:
                    mental_results[mental_state]["restoration error"]+=1
                    q_type_results[q_type]["restoration error"]+=1
                    e_results["restoration error"]+=1
            else:
                if result[pre_1]==1 and result[pre_2]==1:
                    mental_results[mental_state]["local_error"]+=1
                    q_type_results[q_type]["local_error"]+=1
                    e_results["local_error"]+=1
                else:
                    mental_results[mental_state]["full_error"]+=1
                    q_type_results[q_type]["full_error"]+=1
                    e_results["full_error"]+=1
    
    # for mental in ["belief", "intention", "action", "emotion"]:
    #     for e_type in ["full_correct", "local_error", "full_error", "restoration error"]:
    #         mental_results[mental][e_type]=mental_results[mental][e_type]/mental_results[mental]["all"]
    
    # for q_type in ["transformation", "influence"]:
    #     for e_type in ["full_correct", "local_error", "full_error", "restoration error"]:
    #         q_type_results[q_type][e_type]=q_type_results[q_type][e_type]/q_type_results[q_type]["all"]
    
    # for e_type in ["full_correct", "local_error", "full_error", "restoration error"]:
    #     e_results[e_type]=e_results[e_type]/e_results["all"]
    
    path = f"multi_hop/data/all_scripts_analysis/{model}_{information_level}_multi_hop.json"
    results={
        "mental":mental_results,
        "q_type":q_type_results,
        "all":e_results,
    }
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f)

if __name__ == "__main__":
    models = ["gpt-4-turbo-2024-04-09","gpt-4o-2024-05-13"]
    ids = [85,182,234,492,594,762,786,895,925,939]
    information_level = "level1"
    for model in models:
        calculate_error(model, ids, information_level)