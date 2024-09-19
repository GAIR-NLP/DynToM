import json
from math import e
from multi_hop.multi_hop_ import load_answer_ground_truth
from analysis.analysis_question import influence_mapping
import matplotlib.pyplot as plt
import numpy as np

def identify(script, model_name,information_level):

    e_results = {
        "full_correct": 0,
        "local_error": 0,
        "full_error": 0,
        "restoration error": 0,
        "all":0
    }

    _, _, result = load_answer_ground_truth(
        script, model_name, information_type=information_level
    )
    # print(result)

    for q_id, _ in result.items():
        if q_id not in influence_mapping:
            continue
        
        e_results["all"] += 1

        pre = influence_mapping[q_id]
        pre_1 = pre[0]
        pre_2 = pre[1]

        if result[q_id] == 1:
            if result[pre_1] == 1 and result[pre_2] == 1:
                e_results["full_correct"] += 1
                
            else:
                e_results["restoration error"] += 1
                
        else:
            if result[pre_1] == 1 and result[pre_2] == 1:
                e_results["local_error"] += 1
                
            else:
                e_results["full_error"] += 1
    
    path=f"multi_hop/data/trial{script}/{information_level}_multi_hop_{model_name}.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(e_results, f, indent=4)   

def draw_bar(error_type,results,model):
    x = np.arange(len(error_type))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#297A8E', '#CAE11F', '#40BD72', '#472C7A']

    fig, ax = plt.subplots(layout='constrained')

    for mental, measurement in results.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
        ax.bar_label(rects, padding=3,rotation=45)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Status')
    ax.set_ylabel('Percentage')
    ax.set_title("percentage of 4 types of status")
    ax.set_xticks(x + width*(len(results)/2-0.5), error_type)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 0.65)

    plt.show()
    fig.savefig(f"multi_hop/{model}_status.pdf", bbox_inches='tight')
    
def all(scrip_ids,model):
    new_results={
        "full_correct": 0,
        "local_error": 0,
        "full_error": 0,
        "restoration error": 0,
        "all":0
    }
    newpre_results={
        "full_correct": 0,
        "local_error": 0,
        "full_error": 0,
        "restoration error": 0,
        "all":0
    }
    
    for id in scrip_ids:
        path=f"multi_hop/data/trial{id}/level1new_multi_hop_{model}.json"
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)
        new_results["full_correct"]+=data["full_correct"]
        new_results["local_error"]+=data["local_error"]
        new_results["full_error"]+=data["full_error"]
        new_results["restoration error"]+=data["restoration error"]
        new_results["all"]+=data["all"]
    
    for id in scrip_ids:
        path=f"multi_hop/data/trial{id}/level1newpre_multi_hop_{model}.json"
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)
        newpre_results["full_correct"]+=data["full_correct"]
        newpre_results["local_error"]+=data["local_error"]
        newpre_results["full_error"]+=data["full_error"]
        newpre_results["restoration error"]+=data["restoration error"]
        newpre_results["all"]+=data["all"]
    
    for e_type, _ in new_results.items():
        if e_type == "all":
            continue
        new_results[e_type]=new_results[e_type]/new_results["all"]
    
    for e_type, _ in newpre_results.items():
        if e_type == "all":
            continue
        newpre_results[e_type]=newpre_results[e_type]/newpre_results["all"]
        
    results={
        "normal":[round(new_results[e_type],3) for e_type in ["full_correct", "local_error","full_error","restoration error"]],
        "normal+tips":[round(newpre_results[e_type],3) for e_type in ["full_correct", "local_error","full_error","restoration error"]]
    }
    
    draw_bar(["full_correct", "local_error","full_error","restoration error"],results,model)

if __name__ == "__main__":
    scrip_ids = [594,182,492,762]
    # [85,182,234,492,594]
    # ,762,786,895,925,939]
    level = "level1new"
    model = ["gpt-4-turbo-2024-04-09","gpt-4o-2024-05-13"]
    for script_id in scrip_ids:
        for model_ in model:
            identify(script_id, model_, level)
    
    level = "level1newpre"
    for script_id in scrip_ids:
        for model_ in model:
            identify(script_id, model_, level)
    
    for model_ in model:
        all(scrip_ids,model_)
                