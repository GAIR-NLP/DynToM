"""
generate sketch, story,question
"""

import json
import os
import random
import unicodedata

from openai import OpenAI
import openai
from tqdm import tqdm

from llm_api.model_chat import openai_api_key, openai_base_url
from synthesize_data.process_data import process_questions
from synthesize_data.generate_rule_based_question import generate
from util.logger import logger
from util import extract_profile

openai.log = "error"

SKETCH_JSON_FORMAT = """{
        "relationships among characters":{
            "main character with supporting character 1":""
            ...
        },
        "mental states analysis in every scenario":{
            "scenario 1":{
                "belief":"",
                "emotion":"",
                "intention":"",
                "action":"",
                "influence":""
            }
            ...
        },
        "analysis of mental states across scenarios":{
            "Belief":{
                "Changed":"",
                "1":"",
                "2":"",
                "3":"",
                "4":"",
                "Reasons":""
            }
            ...
        }
    }"""
STORY_JSON_FORMAT = """{[scenario number]:{[background]:[background of the dialogue],[dialogue]:[dialogue between main character and other supporting characters]}}"""
QUESTION_JSON_FORMAT = """{"question number":{"question":[content],"options":[a... b... c... d...],"true answer":[content]}}"""


def count_files():
    """count the number of dirs in the data folder

    Returns:
        _type_: _description_
    """
    path = "synthesize_data/script/data/"

    _, dirs, _ = next(os.walk(path))
    file_count = len(dirs)
    return file_count


def make_folder(script_number: int):
    """make a new folder in the data folder

    Returns:
        _type_: _description_
    """
    # count = count_files()
    os.mkdir(f"synthesize_data/script/data/trial{script_number}")
    # return count + 1


def read_script_file():
    """read the script file

    Returns:
        _type_: _description_
    """
    with open(
        "synthesize_data/script/script_example/trial.json", encoding="UTF-8"
    ) as f:
        return json.load(f)


