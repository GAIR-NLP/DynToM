"""
analysis according to the classification of questions
"""

import json

# question a need question b and c answered first.
# question b&c -> a
influence_mapping = {
    "type_d_why_1": ["type_a_what_1", "type_a_what_2"],
    "type_d_why_2": ["type_a_what_2", "type_a_what_3"],
    "type_d_why_3": ["type_a_what_3", "type_a_what_4"],
    "type_d_why_4": ["type_a_what_4", "type_a_what_5"],
    "type_d_why_5": ["type_a_what_6", "type_a_what_7"],
    "type_d_why_6": ["type_a_what_7", "type_a_what_8"],
    "type_d_why_7": ["type_a_what_8", "type_a_what_9"],
    "type_d_why_8": ["type_a_what_9", "type_a_what_10"],
    "type_d_why_9": ["type_a_what_11", "type_a_what_12"],
    "type_d_why_10": ["type_a_what_12", "type_a_what_13"],
    "type_d_why_11": ["type_a_what_13", "type_a_what_14"],
    "type_d_why_12": ["type_a_what_14", "type_a_what_15"],
    "type_d_why_13": ["type_a_what_16", "type_a_what_17"],
    "type_d_why_14": ["type_a_what_17", "type_a_what_18"],
    "type_d_why_15": ["type_a_what_18", "type_a_what_19"],
    "type_d_why_16": ["type_a_what_19", "type_a_what_20"],
    "type_d_whether_1": ["type_a_what_1", "type_a_what_2"],
    "type_d_whether_2": ["type_a_what_2", "type_a_what_3"],
    "type_d_whether_3": ["type_a_what_3", "type_a_what_4"],
    "type_d_whether_4": ["type_a_what_4", "type_a_what_5"],
    "type_d_whether_5": ["type_a_what_6", "type_a_what_7"],
    "type_d_whether_6": ["type_a_what_7", "type_a_what_8"],
    "type_d_whether_7": ["type_a_what_8", "type_a_what_9"],
    "type_d_whether_8": ["type_a_what_9", "type_a_what_10"],
    "type_d_whether_9": ["type_a_what_11", "type_a_what_12"],
    "type_d_whether_10": ["type_a_what_12", "type_a_what_13"],
    "type_d_whether_11": ["type_a_what_13", "type_a_what_14"],
    "type_d_whether_12": ["type_a_what_14", "type_a_what_15"],
    "type_d_whether_13": ["type_a_what_16", "type_a_what_17"],
    "type_d_whether_14": ["type_a_what_17", "type_a_what_18"],
    "type_d_whether_15": ["type_a_what_18", "type_a_what_19"],
    "type_d_whether_16": ["type_a_what_19", "type_a_what_20"],
    "type_c_how_1": ["type_a_what_1", "type_a_what_6"],
    "type_c_how_2": ["type_a_what_2", "type_a_what_7"],
    "type_c_how_3": ["type_a_what_3", "type_a_what_8"],
    "type_c_how_4": ["type_a_what_4", "type_a_what_9"],
    "type_c_how_5": ["type_a_what_5", "type_a_what_10"],
    "type_c_how_6": ["type_a_what_1", "type_a_what_6", "type_a_what_11"],
    "type_c_how_7": ["type_a_what_2", "type_a_what_7", "type_a_what_12"],
    "type_c_how_8": ["type_a_what_3", "type_a_what_8", "type_a_what_13"],
    "type_c_how_9": ["type_a_what_4", "type_a_what_9", "type_a_what_14"],
    "type_c_how_10": ["type_a_what_5", "type_a_what_10", "type_a_what_15"],
    "type_c_how_11": ["type_a_what_11", "type_a_what_16"],
    "type_c_how_12": ["type_a_what_12", "type_a_what_17"],
    "type_c_how_13": ["type_a_what_13", "type_a_what_18"],
    "type_c_how_14": ["type_a_what_14", "type_a_what_19"],
    "type_c_how_15": ["type_a_what_15", "type_a_what_20"],
}

