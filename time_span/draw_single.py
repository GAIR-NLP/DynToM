import json
import csv
import matplotlib.pyplot as plt
import numpy as np

# def draw(models,level,time_span:int):
#     """print the results of the analysis
#     """
#     results={}
#     alol_re={}
#     for model  in models:
#         path=f"time_span/data/{model}_{level}_time_stage_transformation_s{time_span}.json"
#         with open(path) as f:
#             dicts=json.load(f)
#             results[model]=dicts
    
#     for mental in ["belief", "emotion", "intention", "action"]:
#         alol_re[mental]={}
#         for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#             alol_re[mental][transformation_]={
#                 "all":0,
#                 "correct":0
#             }
    
    
#     path=f"paper_table/data/{level}_time_stage_transformation_s{time_span}.csv"
#     for model in models:
#         for mental_state in ["belief", "emotion", "intention", "action"]:
#             for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#                 alol_re[mental_state][transformation_]['all']+=results[model][mental_state][transformation_]['all']
#                 alol_re[mental_state][transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
#     for mental_state in ["belief", "emotion", "intention", "action"]:
#         for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#             alol_re[mental_state][transformation_]["accuracy"] = (
#                 alol_re[mental_state][transformation_]["correct"]
#                 / alol_re[mental_state][transformation_]["all"]
#             )
    
#     # data from https://allisonhorst.github.io/palmerpenguins/

#     time_stage = [f"{i}-{i+1}" for i in range(1,time_span)]
#     mental = {
#         "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
#         "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
#         "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
#         "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
#     }
#     for mental_state in ["belief", "emotion", "intention", "action"]:
#         for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#             mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

#     x = np.arange(len(time_stage))  # the label locations
#     width = 0.2  # the width of the bars
#     multiplier = 0
    
#     color=['#076678', '#8EC07C', '#F28482', '#FFABBE']

#     fig, ax = plt.subplots(layout='constrained')

#     for mental, measurement in mental.items():
#         offset = width * multiplier
#         rects = ax.bar(x + offset, measurement, width, label=mental,color=color[multiplier])
#         ax.bar_label(rects, padding=3,rotation=45,weight='bold')
#         multiplier += 1

#     # Add some text for labels, title and custom x-axis tick labels, etc.
#     ax.set_xlabel('Time Span',weight='bold')
#     ax.set_ylabel('Accuracy',weight='bold')
#     ax.set_title(f"LLM's performance in {time_span} scenarios",weight='bold')
#     ax.set_xticks(x + width*1.5, time_stage)
#     ax.legend(loc='upper left', ncols=2)
#     ax.set_ylim(0, 1)

#     plt.show()
#     fig.savefig(f"time_span/data/time_stage_transformation_s{time_span}.pdf", bbox_inches='tight')


# def draw_no_mental_split(models,level,time_span:int,id:int):
#     """print the results of the analysis
#     """
#     results={}
#     alol_re={}
#     for model  in models:
#         path=f"time_span/data7/{id}_{model}_{level}_time_stage_transformation_s{time_span}.json"
#         with open(path) as f:
#             dicts=json.load(f)
#             results[model]=dicts
    
    
#     for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#             alol_re[transformation_]={
#                 "all":0,
#                 "correct":0
#             }
    
    
#     path=f"paper_table/data7/{id}_{level}_time_stage_transformation_s{time_span}.csv"
#     for model in models:
#         for mental_state in ["belief", "emotion", "intention", "action"]:
#             for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#                 alol_re[transformation_]['all']+=results[model][mental_state][transformation_]['all']
#                 alol_re[transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
    
#     for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#             alol_re[transformation_]["accuracy"] = round(
#                 alol_re[transformation_]["correct"]
#                 / alol_re[transformation_]["all"],2
#             )
    
#     # data from https://allisonhorst.github.io/palmerpenguins/

#     time_stage = [f"{i}-{i+1}" for i in range(1,time_span)]
#     final_=[alol_re[transformation_]["accuracy"] for transformation_ in time_stage]
#     print(final_)
#     # for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#     #     final_[transformation_]=alol_re[transformation_]["accuracy"]
#     # mental = {
#     #     "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
#     #     "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
#     #     "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
#     #     "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
#     # }
#     # for mental_state in ["belief", "emotion", "intention", "action"]:
#     #     for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
#     #         mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

