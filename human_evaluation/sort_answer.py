import json

def find_true_answer(script,question):
    path=f"synthesize_data/script/data/trial{script}/question_new.json"
    with open(path) as f:
        data = json.load(f)
    
    for q_id, q in data.items():
        if q['question'] in question:
            return q['true answer'], q_id
    
    if "Please rate the difficulty of the questions" in question:
        return None, "difficulty"
    
    if "Please rate the quality of the questions and options" in question:
        return None, "quality"
     
    
    return None, None

def sort(script):
    results={}
    path=f"human_evaluation/data/script{script}/records.json"
    with open(path) as f:
        data = json.load(f)
    for record in data:
        question = record['fields']['question_content']
        true_answer, q_id = find_true_answer(script,question)
        results[q_id] = {
            'true answer': true_answer,
            'response':{
                record['responses']['question'][0]['user_id']: record['responses']['question'][0]['value'],
                record['responses']['question'][1]['user_id']: record['responses']['question'][1]['value'],
                record['responses']['question'][2]['user_id']: record['responses']['question'][2]['value'],
            }
        }
    
    path=f"human_evaluation/data/script{script}/sorted_records.json"
    with open(path,'w') as f:
        json.dump(results,f)

if __name__ == "__main__":
    script_id=[60,62,65,70,71,73,75,94,95,102,110,112,129,130]
    for i in script_id:
        sort(i)
    
    
    