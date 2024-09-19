import json
from math import e
from multi_hop.multi_hop_ import load_answer_ground_truth
from analysis.analysis_question import influence_mapping


def identify(script, model_name):

    e_results = {
        "full_correct": {
            "all": {
                "all": 0,
                "keep": 0,
            }
        },
        "local_error": {
            "all": {
                "all": 0,
                "keep": 0,
            }
        },
        "full_error": {
            "all": {
                "all": 0,
                "keep": 0,
            }
        },
        "restoration error": {
            "all": {
                "all": 0,
                "keep": 0,
            }
        },
    }

    _, _, result = load_answer_ground_truth(
        script, model_name, information_type="level1"
    )
    # print(result)

    for q_id, _ in result.items():
        if q_id not in influence_mapping:
            continue

        pre = influence_mapping[q_id]
        pre_1 = pre[0]
        pre_2 = pre[1]

        if result[q_id] == 1:
            if result[pre_1] == 1 and result[pre_2] == 1:
                e_results["full_correct"]["all"]["all"] += 1
                e_results["full_correct"][q_id] = {
                    "level1": result[q_id],
                }
            else:
                e_results["restoration error"]["all"]["all"] += 1
                e_results["restoration error"][q_id] = {
                    "level1": result[q_id],
                }
        else:
            if result[pre_1] == 1 and result[pre_2] == 1:
                e_results["local_error"]["all"]["all"] += 1
                e_results["local_error"][q_id] = {
                    "level1": result[q_id],
                }
            else:
                e_results["full_error"]["all"]["all"] += 1
                e_results["full_error"][q_id] = {
                    "level1": result[q_id],
                }

    _, _, result = load_answer_ground_truth(
        script, model_name, information_type="level1newpre"
    )
    for e_type, _ in e_results.items():
        if e_type == "all":
            continue
        for q_id, _ in e_results[e_type].items():
            if q_id == "all":
                continue
            print(result[q_id])
            e_results[e_type][q_id]["level1newpre"] = result[q_id]

    _, _, result = load_answer_ground_truth(
        script, model_name, information_type="level1new"
    )
    for e_type, _ in e_results.items():
        if e_type == "all":
            continue
        for q_id, _ in e_results[e_type].items():
            if q_id == "all":
                continue
            e_results[e_type][q_id]["level1new"] = result[q_id]

    for e_type, _ in e_results.items():
        if e_type == "all":
            continue
        for q_id, _ in e_results[e_type].items():
            if q_id == "all":
                continue
            if (
                e_results[e_type][q_id]["level1newpre"]
                == e_results[e_type][q_id]["level1new"]
            ):
                e_results[e_type]["all"]["keep"] += 1

    path = f"multi_hop/data/trial{script}/{model_name}_multi_hop.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(e_results, f)


def count(scripts, model):
    results = {
        "full_correct": {
            "all": 0,
            "keep": 0,
        },
        "local_error": {
            "all": 0,
            "keep": 0,
        },
        "full_error": {
            "all": 0,
            "keep": 0,
        },
        "restoration error": {
            "all": 0,
            "keep": 0,
        },
    }

    for script in scripts:
        path = f"multi_hop/data/trial{script}/{model}_multi_hop.json"
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)

        for e_type, _ in results.items():
            results[e_type]["all"] += data[e_type]["all"]["all"]
            results[e_type]["keep"] += data[e_type]["all"]["keep"]
    
    with open(f"multi_hop/data/all_scripts_analysis/{model}_multi_hop.json", "w", encoding="UTF-8") as f:
        json.dump(results, f)

if __name__ == "__main__":
    scrip_ids = [85,182,234,492,594,762,786,895,925,939]

    models = ["gpt-4-turbo-2024-04-09", "gpt-4o-2024-05-13"]
    for script_id in scrip_ids:
        for model in models:
            identify(script_id, model)

    for model in models:
        count(scrip_ids, model)