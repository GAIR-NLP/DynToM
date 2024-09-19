import json
from unittest import result
# from analysis.analysis_question import load_answer_ground_truth
from llm_api.inference import model_name_2_class

classification = {
    "understanding": {
        "belief": [
            "type_a_what_1",
            "type_a_what_2",
            "type_a_what_3",
            "type_a_what_4",
            "type_a_what_5",
        ],
        "emotion": [
            "type_a_what_6",
            "type_a_what_7",
            "type_a_what_8",
            "type_a_what_9",
            "type_a_what_10",
        ],
        "intention": [
            "type_a_what_11",
            "type_a_what_12",
            "type_a_what_13",
            "type_a_what_14",
            "type_a_what_15",
        ],
        "action": [
            "type_a_what_16",
            "type_a_what_17",
            "type_a_what_18",
            "type_a_what_19",
            "type_a_what_20",
        ],
    },
    "transformation": {
        "belief": [
            "type_d_how_1",
            "type_d_why_1",
            "type_d_why_2",
            "type_d_why_3",
            "type_d_why_4",
            "type_d_whether_1",
            "type_d_whether_2",
            "type_d_whether_3",
            "type_d_whether_4",
        ],
        "emotion": [
            "type_d_how_2",
            "type_d_why_5",
            "type_d_why_6",
            "type_d_why_7",
            "type_d_why_8",
            "type_d_whether_5",
            "type_d_whether_6",
            "type_d_whether_7",
            "type_d_whether_8",
        ],
        "intention": [
            "type_d_how_3",
            "type_d_why_9",
            "type_d_why_10",
            "type_d_why_11",
            "type_d_why_12",
            "type_d_whether_9",
            "type_d_whether_10",
            "type_d_whether_11",
            "type_d_whether_12",
        ],
        "action": [
            "type_d_how_4",
            "type_d_why_13",
            "type_d_why_14",
            "type_d_why_15",
            "type_d_why_16",
            "type_d_whether_13",
            "type_d_whether_14",
            "type_d_whether_15",
            "type_d_whether_16",
        ],
    },
    "influence": {
        "belief": [
            "type_c_how_1",
            "type_c_how_2",
            "type_c_how_3",
            "type_c_how_4",
            "type_c_how_5",
        ],
        "emotion": [
            "type_c_how_6",
            "type_c_how_7",
            "type_c_how_8",
            "type_c_how_9",
            "type_c_how_10",
        ],
        "intention": [
            "type_c_how_11",
            "type_c_how_12",
            "type_c_how_13",
            "type_c_how_14",
            "type_c_how_15",
        ],
    },
}

def load_answer_ground_truth(
    script_id: int, use_id: str
):
    """load the answer and ground truth for the given script_id

    Args:
        script_id (int): _description_
        model_name (str): _description_
        information_type (str, optional): _description_. Defaults to "level1".

    Returns:
        _type_: _description_
    """
    # load the answer
    path = f"human_evaluation/data/script{script_id}/sorted_records.json"
    answers = json.load(open(path, encoding="UTF-8"))


    results = {}
    for q_id, answer in answers.items():
        if q_id == "difficulty" or q_id == "quality":
            continue
        truth=answer["true answer"]
        response=answer["response"][use_id]
        response = response.strip()
        
        if response == "none":
            results[q_id] = "none"
        else:
            results[q_id] = 1 if response == truth else 0

    return results


def find_menta_q_type(q_id):
    for q_type in ["understanding", "transformation", "influence"]:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            if q_id in classification[q_type][mental_state]:
                return q_type, mental_state
    return None, None


def analysis(user, ids):
    results = {
        "belief": {
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
            },
        },
        "emotion": {
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
            },
        },
        "intention": {
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
            },
        },
        "action": {
            "understanding": {
                "all": 0,
                "correct": 0,
            },
            "transformation": {
                "all": 0,
                "correct": 0,
            }
        },
    }

    for id in ids:
        result = load_answer_ground_truth(id, user)
        #print(result)

        for q_id, _ in result.items():
            q_type, mental_state = find_menta_q_type(q_id)
            if result[q_id] == "none":
                continue
            results[mental_state][q_type]["all"] += 1 
            results[mental_state][q_type]["correct"] += result[q_id]

    all = 0
    correct = 0
    for mental_state in ["belief", "emotion", "intention", "action"]:
        for q_type in ["understanding", "transformation", "influence"]:
            if mental_state == "action" and q_type == "influence":
                continue
            #print(mental_state, q_type)
            results[mental_state][q_type]["accuracy"] = (
                results[mental_state][q_type]["correct"]
                / results[mental_state][q_type]["all"]
            )

            all += results[mental_state][q_type]["all"]
            correct += results[mental_state][q_type]["correct"]
    results["all"] = {"all": all, "correct": correct, "accuracy": correct / all}

    path = f"human_evaluation/data/all_analysis/{user}_all.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f)

def analysis_split_mental_q_type(user, ids):
    mental_results = {
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
    
    q_type_results={
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
        },
    }

    for id in ids:
        result = load_answer_ground_truth(id, user)
        #print(result)

        for q_id, _ in result.items():
            q_type, mental_state = find_menta_q_type(q_id)
            if result[q_id] == "none":
                continue
            mental_results[mental_state]["all"] += 1
            mental_results[mental_state]["correct"] += result[q_id]
            q_type_results[q_type]["all"] += 1
            q_type_results[q_type]["correct"] += result[q_id]

    for mental_state in ["belief", "emotion", "intention", "action"]:
        mental_results[mental_state]["accuracy"] = (
            mental_results[mental_state]["correct"]
            / mental_results[mental_state]["all"]
        )
    
    for q_type in ["understanding", "transformation", "influence"]:
        q_type_results[q_type]["accuracy"] = (
            q_type_results[q_type]["correct"]
            / q_type_results[q_type]["all"]
        )
    
    results={
        "mental_state": mental_results,
        "q_type": q_type_results
    }
    
    path = f"human_evaluation/data/all_analysis/{user}_all_mental_q_type.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f)


if __name__ == "__main__":
    models = [
        "e788b2ce-fa31-492d-9e6b-67debb5b200e", "80e310da-9f43-4b71-85d4-12192220fc6a", "48b80a75-a9f9-422e-8b36-e47dfa4b3652"
    ]
    script_id=[60,62,65,70,71,73,75,94,95,102,110,112,129,130]
    
    for model in models:
        analysis(model, script_id)
        analysis_split_mental_q_type(model, script_id)
