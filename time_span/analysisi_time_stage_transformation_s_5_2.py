from math import inf
from analysis.analysis_question import load_answer_ground_truth
from analysis.analysis_q_type import find_menta_q_type
import json
from llm_api.inference import model_name_2_class


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
        "type_d_why_5": "1-2",
        "type_d_why_6": "2-3",
        "type_d_why_7": "3-4",
        "type_d_whether_5": "1-2",
        "type_d_whether_6": "2-3",
        "type_d_whether_7": "3-4",
    },
    "intention": {
        "type_d_why_9": "1-2",
        "type_d_why_10": "2-3",
        "type_d_why_11": "3-4",
        "type_d_whether_9": "1-2",
        "type_d_whether_10": "2-3",
        "type_d_whether_11": "3-4",
    },
    "action": {
        "type_d_why_13": "1-2",
        "type_d_why_14": "2-3",
        "type_d_why_15": "3-4",
        "type_d_whether_13": "1-2",
        "type_d_whether_14": "2-3",
        "type_d_whether_15": "3-4",
    },
}


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
            q_type, mental_state = find_menta_q_type(q_id)
            if q_id in transformation[mental_state]:
                if mental_state=="belief":
                    if transformation[mental_state][q_id]=="2-3":
                        if information_level=="level1":
                            print(id, q_id, result[q_id])
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

    path = f"time_span/compare_5_without_5/{model}_{information_level}_time_stage_transformation_s5.json"
    with open(path, "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    models = ["gpt-4o-2024-05-13"]
    ids = range(1180,1190)
    information_level = "level1"
    for model in models:
        analysis(model, ids, information_level)
    information_level = "level2"
    for model in models:
        analysis(model, ids, information_level)