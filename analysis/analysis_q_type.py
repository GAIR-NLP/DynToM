import json
from analysis.analysis_question import load_answer_ground_truth
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


def find_menta_q_type(q_id):
    for q_type in ["understanding", "transformation", "influence"]:
        for mental_state in ["belief", "emotion", "intention", "action"]:
            if q_id in classification[q_type][mental_state]:
                return q_type, mental_state
    return None, None


def analysis(model, ids, information_level):
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
        _, _, result = load_answer_ground_truth(id, model, information_level)
        #print(result)

        for q_id, _ in result.items():
            q_type, mental_state = find_menta_q_type(q_id)
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

    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_all.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f)

def analysis_split_mental_q_type(model, ids, information_level):
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
        _, _, result = load_answer_ground_truth(id, model, information_level)
        #print(result)

        for q_id, _ in result.items():
            q_type, mental_state = find_menta_q_type(q_id)
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
    
    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_all_mental_q_type.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f)


if __name__ == "__main__":
    models = list(model_name_2_class.keys())
    ids = range(50, 1050)
    information_level = "level1"
    for model in models:
        analysis_split_mental_q_type(model, ids, information_level)