#     x = np.arange(len(time_stage))  # the label locations
#     width = 0.2  # the width of the bars
#     multiplier = 0
    
#     color=['#076678', '#8EC07C', '#F28482', '#FFABBE']

#     fig, ax = plt.subplots(layout='constrained')

    
#     offset = width * multiplier
#     rects = ax.bar(x + offset, final_, width,color=color[multiplier])
#     ax.bar_label(rects, padding=3,rotation=45,weight='bold')
#     multiplier += 1

#     # Add some text for labels, title and custom x-axis tick labels, etc.
#     ax.set_xlabel('Time Span',weight='bold')
#     ax.set_ylabel('Accuracy',weight='bold')
#     ax.set_title(f"LLM's performance in {time_span} scenarios",weight='bold')
#     ax.set_xticks(x , time_stage)
#     #ax.legend(loc='upper left', ncols=2)
#     ax.set_ylim(0.3, 0.75)

#     plt.show()
#     fig.savefig(f"time_span/data/time_stage_transformation_s{time_span}_final.pdf", bbox_inches='tight')


def draw_no_mental_split_single_model(model,level,time_span:int,id:int):
    """print the results of the analysis
    """
    results={}
    alol_re={}
    for model  in [model]:
        path=f"time_span/data7/{id}_{model}_{level}_time_stage_transformation_s{time_span}.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    
    for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
            alol_re[transformation_]={
                "all":0,
                "correct":0
            }
    
    
    #path=f"paper_table/data7/{id}_{level}_time_stage_transformation_s{time_span}.csv"
    for model in [model]:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
                alol_re[transformation_]['all']+=results[model][mental_state][transformation_]['all']
                alol_re[transformation_]['correct']+=results[model][mental_state][transformation_]['correct']
    
    
    for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
            alol_re[transformation_]["accuracy"] = round(
                alol_re[transformation_]["correct"]
                / alol_re[transformation_]["all"],2
            )
    
    # data from https://allisonhorst.github.io/palmerpenguins/

    time_stage = [f"{i}-{i+1}" for i in range(1,time_span)]
    final_=[alol_re[transformation_]["accuracy"] for transformation_ in time_stage]
    print(final_)
    # for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
    #     final_[transformation_]=alol_re[transformation_]["accuracy"]
    # mental = {
    #     "belief": [alol_re["belief"][transformation_]["accuracy"] for transformation_ in time_stage],
    #     "emotion": [alol_re["emotion"][transformation_]["accuracy"] for transformation_ in time_stage],
    #     "intention": [alol_re["intention"][transformation_]["accuracy"] for transformation_ in time_stage],
    #     "action": [alol_re["action"][transformation_]["accuracy"] for transformation_ in time_stage],
    # }
    # for mental_state in ["belief", "emotion", "intention", "action"]:
    #     for transformation_ in [f"{i}-{i+1}" for i in range(1,time_span)]:
    #         mental[mental_state][time_stage.index(transformation_)]=round(mental[mental_state][time_stage.index(transformation_)],2)

    x = np.arange(len(time_stage))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    color=['#076678', '#8EC07C', '#F28482', '#FFABBE']

    fig, ax = plt.subplots(layout='constrained')

    
    offset = width * multiplier
    rects = ax.bar(x + offset, final_, width,color=color[multiplier])
    ax.bar_label(rects, padding=3,rotation=45,weight='bold')
    multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Time Span',weight='bold')
    ax.set_ylabel('Accuracy',weight='bold')
    ax.set_title(f"LLM's performance in {time_span} scenarios",weight='bold')
    ax.set_xticks(x , time_stage)
    #ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0.3, 0.75)

    plt.show()
    fig.savefig(f"time_span/data7/{id}_time_stage_transformation_s{time_span}_final_{model}.pdf", bbox_inches='tight')


if __name__ == "__main__":
    models = ["gpt-4-turbo-2024-04-09", "gpt-4o-2024-05-13"]
    level="level1"
    ids=range(1200,1210)
    for time_span in range(7,8):
        #draw_no_mental_split(models,level,time_span)
        
        for model in models:
            for id in ids:
                draw_no_mental_split_single_model(model,level,time_span,id)