# question_id: what the question is about
type_time_stage_mapping = {
    "type_d_why_1": "belief:1->2",
    "type_d_why_2": "belief:2->3",
    "type_d_why_3": "belief:3->4",
    "type_d_why_4": "belief:4->5",
    "type_d_why_5": "emotion:1->2",
    "type_d_why_6": "emotion:2->3",
    "type_d_why_7": "emotion:3->4",
    "type_d_why_8": "emotion:4->5",
    "type_d_why_9": "intention:1->2",
    "type_d_why_10": "intention:2->3",
    "type_d_why_11": "intention:3->4",
    "type_d_why_12": "intention:4->5",
    "type_d_why_13": "action:1->2",
    "type_d_why_14": "action:2->3",
    "type_d_why_15": "action:3->4",
    "type_d_why_16": "action:4->5",
    "type_d_whether_1": "belief:1->2",
    "type_d_whether_2": "belief:2->3",
    "type_d_whether_3": "belief:3->4",
    "type_d_whether_4": "belief:4->5",
    "type_d_whether_5": "emotion:1->2",
    "type_d_whether_6": "emotion:2->3",
    "type_d_whether_7": "emotion:3->4",
    "type_d_whether_8": "emotion:4->5",
    "type_d_whether_9": "intention:1->2",
    "type_d_whether_10": "intention:2->3",
    "type_d_whether_11": "intention:3->4",
    "type_d_whether_12": "intention:4->5",
    "type_d_whether_13": "action:1->2",
    "type_d_whether_14": "action:2->3",
    "type_d_whether_15": "action:3->4",
    "type_d_whether_16": "action:4->5",
    "type_c_how_1": "belief->emotion:1",
    "type_c_how_2": "belief->emotion:2",
    "type_c_how_3": "belief->emotion:3",
    "type_c_how_4": "belief->emotion:4",
    "type_c_how_5": "belief->emotion:5",
    "type_c_how_6": "belief&emotion->intention:1",
    "type_c_how_7": "belief&emotion->intention:2",
    "type_c_how_8": "belief&emotion->intention:3",
    "type_c_how_9": "belief&emotion->intention:4",
    "type_c_how_10": "belief&emotion->intention:5",
    "type_c_how_11": "intention->action:1",
    "type_c_how_12": "intention->action:2",
    "type_c_how_13": "intention->action:3",
    "type_c_how_14": "intention->action:4",
    "type_c_how_15": "intention->action:5",
    "type_a_what_1": "belief:1",
    "type_a_what_2": "belief:2",
    "type_a_what_3": "belief:3",
    "type_a_what_4": "belief:4",
    "type_a_what_5": "belief:5",
    "type_a_what_6": "emotion:1",
    "type_a_what_7": "emotion:2",
    "type_a_what_8": "emotion:3",
    "type_a_what_9": "emotion:4",
    "type_a_what_10": "emotion:5",
    "type_a_what_11": "intention:1",
    "type_a_what_12": "intention:2",
    "type_a_what_13": "intention:3",
    "type_a_what_14": "intention:4",
    "type_a_what_15": "intention:5",
    "type_a_what_16": "action:1",
    "type_a_what_17": "action:2",
    "type_a_what_18": "action:3",
    "type_a_what_19": "action:4",
    "type_a_what_20": "action:5",
}
time_stage_type_mapping = {}
for key, value in type_time_stage_mapping.items():
    if value not in time_stage_type_mapping:
        time_stage_type_mapping[value] = [key]
    else:
        time_stage_type_mapping[value].append(key)

