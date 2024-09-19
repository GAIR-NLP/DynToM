import copy
import json
import random

from util.logger import logger
from synthesize_data.process_data import process_questions


def keep_options_different(options, option_reasons):
    """keep options different, remove the same options

    Args:
        options (_type_): _description_
        option_reasons (_type_): _description_

    Returns:
        _type_: _description_
    """
    depu_id = []
    for id in range(1, len(options)):
        if options[id] == options[0]:
            depu_id.append(id)

    for id in depu_id:
        options.pop(id)
        option_reasons.pop(id)

    return options, option_reasons


def turn_list_to_str(list):
    """turn list to string

    Args:
        list (_type_): _description_

    Returns:
        _type_: _description_
    """
    return " -> ".join(list)


def shuffle_generate_option(mental_states):
    """generate options

    Args:

    Returns:
    """

    _mental_states = copy.deepcopy(mental_states)

    while _mental_states == mental_states:
        random.shuffle(_mental_states)

    return turn_list_to_str(_mental_states)


def change_order_generate_option(mental_states):
    """change order of 2 places

    Args:

    Returns:
    """
    _mental_states = copy.deepcopy(mental_states)

    while _mental_states == mental_states:
        indices = random.choices(range(len(mental_states)), k=2)

        mental_states[indices[0]], mental_states[indices[1]] = (
            mental_states[indices[1]],
            mental_states[indices[0]],
        )

    return turn_list_to_str(mental_states)


def reverse_generate_option(mental_states):
    """reverse the order

    Args:

    Returns:
    """
    mental_states = copy.deepcopy(mental_states)
    mental_states.reverse()

    return turn_list_to_str(mental_states)


# def rewrite_generate_option(mental_states):
#     """rewrite one mental state

#     Args:
#         mental_states (_type_): _description_
#     """
#     pass


def replace_generate_option(mental_states, replace_mental_states):
    """replace one value from mental states a to b

    for example, replce one content from belief to emotion


    Args:
        mental_states (_type_): _description_
    """

    index = random.choice(range(len(mental_states)))
    mental_states = copy.deepcopy(mental_states)
    mental_states[index] = replace_mental_states[index]

    return turn_list_to_str(mental_states)


def remove_generate_option(mental_states):
    """
    remove one mental state
    """

    index = random.choice(range(len(mental_states)))
    mental_states = copy.deepcopy(mental_states)
    mental_states.pop(index)

    return turn_list_to_str(mental_states)


