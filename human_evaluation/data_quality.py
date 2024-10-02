import json

def question_quality_single(script_id):
    path = f"human_evaluation/data/script{script_id}/sorted_records.json"
    
    with open(path, encoding="UTF-8") as f:
        answers = json.load(f)
    
    results = {
        "quality":0,
        "difficulty":0,
    }
    
    difficlity_count={
        1:0,
        2:0,
        3:0
    }
    
    for user in answers["difficulty"]["response"].keys():
        results["difficulty"] += int(answers["difficulty"]["response"][user])
        results["quality"] += int(answers["quality"]["response"][user])
        
        difficlity_count[int(answers["difficulty"]["response"][user])] += 1
    
    results["difficulty"] /= len(answers["difficulty"]["response"])
    results["quality"] /= len(answers["quality"]["response"])
    
    results["quality"] = results["quality"] / 4 * 5 
    
    return results, difficlity_count

def question_quality_all(script_ids):
    results = {
        "quality":0,
        "difficulty":0,
    }
    
    difficulty_count={
        1:0,
        2:0,
        3:0
    }
    
    for script_id in script_ids:
        result, difficulty_count_single=question_quality_single(script_id)
        results["quality"] += result["quality"]
        results["difficulty"] += result["difficulty"]
        
        for key in difficulty_count.keys():
            difficulty_count[key] += difficulty_count_single[key]
        
    
    results["quality"] /= len(script_ids)
    results["difficulty"] /= len(script_ids)
    
    sum_=0
    for rate in difficulty_count.keys():
        sum_ += difficulty_count[rate]
    
    for rate in difficulty_count.keys():
        difficulty_count[rate] /= sum_
    
    return results, difficulty_count

def data_quality():
    path="human_evaluation/data/meta/records.json"
    with open(path) as f:
        meta=json.load(f)
    
    results={
        "rating_of_mental_state_influence":0, # 
        "rating_of_mental_state_change":0, # RQ3-Dynamism:
        "rating_of_plot_consistency":0, #  RQ1-Coherence1
        "rating_of_social_context_consistency":0, #  RQ1-Coherence2
        "rating_of_dialogue_real":0 #RQ2-Authenticity
    }
    
    for record in meta:
        for key in results.keys():
            sum_=0
            for user in record["responses"][key]:
                sum_+=int(user["value"])
            results[key] += sum_/len(record["responses"][key])
    
    for key in results.keys():
        results[key] /= len(meta)
    
    print(results)

def count_percentage_of_real(key="rating_of_dialogue_real"):
    path="human_evaluation/data/meta/records.json"
    with open(path) as f:
        meta=json.load(f)
    
    results={
        key:{
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
        }
    }
    
    for record in meta:
        for key in results.keys():
            for user in record["responses"][key]:
                results[key][int(user["value"])] += 1
    
    sum_=0
    for key in results.keys():
        for rating in results[key].keys():
            sum_+=results[key][rating]
    
    for key in results.keys():
        for rating in results[key].keys():
            results[key][rating] /= sum_
    
    print(results)

if __name__ == "__main__":
    print(question_quality_all([60,62,65,70,71,73,75,94,95,102,110,112,129,130]))
    data_quality()
    # count_percentage_of_real(key="rating_of_mental_state_change")