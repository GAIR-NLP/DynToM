import json
import random

answer_unmber_mapping = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    't':19,
    'u':20,
    'v':21,
    'w':22,
    'x':23,
    'y':24,
    'z':25,
    
}
answer_char_mapping = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
    8: "i",
    9: "j",
    10: "k",
    11: "l",
    12: "m",
    13: "n",
    14: "o",
    15: "p",
    16: "q",
    17: "r",
    18: "s",
    19: 't',
    20: 'u',
    21: 'v',
    22: 'w',
    23: 'x',
    24: 'y',
    25: 'z',
}


def if_start_with_alphabet(strings):
    for id, string in enumerate(strings):
        if string[0:3] not in [value + ". " for value in answer_unmber_mapping.keys()]:
            strings[id] = f"{chr(97+id)}. {string}"
    return strings


def change_true_answer_position(options, true_answer):
    if isinstance(true_answer, list):
        true_answer = true_answer[0]
    true_answer_index = answer_unmber_mapping[true_answer]
    true_answer = options[true_answer_index]

    random.shuffle(options)
    true_answer_index = options.index(true_answer)

    for id, option in enumerate(options):
        if option[0:3] in [value + ". " for value in answer_unmber_mapping.keys()]:
            options[id] = option[3:]
    for id, option in enumerate(options):
        options[id] = f"{chr(97+id)}. {option}"

    return options, answer_char_mapping[true_answer_index]


def process_questions(script_id):
    # if hard:
    #     if question_model:
    #         path = f"synthesize_data/script/data/trial{script_id}/question_hard_{question_model}.json"
    #     else:
    #         path = f"synthesize_data/script/data/trial{script_id}/question_hard.json"
    # else:
    #     if question_model:
    #         path = f"synthesize_data/script/data/trial{script_id}/question_{question_model}.json"
    #     else:
    path = f"synthesize_data/script/data/trial{script_id}/question.json"
    questions = json.load(open(path, encoding="UTF-8"))

    new = {}

    for count, question in questions.items():
        print(count)
        options = question["options"]
        # print(question.keys())
        # print(key)
        # print(count)
        true_answer = question["true answer"]

        options = if_start_with_alphabet(options)
        options, true_answer = change_true_answer_position(options, true_answer)

        question["options"] = options
        question["true answer"] = true_answer
        new[count] = question

    # if hard:
    #     if question_model:
    #         path = f"synthesize_data/script/data/trial{script_id}/question_hard_new_{question_model}.json"
    #     else:
    #         path = (
    #             f"synthesize_data/script/data/trial{script_id}/question_hard_new.json"
    #         )
    # else:
    #     if question_model:
    #         path = f"synthesize_data/script/data/trial{script_id}/question_new_{question_model}.json"
    #     else:
    path = f"synthesize_data/script/data/trial{script_id}/question_new.json"
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(new, f, indent=4)


if __name__ == "__main__":
    scrip_ids = range(2, 37)
    for script_id in scrip_ids:
        process_questions(script_id)
