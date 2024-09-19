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
    path = f"multi_hop/data/trial{script_number}/story.json"
    script = json.load(open(path, encoding="UTF-8"))

    # load the questions
    
    path = f"synthesize_data/script/data/trial{script_number}/question_new.json"
    questions = json.load(open(path, encoding="UTF-8"))

    story = script["story"]
    if information_type == "level1_new" or information_type == "level1newpre":
        # only dialogue
        for key, value in story.items():
            value.pop("background", None)
    else:
        # all information
        pass

    # print(story[list(story.keys())[0]].keys())
    # print(story[list(story.keys())[1]].keys())

    questions_new = {question_id:{
            "question": questions[question_id]["question"],
            "options": questions[question_id]["options"]}
    }

    # calculate the number of tokens
    num_tokens = num_tokens_from_messages(
        [{"role": "user", "content": json.dumps(questions_new)}]
    )
   # print(f"num_tokens input: {num_tokens}")

    system_prompt = (
        f"""Answer the floowing question based on the story"""
    )

    characters_information = script["characters information"]
    if information_type=='level1newpre':
        full_prompt = f"{characters_information}\n{story}\n some information you probabley need:{pre_}\n{system_prompt}\n{questions_new}"
    else:
        full_prompt = f"{system_prompt}\n{characters_information}\n{story}\n{questions_new}\n{system_prompt}"
    # print(full_prompt)
    return full_prompt, len(questions_new)


if __name__ == "__main__":
    print(load_system_prompt("type_d_how_4", "pre_", 88, "level1newpre"))