def write_script_file(data, file_name):
    """store the script into the file

    Args:
        data (_type_): _description_
        file_name (_type_): _description_
    """
    with open(f"synthesize_data/script/data/{file_name}", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def read_profile():
    """generate single person profile

    Returns:
        _type_: _description_
    """
    surname, given_name, gender, occupation, race, education, personality = (
        extract_profile.extract_basic_profile()
    )

    template = extract_profile.load_profile_description_template()
    profile_description = template.format(
        surname=surname,
        given_name=given_name,
        gender=gender,
        occupation=occupation,
        race=race,
        education=education,
        personality=personality,
    )

    return f"{given_name} {surname}", profile_description


def construct_characters(_number_of_characters: int = 2):
    """
    generate characters profiles
    """
    numbers = [_number_of_characters]
    number = random.choice(numbers)

    main_character_name, profile = read_profile()
    result = f"""**Main Character**: {profile}.**Supporting Characters**:"""

    for _ in range(1, number):
        name, profile = read_profile()
        result += f"- **{_}**: {profile}"

    return main_character_name, result


def read_sketch_template():
    """read the sketch template"""
    with open(
        "synthesize_data/script/generate_mental_sktch.json", encoding="UTF-8"
    ) as f:
        return json.load(f)


def construct_sketch(
    _main_character: str,
    _characters_profiles: str,
    _scenario_number: int,
    _version: str = "trail4",
):
    """construct the sketch based on the template

    Args:
        main_character (str): _description_
        characters_profiles (str): _description_
        scenario_number (int): _description_
        version (str, optional): _description_. Defaults to "trail1".

    Returns:
        _type_: _description_
    """
    template = read_sketch_template()[_version]
    social_setting_type, social_setting = extract_profile.extract_social_setting()
    return (
        social_setting_type,
        social_setting,
        template.format(
            characters_information=_characters_profiles,
            scenario_number=_scenario_number,
            main_character=_main_character,
            JSON_format=SKETCH_JSON_FORMAT,
            social_setting=social_setting,
        ),
    )


def read_story_template():
    """ "
    read the story template"""
    with open(
        "synthesize_data/script/generate_story_prompt.json", encoding="UTF-8"
    ) as f:
        return json.load(f)


def construct_story(
    _main_character: str,
    _characters_profiles: str,
    _story_sketch: str,
    _version: str = "trail2",
):
    """construct the story based on the template

    Args:
        main_character (str): _description_
        characters_profiles (str): _description_
        story_sketch (str): _description_
        version (str, optional): _description_. Defaults to "trail2".

    Returns:
        _type_: _description_
    """
    template = read_story_template()[_version]
    return template.format(
        main_character=_main_character,
        characters_information=_characters_profiles,
        story_sketch=_story_sketch,
        json_format=STORY_JSON_FORMAT,
    )


def read_question_template(question_type: str):
    """read the question template

    Returns:
        _type_: _description_
    """
    with open(
        f"synthesize_data/script/generate_question_{question_type}.json",
        encoding="UTF-8",
    ) as f:
        return json.load(f)


# def read_question_hard_template():
#     with open("synthesize_data/script/generate_question_hard.json") as f:
#         return json.load(f)


def construct_question(
    _main_character: str,
    _complete_story: str,
    _character_information: str,
    _mental_states_analysis_in_every_scenario: str,
    _analysis_of_mental_states_across_scenarios: str,
    _scenario_number: int,
    _question_type: str,
    _version: str = "trial1",
):
    """construct the question based on the template

    Args:
        _main_character (str): _description_
        _complete_story (str): _description_
        _character_information (str): _description_
        _mental_states_analysis_in_every_scenario (str): _description_
        _analysis_of_mental_states_across_scenarios (str): _description_
        _scenario_number (int): _description_
        _question_type (str): _description_
        _version (str, optional): _description_. Defaults to "trial4".

    Returns:
        _type_: _description_
    """
    number_of_question = 0
    if _question_type == "type_a":
        number_of_question = _scenario_number * 4
    elif _question_type == "type_b":
        number_of_question = _scenario_number * 4
    elif _question_type == "type_c":
        number_of_question = (_scenario_number - 1) * 4
    elif _question_type == "type_d":
        number_of_question = 4

    template = read_question_template(question_type=_question_type)[_version]["content"]
    return template.format(
        main_character=_main_character,
        complete_story=_complete_story,
        character_information=_character_information,
        mental_states_analysis_in_every_scenario=_mental_states_analysis_in_every_scenario,
        analysis_of_mental_states_across_scenarios=_analysis_of_mental_states_across_scenarios,
        number_of_question=number_of_question,
        json_format=QUESTION_JSON_FORMAT,
    )


class GPT4:
    """GPT4 model"""

    def __init__(self, model_name: str = "gpt-4-turbo-2024-04-09") -> None:

        self.model = OpenAI(api_key=openai_api_key, base_url=openai_base_url)
        self.model_name = model_name

    def chat(self, text, script_number, _json=True):
        """chat with the model

        Args:
            text (_type_): _description_
            _json (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """

        completion = self.model.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text},
            ],
            model=self.model_name,
            temperature=0.0,
            response_format={"type": "json_object"},
            n=1,
            max_tokens=4096,
        )

        message = completion.choices[0].message
        print(completion.choices[0].finish_reason)
        content = unicodedata.normalize("NFKC", message.content)

        # if the requirement require the output to be json, the model will return the json format str start with ```json and end with ```, so we need to remove them
        content = content.strip("```json")
        content = content.strip("```")

        if _json:
            try:
                content = json.loads(content)
                # logger.info("chat with the model successfully")
            except json.JSONDecodeError:
                logger.error("script: %s, chat with the model failed", script_number)
                logger.error(content)

        return content


# class DouBao:
#     """DouBao model"""

#     def __init__(self, model_name: str = "ep-20240714031440-74xxv") -> None:

#         self.model = OpenAI(api_key=doubao_api_key, base_url=doubao_base_url)
#         self.model_name = model_name

#     def chat(self, text, _json=True):

#         completion = self.model.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": text},
#             ],
#             model=self.model_name,
#             temperature=0.0,
#             max_tokens=4096,
#         )

#         message = completion.choices[0].message
#         print(completion.choices[0].finish_reason)
#         content = unicodedata.normalize("NFKC", message.content)

#         # if the requirement require the output to be json, the model will return the json format str start with ```json and end with ```, so we need to remove them
#         content = content.strip("```json")
#         content = content.strip("```")

#         if _json:
#             try:
#                 content = json.loads(content)
#             except json.JSONDecodeError:
#                 print(content)

#         return content


def check_script_correct(script: dict):
    """check the script is correct or not

    if there is missing scenario in the analysis of mental states across scenarios, return False
    if the reasons in the analysis of mental states across scenarios is missing, return False

    Args:
        script (_type_): _description_

    Returns:
        _type_: _description_
    """
    for mental_state in ["Belief", "Emotion", "Intention", "Action"]:
        if len(script["analysis of mental states across scenarios"][mental_state]) != 7:
            return False
        if ";" not in script["analysis of mental states across scenarios"][mental_state]["Reasons"]:
            return False
    return True


