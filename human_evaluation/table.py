import json,csv

def print_table_llm_mental_q_type_accuracy(models):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"human_evaluation/data/all_analysis/{model}_all.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    path="human_evaluation/data/human_mental_q_type_accuracy.csv"
    with open(path,'w',encoding="UTF-8") as f:
        writer=csv.writer(f)
        writer.writerow(["None","belief-u","belief-i","belief-t","emotion-u","emotion-i","emotion-t","intention-u","intention-i","intention-t","action-u","action-t","avg."])
        
        for model in models:
            writer.writerow([model]+[results[model][mental_state][q_type]["accuracy"] for mental_state in ["belief", "emotion", "intention", "action"] for q_type in ["understanding", "influence","transformation"] if not (mental_state=="action" and q_type=="influence")]+[results[model]["all"]["accuracy"]])
            
def print_table_llm_mental_q_type_split(models):
    """print the results of the analysis
    """
    results={}
    for model  in models:
        path=f"human_evaluation/data/all_analysis/{model}_all_mental_q_type.json"
        with open(path) as f:
            dicts=json.load(f)
            results[model]=dicts
    
    path="human_evaluation/data/human_mental_q_type_split.csv"
    with open(path,'w',encoding="UTF-8") as f:
        writer=csv.writer(f)
        writer.writerow(["None","belief","emotion","intention","action","understanding", "influence","transformation"])
        
        for model in models:
            writer.writerow([model]+[results[model]["mental_state"][mental_state]["accuracy"] for mental_state in ["belief", "emotion", "intention", "action"]]+[results[model]["q_type"][q_type]["accuracy"] for q_type in ["understanding", "influence","transformation"]])

if __name__ == "__main__":
    models=[
        "e788b2ce-fa31-492d-9e6b-67debb5b200e", "80e310da-9f43-4b71-85d4-12192220fc6a", "48b80a75-a9f9-422e-8b36-e47dfa4b3652"
    ]
    script_id=[60,62,65,70,71,73,75,94,95,102,110,112,129,130]
    print_table_llm_mental_q_type_accuracy(models)
    print_table_llm_mental_q_type_split(models)
    