def extract_mental_states_time(script_id):
    """
    extract mental states from the script

    Args:
        script_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    path_to_script = f"synthesize_data/script/data/trial{script_id}/story.json"
    with open(path_to_script, encoding="UTF-8") as f:
        script = json.load(f)

    main_characetr = script["main character"]
    scenario_numbers = script["scenario numbers"]

    beliefs = []
    belief_reasons = {}
    emotions = []
    emotion_reasons = {}
    intentions = []
    intention_reasons = {}
    actions = []
    action_reasons = {}

    for scenario_number in range(1, scenario_numbers + 1):
        beliefs.append(
            script["sketch"]["analysis of mental states across scenarios"]["Belief"][
                f"{scenario_number}"
            ]
        )
        emotions.append(
            script["sketch"]["analysis of mental states across scenarios"]["Emotion"][
                f"{scenario_number}"
            ]
        )
        intentions.append(
            script["sketch"]["analysis of mental states across scenarios"]["Intention"][
                f"{scenario_number}"
            ]
        )
        actions.append(
            script["sketch"]["analysis of mental states across scenarios"]["Action"][
                f"{scenario_number}"
            ]
        )

    for scenario_number in range(1, scenario_numbers):
        belief_reasons[f"{scenario_number}_{scenario_number+1}"] = script["sketch"][
            "analysis of mental states across scenarios"
        ]["Belief"]["Reasons"].split(";")[scenario_number - 1]
        emotion_reasons[f"{scenario_number}_{scenario_number+1}"] = script["sketch"][
            "analysis of mental states across scenarios"
        ]["Emotion"]["Reasons"].split(";")[scenario_number - 1]
        intention_reasons[f"{scenario_number}_{scenario_number+1}"] = script["sketch"][
            "analysis of mental states across scenarios"
        ]["Intention"]["Reasons"].split(";")[scenario_number - 1]
        print(script["sketch"]["analysis of mental states across scenarios"]["Action"]["Reasons"])
        action_reasons[f"{scenario_number}_{scenario_number+1}"] = script["sketch"][
            "analysis of mental states across scenarios"
        ]["Action"]["Reasons"].split(";")[scenario_number - 1]

    for reasons in [belief_reasons, emotion_reasons, intention_reasons, action_reasons]:
        for key, value in reasons.items():
            value = value.strip(" ")
            value = value[5:]
            value = value.strip(" ")
            reasons[key] = value

    results = {
        "belief": beliefs,
        "emotion": emotions,
        "intention": intentions,
        "action": actions,
        "belief_reasons": belief_reasons,
        "emotion_reasons": emotion_reasons,
        "intention_reasons": intention_reasons,
        "action_reasons": action_reasons,
    }

    return main_characetr, scenario_numbers, results


def extract_mental_states_influence(script_id):
    """extract mental states influence from the script

    Args:
        script_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    path_to_script = f"synthesize_data/script/data/trial{script_id}/story.json"
    with open(path_to_script, encoding="UTF-8") as f:
        script = json.load(f)

    main_characetr = script["main character"]
    scenario_numbers = script["scenario numbers"]

    scenario_how = {}
    for scenario_number in range(1, scenario_numbers + 1):
        if scenario_number not in scenario_how:
            scenario_how[scenario_number] = {}
        for mental_state_change in [
            "belief->emotion",
            "belief&emotion->intention",
            "intention->action",
        ]:
            scenario_how[scenario_number][mental_state_change] = script["sketch"][
                "mental states analysis in every scenario"
            ][f"scenario {scenario_number}"]["influence"][mental_state_change]

    return main_characetr, scenario_numbers, scenario_how


def generate_type_d_how(script_id):
    """generate type d question, rule based
    how mental states change across scenarios
    from 1->2: how it change from 1 to 2

    Args:
        script_id (_type_): _description_
    """

    main_characetr, scenario_numbers, mental_states = extract_mental_states_time(
        script_id
    )

    questions = {}
    question_count = 1

    for mental_state in ["belief", "emotion", "intention", "action"]:
        mental_value = mental_states[mental_state]
        question_steam = f"How does the {mental_state} of {main_characetr} change across the {scenario_numbers} scenarios?"
        true_answer = turn_list_to_str(mental_value)
        options = [
            true_answer,
            shuffle_generate_option(mental_value),
            change_order_generate_option(mental_value),
            reverse_generate_option(mental_value),
            remove_generate_option(mental_value),
        ]
        option_reasons = [
            {
                "option": true_answer,
                "reason": "true answer",
                "explain": "true answer",
                "short": "true_answer",
            },
            {
                "option": options[1],
                "explain": "shuffle the order of belief in scenarios",
                "reason": "test ability to recognize different time stage in correct order",
                "short": "type_d_how_time_order",
            },
            {
                "option": options[2],
                "explain": "change the order of belief in scenarios",
                "reason": "test ability to recognize different time stage in correct order",
                "short": "type_d_how_time_order",
            },
            {
                "option": options[3],
                "explain": "reverse the order of belief in scenarios",
                "reason": "test ability to recognize different time stage in correct order",
                "short": "type_d_how_time_order",
            },
            {
                "option": options[4],
                "explain": "remove one belief in one time stage",
                "reason": "test ability to recognize the completeness of the mental states",
                "short": "type_d_how_recognize_time_stage_completeness",
            },
        ]

        for _mental_state in ["belief", "emotion", "intention", "action"]:
            if _mental_state != mental_state:
                options.append(
                    replace_generate_option(mental_value, mental_states[_mental_state])
                )
                option_reasons.append(
                    {
                        "option": options[-1],
                        "reason": f"test ability to recognize the relationship between {mental_state} and {_mental_state}",
                        "explain": f"{_mental_state} change reason",
                        "short": "type_d_how_recognize_belief_emotion_intention_action",
                    }
                )

        options, option_reasons = keep_options_different(options, option_reasons)

        questions[f"type_d_how_{question_count}"] = {
            "question": question_steam,
            "true answer": "a",
            "options": options,
            "question type": "type_d",
            "option reasons": option_reasons,
        }

        question_count += 1

    return questions