# does the question(id) need reason(multi-hop-reason) or not
reason_or_not = {
    "reason": [
        "type_d_why_1",
        "type_d_why_2",
        "type_d_why_3",
        "type_d_why_4",
        "type_d_why_5",
        "type_d_why_6",
        "type_d_why_7",
        "type_d_why_8",
        "type_d_why_9",
        "type_d_why_10",
        "type_d_why_11",
        "type_d_why_12",
        "type_d_why_13",
        "type_d_why_14",
        "type_d_why_15",
        "type_d_why_16",
        "type_c_how_1",
        "type_c_how_2",
        "type_c_how_3",
        "type_c_how_4",
        "type_c_how_5",
        "type_c_how_6",
        "type_c_how_7",
        "type_c_how_8",
        "type_c_how_9",
        "type_c_how_10",
        "type_c_how_11",
        "type_c_how_12",
        "type_c_how_13",
        "type_c_how_14",
        "type_c_how_15",
    ],
    "not_reason": [
        "type_d_whether_1",
        "type_d_whether_2",
        "type_d_whether_3",
        "type_d_whether_4",
        "type_d_whether_5",
        "type_d_whether_6",
        "type_d_whether_7",
        "type_d_whether_8",
        "type_d_whether_9",
        "type_d_whether_10",
        "type_d_whether_11",
        "type_d_whether_12",
        "type_d_whether_13",
        "type_d_whether_14",
        "type_d_whether_15",
        "type_d_whether_16",
        "type_a_what_1",
        "type_a_what_2",
        "type_a_what_3",
        "type_a_what_4",
        "type_a_what_5",
        "type_a_what_6",
        "type_a_what_7",
        "type_a_what_8",
        "type_a_what_9",
        "type_a_what_10",
        "type_a_what_11",
        "type_a_what_12",
        "type_a_what_13",
        "type_a_what_14",
        "type_a_what_15",
        "type_a_what_16",
        "type_a_what_17",
        "type_a_what_18",
        "type_a_what_19",
        "type_a_what_20",
    ],
}


