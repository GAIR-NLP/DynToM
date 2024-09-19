from analysis.analysis_question import load_answer_ground_truth

import json


transformation = {
    "belief": {
        "type_d_why_1": "1-2",
        "type_d_why_2": "2-3",
        "type_d_why_3": "3-4",
        "type_d_why_4": "4-5",
        "type_d_why_5": "5-6",
        
        
        "type_d_whether_1": "1-2",
        "type_d_whether_2": "2-3",
        "type_d_whether_3": "3-4",
        "type_d_whether_4": "4-5",
        "type_d_whether_5": "5-6",
        
    },
    "emotion": {
        "type_d_why_6": "1-2",
        "type_d_why_7": "2-3",
        "type_d_why_8": "3-4",
        "type_d_why_9": "4-5",
        "type_d_why_10": "5-6",
        
        
        "type_d_whether_6": "1-2",
        "type_d_whether_7": "2-3",
        "type_d_whether_8": "3-4",
        "type_d_whether_9": "4-5",
        "type_d_whether_10": "5-6",
        
    },
    "intention": {
        "type_d_why_11": "1-2",
        "type_d_why_12": "2-3",
        "type_d_why_13": "3-4",
        "type_d_why_14": "4-5",
        "type_d_why_15": "5-6",
        
        
        "type_d_whether_11": "1-2",
        "type_d_whether_12": "2-3",
        "type_d_whether_13": "3-4",
        "type_d_whether_14": "4-5",
        "type_d_whether_15": "5-6",
        
    },
    "action": {
        "type_d_why_16": "1-2",
        "type_d_why_17": "2-3",
        "type_d_why_18": "3-4",
        "type_d_why_19": "4-5",
        "type_d_why_20": "5-6",
        
        
        "type_d_whether_16": "1-2",
        "type_d_whether_17": "2-3",
        "type_d_whether_18": "3-4",
        "type_d_whether_19": "4-5",
        "type_d_whether_20": "5-6",
        
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
        for transformation_ in ["1-2", "2-3", "3-4", "4-5", "5-6"]:
            results[mental_state][transformation_]["accuracy"] = (
                results[mental_state][transformation_]["correct"]
                / results[mental_state][transformation_]["all"]
            )

    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_time_stage_transformation_s6.json"
    with open(path, "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    models = ["DeepSeek-V2-Lite-Chat"]
    ids = range(1160, 1165)
    information_level = "level1"
    for model in models:
        analysis(model, ids, information_level)