def generate_type_d_why(script_id):
    """generate type d question, rule based
    why mental states change across scenarios
    from 1->2: why it change from 1 to 2

    Args:
        script_id (_type_): _description_
    """

    main_characetr, scenario_numbers, mental_states = extract_mental_states_time(
        script_id
    )

    questions = {}
    question_count = 1

    for mental_key in ["belief", "emotion", "intention", "action"]:
        mental_reasons = mental_states[f"{mental_key}_reasons"]
        for scenario_number in range(1, scenario_numbers):
            question_steam = f"Why does the {mental_key} of {main_characetr} change from scenario {scenario_number} to scenario {scenario_number+1}?"
            true_answer = mental_reasons[f"{scenario_number}_{scenario_number+1}"]
            options = [true_answer]

            option_reasons = [
                {
                    "option": true_answer,
                    "reason": "true answer",
                    "explain": "true answer",
                    "short": "true_answer",
                }
            ]

            for id_, option in mental_reasons.items():
                if id_ != f"{scenario_number}_{scenario_number+1}":
                    options.append(option)
                    option_reasons.append(
                        {
                            "option": option,
                            "reason": f"test ability to recognize the reason of {mental_key} change in different time stage",
                            "explain": f"{mental_key} change reason in other time stage",
                            "short": "type_d_why_time_stage",
                        }
                    )

            for _mental_key in ["belief", "emotion", "intention", "action"]:
                if _mental_key != mental_key:
                    for id_, option in mental_states[f"{_mental_key}_reasons"].items():
                        options.append(option)
                        option_reasons.append(
                            {
                                "option": option,
                                "reason": f"test ability to recognize the reason between {mental_key} and {_mental_key}",
                                "explain": f"{_mental_key} change reason",
                                "short": "type_d_why_recognize_belief_emotion_intention_action",
                            }
                        )

            options, option_reasons = keep_options_different(options, option_reasons)

            questions[f"type_d_why_{question_count}"] = {
                "question": question_steam,
                "true answer": "a",
                "options": options,
                "question type": "type_d",
                "option reasons": option_reasons,
            }
            question_count += 1

    return questions


