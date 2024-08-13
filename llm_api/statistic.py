import json
from os import write

from synthesize_data.process_data import answer_unmber_mapping


def find_option_set_reason(truth, q_id, answer) -> str:
    """find out why to set the option,
    what capibility does the option what to test

    Args:
        truth (_type_): _description_
        option_reasons (_type_): _description_
        q_id (_type_): _description_
        answer (_type_): _description_

    Returns:
        _type_: _description_
    """
    if answer not in answer_unmber_mapping:
        return "chosen answer not in the option"
    option_reasons = truth[q_id]["option reasons"]

    option_id = answer_unmber_mapping[answer]
    if option_id >= len(truth[q_id]["options"]):
        return "chosen answer not in the option"

    option = truth[q_id]["options"][option_id]

    for option_reason in option_reasons:
        if option_reason["option"] in option:
            return option_reason["short"]


def calculate_accuracy(
    script_id: int,
    model_name: str,
    information_type="level1",
):
    """calculate the accuracy of the model for the given script_id"""
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

    # load option reasons
    option_reasons = {}
    for key, value in truth.items():
        option_reasons[key] = value["option reasons"]

    # calculate the accuracy
    correct = 0
    error_list = []
    for q_id, answer in truth_.items():
        if q_id not in answers:
            error_list.append(
                {
                    "id": q_id,
                    "answer": "not answered",
                    "truth": truth_[q_id],
                    "wrong_reason": "not answered",
                }
            )
        else:
            if answer == answers[q_id]:
                correct += 1
            else:
                error_list.append(
                    {
                        "id": q_id,
                        "answer": answers[q_id],
                        "truth": truth_[q_id],
                        "wrong_reason": find_option_set_reason(
                            truth, q_id, answers[q_id]
                        ),
                    }
                )

    all_numbers = len(truth_)

    accuracy = correct / all_numbers
    answers["accuracy"] = accuracy
    answers["question_count"] = all_numbers
    answers["error_list"] = error_list
    answers["error_analysis"] = error_analysis(error_list)

    # write the accuracy to the file

    path = f"synthesize_data/script/data/trial{script_id}/{information_type}_answer_{model_name}.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(answers, f, indent=4)


def error_analysis(error_list):
    """count the error reasons for all question wrong answered

    Args:
        error_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    error_map = {}
    error_count = 0
    for error in error_list:
        error_reason = error["wrong_reason"]

        if error_reason not in error_map:
            error_map[error_reason] = 1
        else:
            error_map[error_reason] += 1

    for key, value in error_map.items():
        error_count += value

    error_map["total"] = error_count

    return error_map


def overal_analysis(script_ids, model, information_level):
    """calculate the overall accuracy for the given scripts

    Args:
        script_ids (_type_): _description_
        model (_type_): _description_
        information_level (_type_): _description_
    """
    accuracy_list = []
    count_list = []
    error_map = {}
    error_count = 0
    for script_id in script_ids:
        path = f"synthesize_data/script/data/trial{script_id}/{information_level}_answer_{model}.json"
        answers = json.load(open(path, encoding="UTF-8"))
        accuracy_list.append(answers["accuracy"])
        count_list.append(answers["question_count"])

        errors = answers["error_analysis"]
        for error in errors:
            if error not in error_map:
                error_map[error] = 0
            error_map[error] += errors[error]

        error_count += errors["total"]

    accuracy_all = 0

    for count, accuracy in zip(count_list, accuracy_list):
        accuracy_all += count * accuracy
    accuracy_all = accuracy_all / sum(count_list)

    for key, value in error_map.items():
        error_map[key] = {"count": value, "percentage": value / error_count}

    results = {
        "accuracy": accuracy_all,
        "error_map": error_map,
        "error_count": error_count,
        "count_all": sum(count_list),
    }

    path = f"synthesize_data/script/data/all_scripts_analysis/{model}_{information_level}_accuracy_error.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    # scrip_ids = range(51, 57)
    # level = "level1"
    # model = "gpt-4-turbo-2024-04-09"
    # for script_id in scrip_ids:
    #     calculate_accuracy(script_id, model, level)

    scrip_ids = range(50, 57)
    level = "level1"
    model = "gpt-4-turbo-2024-04-09"
    overal_analysis(scrip_ids, model, level)

    # scrip_ids = range(38, 49)
    # for script_id in scrip_ids:
    #     # model_name = "gpt-3.5-turbo-0125"
    #     model_name = "gpt-4-turbo-2024-04-09"
    #     information_level = "level1"
    #     calculate_type_accuracy(script_id, model_name, information_level)

    # scrip_ids = range(38, 49)
    # level = "level1"
    # model = "gpt-4-turbo-2024-04-09"
    # type_accuracy = overal_type_analysis(scrip_ids, model, level)
    # print(type_accuracy)

    # scrip_ids = range(50, 51)
    # level = "level1"
    # model = "gpt-4-turbo-2024-04-09"
    # for script_id in scrip_ids:
    #     question_analysis(script_id, model, level)
    pass
