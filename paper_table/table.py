import json
import csv
import matplotlib.pyplot as plt
import numpy as np
from sympy import rotations


def print_table_llm_mental_q_type_accuracy(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_all.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    path="paper_table/data/llm_mental_q_type_accuracy.csv"
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
    
    path="paper_table/data/llm_mental_q_type_split.csv"
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

    
    path="paper_table/data/time_stage_transformation.csv"
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


def draw_table_time_stage(models,level):
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

    
    path="paper_table/data/time_stage_transformation.csv"
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
    
    # data from https://allisonhorst.github.io/palmerpenguins/

    time_stage = ["1-2", "2-3", "3-4", "4-5"]
    mental = {
        "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
        "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
        "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
        "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
    }
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5"]:
            mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

    x = np.arange(len(time_stage))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#297A8E', '#CAE11F', '#40BD72', '#472C7A']

    fig, ax = plt.subplots(layout='constrained')

    for mental, measurement in mental.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
        ax.bar_label(rects, padding=3,rotation=45)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Time Span')
    ax.set_ylabel('Accuracy')
    ax.set_title("LLM's performance of transformation")
    ax.set_xticks(x + width*1.5, time_stage)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 0.5)

    plt.show()
    fig.savefig("paper_table/data/time_stage_transformation.pdf", bbox_inches='tight')


def draw_table_time_stage_7(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_time_stage_transformation_s7.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    alol_re={
        "belief": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            "6-7": {"all": 0, "correct": 0},
        },
        "emotion": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            "6-7": {"all": 0, "correct": 0},
        },
        "intention": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            "6-7": {"all": 0, "correct": 0},
        },
        "action": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            "6-7": {"all": 0, "correct": 0},
        },
    }

    
    #path="paper_table/data/time_stage_transformation7.csv"
    for model in models:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7"]:
                alol_re[mental_state][transformation_]['all']+=results[model][mental_state][transformation_]['all']
                alol_re[mental_state][transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7"]:
            alol_re[mental_state][transformation_]["accuracy"] = (
                alol_re[mental_state][transformation_]["correct"]
                / alol_re[mental_state][transformation_]["all"]
            )
    
    # data from https://allisonhorst.github.io/palmerpenguins/

    time_stage = ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7"]
    mental = {
        "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
        "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
        "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
        "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
    }
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7"]:
            mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

    x = np.arange(len(time_stage))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#297A8E', '#CAE11F', '#40BD72', '#472C7A', '#F9A03F', '#F9D03F', '#F9F03F']

    fig, ax = plt.subplots(layout='constrained')

    for mental, measurement in mental.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
        ax.bar_label(rects, padding=3,rotation=45)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Time Span')
    ax.set_ylabel('Accuracy')
    ax.set_title("LLM's performance of transformation")
    ax.set_xticks(x + width*1.5, time_stage)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 0.7)

    plt.show()
    fig.savefig("paper_table/data/time_stage_transformation7.pdf", bbox_inches='tight')
    
def draw_table_time_stage_6(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_time_stage_transformation_s6.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    alol_re={
        "belief": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            
        },
        "emotion": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            
        },
        "intention": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            
        },
        "action": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            
        },
    }

    
    #path="paper_table/data/time_stage_transformation7.csv"
    for model in models:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6"]:
                alol_re[mental_state][transformation_]['all']+=results[model][mental_state][transformation_]['all']
                alol_re[mental_state][transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6"]:
            alol_re[mental_state][transformation_]["accuracy"] = (
                alol_re[mental_state][transformation_]["correct"]
                / alol_re[mental_state][transformation_]["all"]
            )
    
    # data from https://allisonhorst.github.io/palmerpenguins/

    time_stage = ["1-2", "2-3", "3-4", "4-5", "5-6"]
    mental = {
        "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
        "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
        "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
        "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
    }
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6"]:
            mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

    x = np.arange(len(time_stage))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#297A8E', '#CAE11F', '#40BD72', '#472C7A']

    fig, ax = plt.subplots(layout='constrained')

    for mental, measurement in mental.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
        ax.bar_label(rects, padding=3,rotation=45)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Time Span')
    ax.set_ylabel('Accuracy')
    ax.set_title("LLM's performance of transformation")
    ax.set_xticks(x + width*1.5, time_stage)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 0.7)

    plt.show()
    fig.savefig("paper_table/data/time_stage_transformation6.pdf", bbox_inches='tight')
    
def draw_table_time_stage_4(models,level):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_time_stage_transformation_s4.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    alol_re={
        "belief": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            
            
        },
        "emotion": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
            "5-6": {"all": 0, "correct": 0},
            
        },
        "intention": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            
            
        },
        "action": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            
            
        },
    }

    
    #path="paper_table/data/time_stage_transformation7.csv"
    for model in models:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for transformation_ in ["1-2", "2-3", "3-4"]:
                alol_re[mental_state][transformation_]['all']+=results[model][mental_state][transformation_]['all']
                alol_re[mental_state][transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4"]:
            alol_re[mental_state][transformation_]["accuracy"] = (
                alol_re[mental_state][transformation_]["correct"]
                / alol_re[mental_state][transformation_]["all"]
            )
    
    # data from https://allisonhorst.github.io/palmerpenguins/

    time_stage = ["1-2", "2-3", "3-4"]
    mental = {
        "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
        "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
        "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
        "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
    }
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4"]:
            mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

    x = np.arange(len(time_stage))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#297A8E', '#CAE11F', '#40BD72', '#472C7A']

    fig, ax = plt.subplots(layout='constrained')

    for mental, measurement in mental.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
        ax.bar_label(rects, padding=3,rotation=45)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Time Span')
    ax.set_ylabel('Accuracy')
    ax.set_title("LLM's performance of transformation")
    ax.set_xticks(x + width*1.5, time_stage)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 0.7)

    plt.show()
    fig.savefig("paper_table/data/time_stage_transformation4.pdf", bbox_inches='tight')
    
    
if __name__ == "__main__":
    
    models=[
    "gpt-4o-2024-05-13", 
    "gpt-4-turbo-2024-04-09",
   
    
    # "Meta-Llama-3.1-70B-Instruct",
    "Meta-Llama-3.1-8B-Instruct",
    
    # "Mixtral-8x7B-Instruct-v0.1",
    # "Mistral-7B-Instruct-v0.3",
    
    # "Qwen2-72B-Instruct",
    # "Qwen2-7B-Instruct",
    
    "DeepSeek-V2-Lite-Chat",
    
    "glm-4-9b-chat", 
]

    draw_table_time_stage_7(models,"level1")
    draw_table_time_stage_6(models,"level1")
    draw_table_time_stage_4(models,"level1")