def generate_script_story(
    _scenario_number: int, _model: GPT4, _number_of_characters: int, script_number: int
):
    """generate script and story

    Args:
        _scenario_number (int): _description_
        _model (GPT4): _description_
        _number_of_characters (int): _description_

    Returns:
        _type_: _description_
    """
    main_character_name, characters_profiles = construct_characters(
        _number_of_characters
    )
    logger.info("script: %s, generate character profiles finished", script_number)

    social_setting_type, social_setting, story_sketch_prompt = construct_sketch(
        main_character_name, characters_profiles, _scenario_number
    )
    
    story_sketch = _model.chat(story_sketch_prompt, script_number)
    # make sure the script is correct
    if not check_script_correct(story_sketch):
        logger.error("script: %s, generate story sketch failed", script_number)
        return False
    logger.info("script: %s, generate story sketch finished", script_number)

    complete_story_prompt = construct_story(
        main_character_name,
        characters_profiles,
        story_sketch,
    )
    complete_story = _model.chat(complete_story_prompt, script_number)
    logger.info("script: %s, generate complete story finished", script_number)

    make_folder(script_number=script_number)

    script = {
        "social setting": social_setting,
        "social setting type": social_setting_type,
        "main character": main_character_name,
        "scenario numbers": _scenario_number,
        "characters information": characters_profiles,
        "sketch": story_sketch,
        "story": complete_story,
    }

    meta = {
        "generate_model": _model.model_name,
    }
    write_script_file(meta, file_name=f"trial{script_number}/meta.json")

    write_script_file(script, file_name=f"trial{script_number}/story.json")
    return True


# def generate_question(
#     _script_number: int,
#     _main_character: str,
#     _scenario_number: int,
#     _model,
#     _question_type: str,
# ):
#     """generate question

#     Args:
#         _script_number (int): _description_
#         _main_character (str): _description_
#         _scenario_number (int): _description_
#         _model (_type_): _description_
#         _question_type (str): _description_
#     """
#     path = f"synthesize_data/script/data/trial{_script_number}/story.json"
#     script = json.load(open(path, encoding="UTF-8"))

#     questions_prompt = construct_question(
#         _main_character=_main_character,
#         _complete_story=script["story"],
#         _character_information=script["characters information"],
#         _mental_states_analysis_in_every_scenario=script["sketch"][
#             "mental states analysis in every scenario"
#         ],
#         _analysis_of_mental_states_across_scenarios=script["sketch"][
#             "analysis of mental states across scenarios"
#         ],
#         _scenario_number=_scenario_number,
#         _question_type=_question_type,
#     )
#     # print(questions_prompt)
#     questions = _model.chat(questions_prompt)
#     # print(questions)
#     print(f"generate questions {_question_type}")

#     script = {
#         _question_type: questions,
#     }

#     write_script_file(
#         script,
#         file_name=f"trial{_script_number}/question_{_question_type}_{_model.model_name}.json",
#     )

#     return questions


def pipeline(
    _model: GPT4,
    _script_numbers: list[int],
    _number_of_characters: list[int],
    _scenario_numbers: list[int],
):
    """generate script, story and question

    Args:
        scenario_number (int): _description_
        model (GPT4): _description_

    Returns:
        _type_: _description_
    """

    for script_number, number_of_character, scenario_number in tqdm(
        zip(_script_numbers, _number_of_characters, _scenario_numbers),
        total=len(_script_numbers),
    ):
        logger.info("-----script: %s, Experiment started-----", script_number)

        result=generate_script_story(
            scenario_number, _model, number_of_character, script_number
        )
        # make sure the script is correct
        # if the script is not correct, regenerate the script
        while not result:
            result = generate_script_story(
                scenario_number, _model, number_of_character, script_number
            )
        
        generate(script_number)
        process_questions(script_number)

        logger.info("-----script: %s, Experiment end-----", script_number)


if __name__ == "__main__":
    # model = GPT4(model_name="gpt-4o-2024-05-13")
    model = GPT4(model_name="gpt-4-turbo-2024-04-09")
    script_numbers = range(250, 550)
    number_of_characters = [2] * len(script_numbers)
    scenario_numbers = [5] * len(script_numbers)

    pipeline(model, script_numbers, number_of_characters, scenario_numbers)
