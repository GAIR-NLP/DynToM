import json
from util.token_counter import num_tokens_from_messages


def load_system_prompt(
    script_number: int,
    information_type="level1",
):
    """load system prompt"""

    # load the story
    path = f"synthesize_data/script/data/trial{script_number}/story.json"
    script = json.load(open(path, encoding="UTF-8"))

    # load the questions
    
    path = f"synthesize_data/script/data/trial{script_number}/question_new.json"
    questions = json.load(open(path, encoding="UTF-8"))

    story = script["story"]
    
    for key, value in story.items():
        value.pop("background", None)
    

    # print(story[list(story.keys())[0]].keys())
    # print(story[list(story.keys())[1]].keys())

    questions_new = {}
    if "questions" in questions:
        questions = questions["questions"]
    for key, value in questions.items():
        questions_new[key] = {
            "question": value["question"],
            "options": value["options"],
        }

    # calculate the number of tokens
    num_tokens = num_tokens_from_messages(
        [{"role": "user", "content": json.dumps(questions_new)}]
    )
   # print(f"num_tokens input: {num_tokens}")

    if information_type == "level1":
        system_prompt = (
            f"""Answer all the {len(questions_new)} questions based on the story"""
        )
    elif information_type == "level1CoT":
        system_prompt = (
            f"""Answer all the {len(questions_new)} questions based on the story, Please first think step by step, conduct analysis on the answers to the questions, and finally output the most likely answers."""
        )

    characters_information = script["characters information"]
    full_prompt = f"{system_prompt}\n{characters_information}\n{story}\n{questions_new}\n{system_prompt}"
    # print(full_prompt)
    return full_prompt, len(questions_new)


if __name__ == "__main__":
    load_system_prompt(
        28,information_type="level1"
    )
