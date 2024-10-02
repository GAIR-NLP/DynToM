import json
import csv
import matplotlib.pyplot as plt
import numpy as np
color=['#CC88B0', '#998DB7', '#DBE0ED', '#87B5B2']
def draw_mental(model,levels):
    results={}
    for level  in levels:
        path=f"profile_function/data/all_scripts_analysis/{model}_{level}_all.json"
        with open(path) as f:
            dicts=json.load(f)
            results[level]=dicts
    
    mental_all={}
    for level in levels:
        mental_all[level] = {
            "belief": {
                "all": 0,
                "correct": 0,
            },
            "emotion": {
                "all": 0,
                "correct": 0,
            },
            "intention": {
                "all": 0,
                "correct": 0,
            },
            "action": {
                "all": 0,
                "correct": 0,
            },
        }
    
    for level in levels:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for q_type in ["understanding", "transformation", "influence"]:
                if mental_state=="action" and q_type=="influence":
                    continue
                mental_all[level][mental_state]["all"]+=results[level][mental_state][q_type]["all"]
                mental_all[level][mental_state]["correct"]+=results[level][mental_state][q_type]["correct"]
    
    for level in levels:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            mental_all[level][mental_state]["accuracy"] = round(
                mental_all[level][mental_state]["correct"]
                / mental_all[level][mental_state]["all"],2
            )
    
    results={}
    for level  in levels:
        results[level]=[
            mental_all[level]["belief"]["accuracy"],
            mental_all[level]["emotion"]["accuracy"],
            mental_all[level]["intention"]["accuracy"],
            mental_all[level]["action"]["accuracy"]
        ]

    x = np.arange(len(["belief", "emotion", "intention", "action"]))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for level, mental_acc in results.items():
        if level =="level1":
            label="presence"
        else:
            label="absence"
        offset = width * multiplier
        rects = ax.bar(x + offset, mental_acc, width, label=label,color=color[multiplier])
        ax.bar_label(rects, padding=3,weight='bold')
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy',weight='bold')
    ax.set_xlabel('ToM Ability',weight='bold')
    ax.set_title('Accuracy between profile absence and presence',weight='bold')
    ax.set_xticks(x + width, ["belief", "emotion", "intention", "action"])
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0.3, 0.8)

    plt.show()
    fig.savefig(f"profile_function/data/compare_mental.pdf", bbox_inches='tight')

def draw_q_type(model,levels):
    results={}
    for level  in levels:
        path=f"profile_function/data/all_scripts_analysis/{model}_{level}_all.json"
        with open(path) as f:
            dicts=json.load(f)
            results[level]=dicts
    
    mental_all={}
    for level in levels:
        mental_all[level] = {
            "understanding": {
                "all": 0,
                "correct": 0,
            },
            "transformation": {
                "all": 0,
                "correct": 0,
            },
            "influence": {
                "all": 0,
                "correct": 0,
            }
        }
    
    for level in levels:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for q_type in ["understanding", "transformation", "influence"]:
                if mental_state=="action" and q_type=="influence":
                    continue
                mental_all[level][q_type]["all"]+=results[level][mental_state][q_type]["all"]
                mental_all[level][q_type]["correct"]+=results[level][mental_state][q_type]["correct"]
    
    for level in levels:
        for q_type in ["understanding", "transformation", "influence"]:
            mental_all[level][q_type]["accuracy"] = round(
                mental_all[level][q_type]["correct"]
                / mental_all[level][q_type]["all"],2
            )
    
    results={}
    for level  in levels:
        results[level]=[
            mental_all[level]["understanding"]["accuracy"],
            mental_all[level]["transformation"]["accuracy"],
            mental_all[level]["influence"]["accuracy"]
        ]

    x = np.arange(len(["understanding", "transformation", "influence"]))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for level, mental_acc in results.items():
        if level =="level1":
            label="presence"
        else:
            label="absence"
        offset = width * multiplier
        rects = ax.bar(x + offset, mental_acc, width, label=label,color=color[multiplier])
        ax.bar_label(rects, padding=3,weight='bold')
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy',weight='bold')
    ax.set_xlabel('Question Type',weight='bold')
    ax.set_title('Accuracy between profile absence and presence',weight='bold')
    ax.set_xticks(x + width, ["understanding", "transformation", "influence"])
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0.3, 0.6)

    plt.show()
    fig.savefig(f"profile_function/data/compare_q_type.pdf", bbox_inches='tight')

if __name__=="__main__":
    levels = ["level1absenceprofile",'level1']
    model="gpt-4o-2024-05-13"
    draw_mental(model,levels)
    draw_q_type(model,levels)