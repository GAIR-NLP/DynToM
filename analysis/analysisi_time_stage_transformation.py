from analysis.analysis_question import load_answer_ground_truth
from analysis.analysis_q_type import find_menta_q_type
import json
from llm_api.inference import model_name_2_class


transformation = {
    "belief": {
        "type_d_why_1": "1-2",
        "type_d_why_2": "2-3",
        "type_d_why_3": "3-4",
        "type_d_why_4": "4-5",
        "type_d_whether_1": "1-2",
        "type_d_whether_2": "2-3",
        "type_d_whether_3": "3-4",
        "type_d_whether_4": "4-5",
    },
    "emotion": {
        "type_d_why_5": "1-2",
        "type_d_why_6": "2-3",
        "type_d_why_7": "3-4",
        "type_d_why_8": "4-5",
        "type_d_whether_5": "1-2",
        "type_d_whether_6": "2-3",
        "type_d_whether_7": "3-4",
        "type_d_whether_8": "4-5",
    },
    "intention": {
        "type_d_why_9": "1-2",
        "type_d_why_10": "2-3",
        "type_d_why_11": "3-4",
        "type_d_why_12": "4-5",
        "type_d_whether_9": "1-2",
        "type_d_whether_10": "2-3",
        "type_d_whether_11": "3-4",
        "type_d_whether_12": "4-5",
    },
    "action": {
        "type_d_why_13": "1-2",
        "type_d_why_14": "2-3",
        "type_d_why_15": "3-4",
        "type_d_why_16": "4-5",
        "type_d_whether_13": "1-2",
        "type_d_whether_14": "2-3",
        "type_d_whether_15": "3-4",
        "type_d_whether_16": "4-5",
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
            "4-5": {"all": 0, "correct": 0},
        },
        "emotion": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
        "intention": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
        "action": {
            "1-2": {"all": 0, "correct": 0},
            "2-3": {"all": 0, "correct": 0},
            "3-4": {"all": 0, "correct": 0},
            "4-5": {"all": 0, "correct": 0},
        },
    }

    for id in ids:
        _, _, result = load_answer_ground_truth(id, model, information_level)
        # print(result)

        for q_id, _ in result.items():
            q_type, mental_state = find_menta_q_type(q_id)
            if q_id in transformation[mental_state]:
                results[mental_state][transformation[mental_state][q_id]]["all"] += 1
                results[mental_state][transformation[mental_state][q_id]][
                    "correct"
                ] += result[q_id]

    for mental_state in ["belief", "emotion", "intention", "action"]:
        for transformation_ in ["1-2", "2-3", "3-4", "4-5"]:
            results[mental_state][transformation_]["accuracy"] = (
                results[mental_state][transformation_]["correct"]
                / results[mental_state][transformation_]["all"]
            )

    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_time_stage_transformation.json"
    with open(path, "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    models = list(model_name_2_class.keys())
    ids = range(50, 1050)
    information_level = "level1"
    for model in models:
        analysis(model, ids, information_level)