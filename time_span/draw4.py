import json
import csv
import matplotlib.pyplot as plt
import numpy as np


def draw_no_mental_split_single_model(model,levels,time_span:int):
    """print the results of the analysis
    """
    finals={}
    time_stage = [f"{i}-{i+1}" for i in range(1,time_span-3)]
    for level in levels:
        results={}
        alol_re={}
        for model  in [model]:
            path=f"time_span/compare_7_without_7/{model}_{level}_time_stage_transformation_s{time_span}.json"
            with open(path) as f:
                dicts=json.load(f)
                results[model]=dicts
        
        
        for transformation_ in time_stage:
                alol_re[transformation_]={
                    "all":0,
                    "correct":0
                }
                
        for model in [model]:
            for mental_state in ["belief", "emotion", "intention", "action"]:
                for transformation_ in time_stage:
                    alol_re[transformation_]['all']+=results[model][mental_state][transformation_]['all']
                    alol_re[transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
        
        
        for transformation_ in time_stage:
                alol_re[transformation_]["accuracy"] = round(
                    alol_re[transformation_]["correct"]
                    / alol_re[transformation_]["all"],2
                )
        
        # data from https://allisonhorst.github.io/palmerpenguins/

        
        final_=[alol_re[transformation_]["accuracy"] for transformation_ in time_stage]
        
        finals[level]=final_
    
    

    x = np.arange(len(time_stage))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color= ['#CC88B0', '#998DB7', '#DBE0ED', '#87B5B2']

    fig, ax = plt.subplots(layout='constrained')

    for level in levels:
        offset = width * multiplier
        rects = ax.bar(x + offset, finals[level], width,color=color[multiplier],label="w/ the fifth scenario" if level=="level1" else "w/o the fifth scenario")
        ax.bar_label(rects, padding=3,rotation=45,weight='bold')
        multiplier += 1
    # offset = width * multiplier
    # rects = ax.bar(x + offset, final_, width,color=color[multiplier])
    # ax.bar_label(rects, padding=3,rotation=45,weight='bold')
    # multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Time Span',weight='bold')
    ax.set_ylabel('Accuracy',weight='bold')
    ax.set_title(f"Comparation of LLM's performance between w/ and w/o the fifth scenario",weight='bold')
    ax.set_xticks(x , time_stage)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0.0, 0.75)

    plt.show()
    fig.savefig(f"time_span/compare_7_without_7/time_stage_transformation_s{time_span}_compare_{model}.pdf", bbox_inches='tight')


if __name__ == "__main__":
    models = ["gpt-4o-2024-05-13"]
    levels=["level1","level2"]
    for time_span in range(7,8):
        # draw_no_mental_split(models,level,time_span)
        # draw(models,level,time_span)
        for model in models:
            draw_no_mental_split_single_model(model,levels,time_span)