def generate_type_d_whether(script_id):
    """generate type d question, rule based
    whether mental states change across scenarios
    from 1->2: whether it change from 1 to 2

    Args:
        script_id (_type_): _description_
    """
    main_characetr, scenario_numbers, mental_states = extract_mental_states_time(
        script_id
    )

    questions = {}
    question_count = 1

    path_to_script = f"synthesize_data/script/data/trial{script_id}/story.json"
    with open(path_to_script, encoding="UTF-8") as f:
        script = json.load(f)

    # whether mental states change across scenarios
    # belief
    for mental_key in ["belief", "emotion", "intention", "action"]:
        mental_state = mental_states[mental_key]
        for scenario_number in range(1, scenario_numbers):
            option_reasons = []
            question_steam = f"Whether the {mental_key} of {main_characetr} change from scenario {scenario_number} to scenario {scenario_number+1}? if yes, from what to what?"

            true_answer_ = script["sketch"][
                "analysis of mental states across scenarios"
            ]["Belief"]["Changed"]
            change = False
            if true_answer_ == "True" or true_answer_ == "true" or true_answer_ is True:
                change = True

            if change:
                true_answer = f"Yes, from {mental_state[scenario_number-1]} to {mental_state[scenario_number]}"
            else:
                true_answer = "No"

            options = [true_answer]
            option_reasons.append(
                {
                    "option": true_answer,
                    "reason": "true answer",
                    "explain": "true answer",
                    "short": "true_answer",
                }
            )

            if change:
                options.append("No")
                option_reasons.append(
                    {
                        "option": "No",
                        "reason": f"test ability to recognize whether the {mental_key} change in the time stage",
                        "explain": "no change",
                        "short": "type_d_whether_recognize_if_change",
                    }
                )
                for scenario_id in range(1, scenario_numbers):
                    if scenario_id != scenario_number:
                        options.append(
                            f"Yes, from {mental_state[scenario_id-1]} to {mental_state[scenario_id]}"
                        )
                        option_reasons.append(
                            {
                                "option": f"Yes, from {mental_state[scenario_id-1]} to {mental_state[scenario_id]}",
                                "reason": f"test ability to recognize how the {mental_key} change in the correct time stage",
                                "explain": f"how the {mental_key} change in other time stage",
                                "short": "type_d_whether_time_stage",
                            }
                        )
            else:
                for scenario_id in range(1, scenario_numbers):
                    options.append(
                        f"Yes, from {mental_state[scenario_id-1]} to {mental_state[scenario_id]}"
                    )
                    option_reasons.append(
                        {
                            "option": f"Yes, from {mental_state[scenario_id-1]} to {mental_state[scenario_id]}",
                            "reason": f"test ability to recognize whether the {mental_key} change in the time stage",
                            "explain": f"how the {mental_key} change in some time stage",
                            "short": "type_d_whether_recognizae_if_change",
                        }
                    )

            options, option_reasons = keep_options_different(options, option_reasons)

            questions[f"type_d_whether_{question_count}"] = {
                "question": question_steam,
                "true answer": "a",
                "options": options,
                "question type": "type_d",
                "option reasons": option_reasons,
            }
            question_count += 1

    return questions

def generate_type_c_how(script_id):
    """
    in one scenario, how mental states a influence mental states b
    """
    main_characetr, scenario_numbers, scenario_how = extract_mental_states_influence(
        script_id
    )

    questions = {}
    question_count = 1

    # how mental states a influence mental states b
    # belief -> emotion
    for start_mental, target_mental in [
        ("belief", "emotion"),
        ("belief&emotion", "intention"),
        ("intention", "action"),
    ]:
        for scenario_number in range(1, scenario_numbers + 1):
            option_reasons = []
            question_steam = f"In scenario {scenario_number}, how does the {start_mental} of {main_characetr} influence the {target_mental} of {main_characetr}?"
            true_answer = scenario_how[scenario_number][
                f"{start_mental}->{target_mental}"
            ]
            options = [true_answer]
            option_reasons.append(
                {
                    "option": true_answer,
                    "reason": "true answer",
                    "explain": "true answer",
                    "short": "true_answer",
                }
            )

            for id_, option in scenario_how[scenario_number].items():
                if id_ != f"{start_mental}->{target_mental}":
                    options.append(option)
                    option_reasons.append(
                        {
                            "option": option,
                            "reason": f"test ability to correctly recognize how the {start_mental} influence {target_mental} in the current time stage",
                            "explain": "how the other mental states influence each other in current time stage",
                            "short": "type_c_how_recognizae_influence_between_not_belief_emotion",
                        }
                    )
            for _scenario_number in range(1, scenario_numbers):
                if _scenario_number != scenario_number:
                    options.append(
                        scenario_how[_scenario_number][
                            f"{start_mental}->{target_mental}"
                        ]
                    )
                    option_reasons.append(
                        {
                            "option": scenario_how[_scenario_number][
                                f"{start_mental}->{target_mental}"
                            ],
                            "reason": f"test ability to correctly recognize how the {start_mental} influence {target_mental} in other time stage",
                            "explain": f"how the {start_mental} influence {target_mental} in other time stage",
                            "short": "type_c_how_time_stage",
                        }
                    )

            options, option_reasons = keep_options_different(options, option_reasons)

            questions[f"type_c_how_{question_count}"] = {
                "question": question_steam,
                "true answer": "a",
                "options": options,
                "question type": "type_c",
                "option reasons": option_reasons,
            }
            question_count += 1

    return questions


