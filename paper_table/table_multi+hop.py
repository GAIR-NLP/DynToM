import json
import csv
from math import e
import matplotlib.pyplot as plt
import numpy as np
from sympy import rotations
import matplotlib.pyplot as plt
import numpy as np

def draw_bar(error_type,results,title):
    x = np.arange(len(error_type))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#CC88B0', '#998DB7', '#DBE0ED', '#87B5B2']

    fig, ax = plt.subplots(layout='constrained')

    for mental, measurement in results.items():
        measurement= [round(i,2) for i in measurement]
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
        ax.bar_label(rects, padding=3,rotation=60,weight='bold')
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Category',weight='bold')
    ax.set_ylabel('Percentage',weight='bold')
    #ax.set_title(f"{title[0]}")
    ax.set_xticks(x + width*(len(results)/2-0.5), ["fully correct","local error","full error","restoration error"])
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 0.7)

    plt.show()
    fig.savefig(f"paper_table/data/multi_hop_{title}.pdf", bbox_inches='tight')

def print_table_llm_mental_q_type_accuracy(models,level):
    """print the results of the analysis
    """
    
    
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
    
    
    results={}
    for model  in models:
        path=f"synthesize_data/script/data/all_scripts_analysis/{model}_{level}_multi_hop.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    
    for model in models:
        for e_type in ["full_correct","local_error","full_error","restoration error"]:
            e_results[e_type]+=results[model]["all"][e_type]
        e_results["all"]+=results[model]["all"]["all"]
    for e_type in ["full_correct","local_error","full_error","restoration error"]:
        e_results[e_type]=e_results[e_type]/e_results["all"]
    draw_bar(["full_correct","local_error","full_error","restoration error"],{
        "all":[e_results["full_correct"],e_results["local_error"],e_results["full_error"],e_results["restoration error"]]
        },"0e_type")
    
    for model in models:
        for mental in ["belief", "intention", "action", "emotion"]:
            for e_type in ["full_correct","local_error","full_error","restoration error"]:
                mental_results[mental][e_type]+=results[model]['mental'][mental][e_type]
            mental_results[mental]["all"]+=results[model]["mental"][mental]["all"]
    for mental in ["belief", "intention", "action", "emotion"]:
        for e_type in ["full_correct","local_error","full_error","restoration error"]:
            mental_results[mental][e_type]=mental_results[mental][e_type]/mental_results[mental]["all"]
    draw_bar(["full_correct","local_error","full_error","restoration error"],{
        mental: [mental_results[mental]["full_correct"],mental_results[mental]["local_error"],mental_results[mental]["full_error"],mental_results[mental]["restoration error"]] for mental in ["belief", "intention", "action", "emotion"]
        },"1mental")
    
    for model in models:
        for q_type in ["transformation", "influence"]:
            for e_type in ["full_correct","local_error","full_error","restoration error"]:
                q_type_results[q_type][e_type]+=results[model]['q_type'][q_type][e_type]
            q_type_results[q_type]["all"]+=results[model]["q_type"][q_type]["all"]
    for q_type in ["transformation", "influence"]:
        for e_type in ["full_correct","local_error","full_error","restoration error"]:
            q_type_results[q_type][e_type]=q_type_results[q_type][e_type]/q_type_results[q_type]["all"]
    draw_bar(["full_correct","local_error","full_error","restoration error"],{
        q_type: [q_type_results[q_type]["full_correct"],q_type_results[q_type]["local_error"],q_type_results[q_type]["full_error"],q_type_results[q_type]["restoration error"]] for q_type in ["transformation", "influence"]},"2q_type")
            
  
if __name__ == "__main__":
    
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

    print_table_llm_mental_q_type_accuracy(models,"level1")
