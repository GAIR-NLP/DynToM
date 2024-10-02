import json
import csv
import matplotlib.pyplot as plt
import numpy as np
from sympy import rotations
from util.random_id_cot import cot_list


def print_table_llm_mental_q_type_accuracy(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_all.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    path=f"paper_table/data/llm_{level}_mental_q_type_accuracy.csv"
    with open(path,'w',encoding="UTF-8") as f:
        writer=csv.writer(f)
        writer.writerow(["None","belief-u","belief-i","belief-t","emotion-u","emotion-i","emotion-t","intention-u","intention-i","intention-t","action-u","action-t","avg."])
        
        for model in models:
            writer.writerow([model]+[results[model][mental_state][q_type]["accuracy"] for mental_state in ["belief", "emotion", "intention", "action"] for q_type in ["understanding", "influence","transformation"] if not (mental_state=="action" and q_type=="influence")]+[results[model]["all"]["accuracy"]])
            
def print_table_llm_mental_q_type_split(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_all_mental_q_type.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    path=f"paper_table/data/llm_{level}_mental_q_type_split.csv"
    with open(path,'w',encoding="UTF-8") as f:
        writer=csv.writer(f)
        writer.writerow(["None","belief","emotion","intention","action","understanding", "influence","transformation"])
        
        for model in models:
            writer.writerow([model]+[results[model]["mental_state"][mental_state]["accuracy"] for mental_state in ["belief", "emotion", "intention", "action"]]+[results[model]["q_type"][q_type]["accuracy"] for q_type in ["understanding", "influence","transformation"]])

def print_table_time_stage(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_time_stage_transformation.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    alol_re={
        "belief": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
        "emotion": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
        "intention": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
        "action": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
    }

    
    path=f"paper_table/data/{level}_time_stage_transformation.csv"
    for model in models:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for transformation_ in ["1-2", "2-3", "3-4", "4-5"]:
                alol_re[mental_state][transformation_]['all']+=results[model][mental_state][transformation_]['all']
                alol_re[mental_state][transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5"]:
            alol_re[mental_state][transformation_]["accuracy"] = (
                alol_re[mental_state][transformation_]["correct"]
                / alol_re[mental_state][transformation_]["all"]
            )
    with open(path,'w',encoding="UTF-8") as f:
        writer=csv.writer(f)
        writer.writerow(["None","1-2","2-3","3-4","4-5"])
        
        for mental in ["belief", "emotion", "intention", "action"]:
            writer.writerow([mental]+[alol_re[mental][transformation_]["accuracy"] for transformation_ in ["1-2", "2-3", "3-4", "4-5"]])



    
if __name__ == "__main__":
#     models=[
#     "gpt-4o-2024-05-13", 
#     "gpt-4-turbo-2024-04-09",
   
    
#     "Meta-Llama-3.1-70B-Instruct",
#     "Meta-Llama-3.1-8B-Instruct",
    
#     "Mixtral-8x7B-Instruct-v0.1",
#     "Mistral-7B-Instruct-v0.3",
    
#     "Qwen2-72B-Instruct",
#     "Qwen2-7B-Instruct",
    
#     "DeepSeek-V2-Lite-Chat",
    
#     "glm-4-9b-chat", 
# ]
#     draw_table_time_stage(models,"level1")
    
    models=[
    "gpt-4o-2024-05-13", 
    "gpt-4-turbo-2024-04-09",
   
    
    "Meta-Llama-3.1-70B-Instruct",
    "Meta-Llama-3.1-8B-Instruct",
    
    "Mixtral-8x7B-Instruct-v0.1",
    "Mistral-7B-Instruct-v0.3",
    
    "Qwen2-72B-Instruct",
    "Qwen2-7B-Instruct",
    
    "DeepSeek-V2-Lite-Chat",
    
    "glm-4-9b-chat", 
]
    
#     draw_table_time_stage_7(models,"level1")
#     draw_table_time_stage_6(models,"level1")
#    #draw_table_time_stage_4(models,"level1")
    # models=["Meta-Llama-3.1-8B-Instruct","Meta-Llama-3.1-70B-Instruct","Mistral-7B-Instruct-v0.3","Mixtral-8x7B-Instruct-v0.1","Qwen2-7B-Instruct","Qwen2-72B-Instruct","DeepSeek-V2-Lite-Chat","gpt-4-turbo-2024-04-09","gpt-4o-2024-05-13","glm-4-9b-chat"]
    #print_table_llm_mental_q_type_accuracy(models,"level1CoT")
    print_table_llm_mental_q_type_split(models,"level1CoT")