def generate_type_a_what(script_id):
    """
    what is the mental state of the main character in a specific scenario
    """
    main_characetr, scenario_numbers, mental_states = extract_mental_states_time(
        script_id
    )

    questions = {}
    question_count = 1

    # what is the mental state of the main character in a specific scenario
    # belief
    for mental_key in ["belief", "emotion", "intention", "action"]:
        mental_state = mental_states[mental_key]
        for scenario_number in range(1, scenario_numbers + 1):
            question_steam = f"What is the {mental_key} of {main_characetr} in scenario {scenario_number}?"
            true_answer = mental_state[scenario_number - 1]
            options = [true_answer]
            option_reasons = [
                {
                    "option": true_answer,
                    "reason": "true answer",
                    "explain": "true answer",
                    "short": "true_answer",
                }
            ]

            for _scenario_number in range(1, scenario_numbers + 1):
                if _scenario_number != scenario_number:
                    options.append(mental_state[_scenario_number - 1])
                    option_reasons.append(
                        {
                            "option": mental_state[_scenario_number - 1],
                            "reason": f"test ability to recognize the {mental_key} in correct time stage",
                            "explain": f"{mental_key} in other time stage",
                            "short": "type_a_what_time_stage",
                        }
                    )

            for _mental_key in ["belief", "emotion", "intention", "action"]:
                if _mental_key != mental_key:
                    options.append(mental_states[_mental_key][scenario_number - 1])
                    option_reasons.append(
                        {
                            "option": mental_states[_mental_key][scenario_number - 1],
                            "reason": "test ability to recognize the difference between belief, emotion, intention, and action",
                            "explain": f"{_mental_key} in the same time stage",
                            "short": "type_a_what_recognize_belief_emotion_intention_action",
                        }
                    )

            options, option_reasons = keep_options_different(options, option_reasons)

            questions[f"type_a_what_{question_count}"] = {
                "question": question_steam,
                "true answer": "a",
                "options": options,
                "question type": "type_a",
                "option reasons": option_reasons,
            }
            question_count += 1

    return questions


def generate(script_id):
    """
    generate all questions
    """
    questions = {}
    questions.update(generate_type_d_how(script_id))
    questions.update(generate_type_d_why(script_id))
    questions.update(generate_type_d_whether(script_id))
    questions.update(generate_type_c_how(script_id))
    questions.update(generate_type_a_what(script_id))

    save_questions_to_json(questions, script_id)
    logger.info("script: %s, generate questions successfully", script_id)

    return questions


def save_questions_to_json(questions, script_id):
    """
    save questions to json file
    """
    path = f"synthesize_data/script/data/trial{script_id}/question.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(questions, f, indent=4)


if __name__ == "__main__":
    scrips = range(1050, 1150)
    for script_id in scrips:
        generate(script_id)
        process_questions(script_id)

    # print(change_order_generate_option([
    #     "a","b",'c','d','e','f'
    # ]))
    # print(change_order_generate_option([
    #     "a","b",'c','d','e','f'
    # ]))
    # print(change_order_generate_option([
    #     "a","b",'c','d','e','f'
    # ]))
    # print(change_order_generate_option([
    #     "a","b",'c','d','e','f'
    # ]))
    # a = ["a", "b", "c", "d", "e", "f", "g"]

    # print(shuffle_generate_option(a))

    # a = ["a", "b", "c", "d", "e", "f", "g"]

    # print(change_order_generate_option(a))