def load_answer_ground_truth(
    script_id: int, model_name: str, information_type="level1"
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
    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    answers = json.load(open(path, encoding="UTF-8"))

    # load the ground truth

    path = f"synthesize_data/script/data/trial{script_id}/question_new.json"
    truth = json.load(open(path, encoding="UTF-8"))

    if "questions" in truth:
        truth = truth["questions"]

    truth_ = {}
    for key, value in truth.items():
        truth_[key] = value["true answer"]

    results = {}
    for q_id, answer in truth_.items():
        if q_id in answers:
            results[q_id] = answer == answers[q_id]
        else:
            results[q_id] = False

    return answers, truth_, results


def question_analysis(script_id: int, model_name: str, information_type="level1"):
    """calcualte the accuracy of the model for different time stage

    Args:
        script_id (int): _description_
        model_name (str): _description_
        information_type (str, optional): _description_. Defaults to "level1".
    """
    time_stage = time_stage_type_mapping.keys()
    time_results = {}
    for value in time_stage:
        time_results[value] = {"count": 0, "correct": 0}

    reason_or_not_reaults = {
        "reason": {"count": 0, "correct": 0},
        "not_reason": {"count": 0, "correct": 0},
    }

    answers, truth_, _ = load_answer_ground_truth(
        script_id, model_name, information_type
    )

    for q_id, answer in truth_.items():

        if "type_d_how" in q_id:
            continue
        time_results[type_time_stage_mapping[q_id]]["count"] += 1

        if q_id in reason_or_not["reason"]:
            reason_or_not_reaults["reason"]["count"] += 1
        else:
            reason_or_not_reaults["not_reason"]["count"] += 1

        if q_id in answers:
            if answer == answers[q_id]:
                time_results[type_time_stage_mapping[q_id]]["correct"] += 1

                if q_id in reason_or_not["reason"]:
                    reason_or_not_reaults["reason"]["correct"] += 1
                else:
                    reason_or_not_reaults["not_reason"]["correct"] += 1

    # print(results)

    for key, value in time_results.items():
        value["accuracy"] = value["correct"] / value["count"]

    time_analysis = time_stage_analysis(time_results)
    _mental_type_analysis = mental_type_analysis(time_results)

    reason_or_not_reaults = reason_or_not_analysis(reason_or_not_reaults)

    _question_type_accuracy = question_type_accuracy(
        script_id, model_name, information_type
    )

    re = {
        "question_all": time_results,
        "time": time_analysis,
        "mental_type": _mental_type_analysis,
        "reason_or_not": reason_or_not_reaults,
        "influence": question_influence_analysis(
            script_id, model_name, information_type
        ),
        "question_type_accuracy": _question_type_accuracy,
    }

    # write the accuracy to the file
    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_q_a_{model_name}.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(re, f, indent=4)


def time_stage_analysis(accuracy_detail):
    """does different time stage have different accuracy

    Args:
        accuracy_detail (_type_): _description_

    Returns:
        _type_: _description_
    """
    time_analysisi = {}
    for key, value in accuracy_detail.items():
        _key = key.split(":")[1]
        if _key not in time_analysisi:
            time_analysisi[_key] = {"count": 0, "correct": 0, "accuracy": 0}
        time_analysisi[_key]["count"] += value["count"]
        time_analysisi[_key]["correct"] += value["correct"]
        time_analysisi[_key]["accuracy"] = (
            time_analysisi[_key]["correct"] / time_analysisi[_key]["count"]
        )

    return time_analysisi


def mental_type_analysis(accuracy_detail):
    """does different mental type have different accuracy

    belief, emotion, intention, action
    belief->emotion
    belief&emotion->intention
    intention->action

    Args:
        accuracy_detail (_type_): _description_

    Returns:
        _type_: _description_
    """
    type_analysisi = {}
    for key, value in accuracy_detail.items():
        _key = key.split(":")[0]
        if _key not in type_analysisi:
            type_analysisi[_key] = {"count": 0, "correct": 0, "accuracy": 0}
        type_analysisi[_key]["count"] += value["count"]
        type_analysisi[_key]["correct"] += value["correct"]
        type_analysisi[_key]["accuracy"] = (
            type_analysisi[_key]["correct"] / type_analysisi[_key]["count"]
        )

    return type_analysisi


def reason_or_not_analysis(reason_or_not_reaults):
    """does the question need reason have different accuracy with the question not need reason

    Args:
        reason_or_not_reaults (_type_): _description_

    Returns:
        _type_: _description_
    """
    reason_or_not_reaults["reason"]["accuracy"] = (
        reason_or_not_reaults["reason"]["correct"]
        / reason_or_not_reaults["reason"]["count"]
    )
    reason_or_not_reaults["not_reason"]["accuracy"] = (
        reason_or_not_reaults["not_reason"]["correct"]
        / reason_or_not_reaults["not_reason"]["count"]
    )
    return reason_or_not_reaults


def question_influence_analysis(
    script_id: int, model_name: str, information_type="level1"
):
    """does the question have preliminary question have different accuracy

    pre:{0,1}
    self:{0,1}

    if qa,qa->qc. if qa and qc both correct, then preliminary is 1; else, preliminary is 0.

    Args:
        script_id (int): _description_
        model_name (str): _description_
        information_type (str, optional): _description_. Defaults to "level1".

    Returns:
        _type_: _description_
    """
    _, _, answer_results = load_answer_ground_truth(
        script_id, model_name, information_type
    )

    influence_results = {}
    for key, value in influence_mapping.items():
        influence_results[key] = {
            "self": answer_results[key],
            "pre": [answer_results[pre_key] for pre_key in value],
        }

    analysis_influence = {
        "pre_0": {"correct": 0, "count": 0, "accuracy": 0},
        "pre_1": {"correct": 0, "count": 0, "accuracy": 0},
    }
    for key, value in influence_results.items():
        if sum(value["pre"]) < len(value["pre"]):
            analysis_influence["pre_0"]["count"] += 1
            analysis_influence["pre_0"]["correct"] += value["self"]
            analysis_influence["pre_0"]["accuracy"] = (
                analysis_influence["pre_0"]["correct"]
                / analysis_influence["pre_0"]["count"]
            )
        else:
            analysis_influence["pre_1"]["count"] += 1
            analysis_influence["pre_1"]["correct"] += value["self"]
            analysis_influence["pre_1"]["accuracy"] = (
                analysis_influence["pre_1"]["correct"]
                / analysis_influence["pre_1"]["count"]
            )

    results = {"influence": influence_results, "analysis": analysis_influence}

    return results


def question_type_accuracy(script_id: int, model_name: str, information_type="level1"):
    """calculate the accuracy of the model for the given script_id for different type of questions

    type_a, type_c, type_d
    """
    # load the answer

    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    answers = json.load(open(path, encoding="UTF-8"))

    type_a_count = 0
    type_a_error = 0
    type_c_count = 0
    type_c_error = 0
    type_d_count = 0
    type_d_error = 0

    # load the ground truth

    path = f"synthesize_data/script/data/trial{script_id}/question_new.json"
    truth = json.load(open(path, encoding="UTF-8"))

    if "questions" in truth:
        truth = truth["questions"]

    truth_ = {}
    for key, value in truth.items():
        truth_[key] = value["true answer"]
        if "type_d" in key:
            type_d_count += 1
        elif "type_c" in key:
            type_c_count += 1
        else:
            type_a_count += 1

    # load option reasons
    option_reasons = {}
    for key, value in truth.items():
        option_reasons[key] = value["option reasons"]

    # calculate the accuracy
    for q_id, answer in truth_.items():
        if q_id not in answers:
            if "type_d" in q_id:
                type_d_error += 1
            elif "type_c" in q_id:
                type_c_error += 1
            else:
                type_a_error += 1
        else:
            if answer != answers[q_id]:
                if "type_d" in q_id:
                    type_d_error += 1
                elif "type_c" in q_id:
                    type_c_error += 1
                else:
                    type_a_error += 1

    # print(type_a_count, type_a_error)
    # print(type_c_count, type_c_error)
    # print(type_d_count, type_d_error)

    type_a_accuracy = (type_a_count - type_a_error) / type_a_count
    type_c_accuracy = (type_c_count - type_c_error) / type_c_count
    type_d_accuracy = (type_d_count - type_d_error) / type_d_count
    results = {
        "type_a": type_a_accuracy,
        "type_a_count": type_a_count,
        "type_c": type_c_accuracy,
        "type_c_count": type_c_count,
        "type_d": type_d_accuracy,
        "type_d_count": type_d_count,
    }

    return results


def overall_analysis(script_ids, model, information_level):
    """overall analysis for the given script_ids

    Args:
        script_ids (_type_): _description_
        model (_type_): _description_
        information_level (_type_): _description_
    """
    question_all = {}
    time = {}
    mental_type = {}
    reason_or_not = {}
    influence = {}
    for script_id in script_ids:
        path = f"synthesize_data/script/data/trial{script_id}/{information_level}_q_a_{model}.json"
        result = json.load(open(path, encoding="UTF-8"))
        question_all_ = result["question_all"]
        time_ = result["time"]
        mental_type_ = result["mental_type"]
        reason_or_not_ = result["reason_or_not"]
        influence_ = result["influence"]["analysis"]

        for key in question_all_:
            if key not in question_all:
                question_all[key] = question_all_[key]
            else:
                question_all[key]["count"] += question_all_[key]["count"]
                question_all[key]["correct"] += question_all_[key]["correct"]

        for key in time_:
            if key not in time:
                time[key] = time_[key]
            else:
                time[key]["count"] += time_[key]["count"]
                time[key]["correct"] += time_[key]["correct"]

        for key in mental_type_:
            if key not in mental_type:
                mental_type[key] = mental_type_[key]
            else:
                mental_type[key]["count"] += mental_type_[key]["count"]
                mental_type[key]["correct"] += mental_type_[key]["correct"]
                
        for key in reason_or_not_:
            if key not in reason_or_not:
                reason_or_not[key] = reason_or_not_[key]
            else:
                reason_or_not[key]["count"] += reason_or_not_[key]["count"]
                reason_or_not[key]["correct"] += reason_or_not_[key]["correct"]
                
        for key in influence_:
            if key not in influence:
                influence[key] = influence_[key]
            else:
                influence[key]["count"] += influence_[key]["count"]
                influence[key]["correct"] += influence_[key]["correct"]

    
    
    for key,value in question_all.items():
        question_all[key]["accuracy"] = value["correct"] / value["count"]
    
    for key,value in time.items():
        time[key]["accuracy"] = value["correct"] / value["count"]
    
    for key,value in mental_type.items():
        mental_type[key]["accuracy"] = (
                    mental_type[key]["correct"] / mental_type[key]["count"]
                )
    
    for key,value in reason_or_not.items():
        reason_or_not[key]["accuracy"] = reason_or_not[key]["correct"] / reason_or_not[key]["count"]
        
    for key,value in influence.items():
            influence[key]["accuracy"] = influence[key]["correct"] / influence[key]["count"]

    results = {
        "question_all": question_all,
        "time": time,
        "mental_type": mental_type,
        "reason_or_not": reason_or_not,
        "influence": influence,
    }

    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_q_a_analysis.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    scripts = range(50, 1050)
    models = ["Qwen2-72B-Instruct"]

    for script_id in scripts:
        for model in models:
            print(script_id, model)
            question_analysis(script_id, model, "level1")

    for model in models:
        # print(model)
        overall_analysis(scripts, model, "level1")
