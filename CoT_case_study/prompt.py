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
    
    for key, value in story.items():
            value.pop("background", None)
    

    questions_new = {question_id:{
            "question": questions[question_id]["question"],
            "options": questions[question_id]["options"]}
    }

    if information_type=="level1CoT":
        system_prompt = (
            f"""answer the floowing question based on the story. Please first think step by step, conduct analysis on the answers to the questions, and finally output the most likely answers."""
        )
    else:
        system_prompt = (
            f"""answer the floowing question based on the story"""
        )

    characters_information = script["characters information"]
    
    full_prompt = f"{characters_information}\n{story}\n{system_prompt}\n{questions_new}\n"
    # print(full_prompt)
    return full_prompt, len(questions_new)


if __name__ == "__main__":
    pass
