import json
from util.token_counter import num_tokens_from_messages


def load_system_prompt(
    question_id,
    pre_,
    script_number: int,
    information_type,
):
    """load system prompt"""

    # load the story
    path = f"synthesize_data/script/data/trial{script_number}/story.json"
    script = json.load(open(path, encoding="UTF-8"))

    # load the questions
    
    path = f"synthesize_data/script/data/trial{script_number}/question_new.json"
    questions = json.load(open(path, encoding="UTF-8"))

    story = script["story"]
    if information_type == "level1":
        # only dialogue
        for key, value in story.items():
            value.pop("background", None)
    elif information_type == "level2":
        for key, value in story.items():
            value.pop("background", None)
        story.pop("scenario 6",None)
        story.pop("scenario 5",None)
        story.pop("scenario 7",None)
        

    # print(story[list(story.keys())[0]].keys())
    # print(story[list(story.keys())[1]].keys())

    questions_new = {question_id:{
            "question": questions[question_id]["question"],
            "options": questions[question_id]["options"]}
    }

    # calculate the number of tokens
    # num_tokens = num_tokens_from_messages(
    #     [{"role": "user", "content": json.dumps(questions_new)}]
    # )
   # print(f"num_tokens input: {num_tokens}")

    system_prompt = (
        f"""based on the given information, answer the floowing question based on the story"""
    )

    characters_information = script["characters information"]
    full_prompt = f"{characters_information}\n{story}\n{system_prompt}\n{questions_new}\n"
    # print(full_prompt)
    return full_prompt, len(questions_new)


if __name__ == "__main__":
    print(load_system_prompt("type_d_how_4", "pre_", 88, "level1newpre"))
