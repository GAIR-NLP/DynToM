from analysis.analysis_question import load_answer_ground_truth

import json


transformation = {
    "belief": {
        "type_d_why_1": "1-2",
        "type_d_why_2": "2-3",
        "type_d_why_3": "3-4",
        
        
        
        "type_d_whether_1": "1-2",
        "type_d_whether_2": "2-3",
        "type_d_whether_3": "3-4",
        
        
    },
    "emotion": {
        "type_d_why_4": "1-2",
        "type_d_why_5": "2-3",
        "type_d_why_6": "3-4",
        
        "type_d_whether_4": "1-2",
        "type_d_whether_5": "2-3",
        "type_d_whether_6": "3-4",
    },
    "intention": {
        "type_d_why_7": "1-2",
        "type_d_why_8": "2-3",
        "type_d_why_9": "3-4",
        
        "type_d_whether_7": "1-2",
        "type_d_whether_8": "2-3",
        "type_d_whether_9": "3-4",
    },
    "action": {
        "type_d_why_10": "1-2",
        "type_d_why_11": "2-3",
        "type_d_why_12": "3-4",
        
        "type_d_whether_10": "1-2",
        "type_d_whether_11": "2-3",
        "type_d_whether_12": "3-4",
    },
}
def find_menta_q_type(q_id):
    print(q_id)
    for mental_state in ["belief", "emotion", "intention", "action"]:
        print(mental_state)
        if q_id in transformation[mental_state]:
            return mental_state
    return None

def analysis(model, ids, information_level):
    """ analysis the time stage transformation

    Args:
        model (_type_): _description_
        ids (_type_): _description_
        information_level (_type_): _description_
    """
    results = {
        "belief": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            
            
        },
        "emotion": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            
            
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

    for id in ids:
        _, _, result = load_answer_ground_truth(id, model, information_level)
        # print(result)

        for q_id, _ in result.items():
            mental_state = find_menta_q_type(q_id)
            if mental_state is None:
                continue
            if q_id in transformation[mental_state]:
                results[mental_state][transformation[mental_state][q_id]]["all"] += 1
                results[mental_state][transformation[mental_state][q_id]][
                    "correct"
                ] += result[q_id]

    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4"]:
            results[mental_state][transformation_]["accuracy"] = (
                results[mental_state][transformation_]["correct"]
                / results[mental_state][transformation_]["all"]
            )

    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_time_stage_transformation_s4.json"
    with open(path, "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    models = ["DeepSeek-V2-Lite-Chat"]
    ids = range(1165, 1170)
    information_level = "level1"
    for model in models:
        analysis(model, ids, information_level)