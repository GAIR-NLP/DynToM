import json
from util import extract_profile
import random
import unicodedata
from openai import OpenAI
from llm_api.model_chat import openai_api_key, openai_base_url
from util.token_counter import num_tokens_from_messages
import os

sketch_json_format = """{
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
story_json_format = """{[scenario number]:{[background]:[background of the dialogue],[dialogue]:[dialogue between main character and other supporting characters]}}"""
question_json_format = """{"question number":{"question":[content],"options":[a... b... c... d...],"true answer":[content],"explain":[content]}}"""


def count_files():
    path = "synthesize_data/script/data/"

    _, dirs, files = next(os.walk(path))
    file_count = len(dirs)
    return file_count

def make_folder():
    count = count_files()
    os.mkdir(f"synthesize_data/script/data/trial{count+1}")
    return count+1

def read_script_file():
    with open("synthesize_data/script/script_example/trial.json") as f:
        return json.load(f)


def write_script_file(data, file_name):
    with open(f"synthesize_data/script/data/{file_name}", "w") as f:
        json.dump(data, f, indent=4)


def read_profile():
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


def construct_characters():
    numbers = [3, 4]
    number = random.choice(numbers)

    main_character_name, profile = read_profile()
    result = f"""**Main Character**: {profile}.**Supporting Characters**:"""

    for _ in range(1, number):
        name, profile = read_profile()
        result += f"- **{_}**: {profile}"

    return main_character_name, result


def read_sketch_template():
    with open("synthesize_data/script/generate_mental_sktch.json") as f:
        return json.load(f)


def construct_sketch(
    main_character: str,
    characters_profiles: str,
    version: str = "trail1",
    scenario_number: int = 3,
):
    template = read_sketch_template()[version]
    return template.format(
        characters_information=characters_profiles,
        scenario_number=scenario_number,
        main_character=main_character,
        JSON_format=sketch_json_format,
    )


def read_story_template():
    with open("synthesize_data/script/generate_story_prompt.json") as f:
        return json.load(f)


def construct_story(
    characters_profiles: str,
    story_sketch: str,
    version: str = "trail2",
):
    template = read_story_template()[version]
    return template.format(
        characters_information=characters_profiles,
        story_sketch=story_sketch,
        json_format=story_json_format,
    )


def read_question_template():
    with open("synthesize_data/script/generate_question_for_story_prompt.json") as f:
        return json.load(f)


def construct_question(
    complete_story: str,
    character_information: str,
    mental_states_analysis_in_every_scenario: str,
    analysis_of_mental_states_across_scenarios: str,
    number_of_questions: int = 28,
    number_of_type1: int = 12,
    number_of_type2: int = 4,
    number_of_type3: int = 8,
    number_of_type4: int = 4,
    version: str = "trial3",
):
    template = read_question_template()[version]["content"]
    return template.format(
        complete_story=complete_story,
        character_information=character_information,
        mental_states_analysis_in_every_scenario=mental_states_analysis_in_every_scenario,
        analysis_of_mental_states_across_scenarios=analysis_of_mental_states_across_scenarios,
        number_of_questions=number_of_questions,
        number_of_type1=number_of_type1,
        number_of_type2=number_of_type2,
        number_of_type3=number_of_type3,
        number_of_type4=number_of_type4,
        json_format=question_json_format,
    )


class GPT4:
    def __init__(self,model_name:str="gpt-4-turbo-2024-04-09") -> None:

        self.model = OpenAI(api_key=openai_api_key, base_url=openai_base_url)
        self.model_name = model_name

    def chat(self, text, _json=True):

        completion = self.model.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text},
            ],
            model=self.model_name,
            temperature=0.0,
        )

        message = completion.choices[0].message
        content = unicodedata.normalize("NFKC", message.content)

        # if the requirement require the output to be json, the model will return the json format str start with ```json and end with ```, so we need to remove them
        content = content.strip("```json")
        content = content.strip("```")

        if _json:
            print(content)
            content = json.loads(content)

        return content


def pipeline():
    model = GPT4(model_name="gpt-4-turbo-2024-04-09")

    main_character_name, characters_profiles = construct_characters()
    print(characters_profiles)

    story_sketch_prompt = construct_sketch(main_character_name, characters_profiles)
    print(story_sketch_prompt)
    story_sketch = model.chat(story_sketch_prompt)
    print(story_sketch)

    complete_story_prompt = construct_story(characters_profiles, story_sketch)
    print(complete_story_prompt)
    complete_story = model.chat(complete_story_prompt)
    print(complete_story)
    
    count=make_folder()
    
    script = {
        "characters information": characters_profiles,
        "sketch": story_sketch,
        "story": complete_story,
    }
    write_script_file(script, file_name=f"trial{count}/story.json")
    
    model = GPT4("gpt-4o-2024-05-13")
    
    questions_prompt = construct_question(
        complete_story=complete_story,
        character_information=characters_profiles,
        mental_states_analysis_in_every_scenario=story_sketch[
            "mental states analysis in every scenario"
        ],
        analysis_of_mental_states_across_scenarios=story_sketch[
            "analysis of mental states across scenarios"
        ],
    )
    print(questions_prompt)
    questions = model.chat(questions_prompt)
    print(questions)
    
    script = {
        "questions": questions,
    }

    write_script_file(script, file_name=f"trial{count}/question.json")
    
def pipeline_only_question(script_number:int):
    path=f"synthesize_data/script/data/trial{script_number}/story.json"
    script=json.load(open(path))
    
    model = GPT4("gpt-4o-2024-05-13")
    
    questions_prompt = construct_question(
        complete_story=script["story"],
        character_information=script["characters information"],
        mental_states_analysis_in_every_scenario=script["sketch"][
            "mental states analysis in every scenario"
        ],
        analysis_of_mental_states_across_scenarios=script["sketch"][
            "analysis of mental states across scenarios"
        ],
    )
    print(questions_prompt)
    questions = model.chat(questions_prompt)
    print(questions)
    
    script = {
        "questions": questions,
    }

    write_script_file(script, file_name=f"trial{script_number}/question.json")
    

if __name__ == "__main__":

    # characters_profiles = "**Main Character**: Susan Marquez, woman, is a Event Planner whose race is Hispanic. Susan Marquez obtained a doctorate degree, and has a intj personality..**Supporting Characters**:- **1**: Beverly Castaneda, woman, is a Interior Designer whose race is Latino. Beverly Castaneda obtained a bachelor’s degree, and has a entp personality.- **2**: Kathryn Huber, woman, is a Human Resources Manager whose race is White. Kathryn Huber obtained a doctorate degree, and has a intj personality.- **3**: Lawrence Pierrelouis, man, is a Chef whose race is Black. Lawrence Pierrelouis obtained a Primary Education, and has a estj personality.- **4**: Maria Dominguez, woman, is a Physical Therapist whose race is Hispanic. Maria Dominguez obtained a high school, and has a istj personality."
    # story = json.dumps({
    #         "scenario_1": {
    #             "background": "Susan Marquez, an event planner, believes that Beverly Castaneda's innovative interior designs will enhance the upcoming event she is planning. Feeling excited about the potential collaboration, Susan schedules a meeting with Beverly to propose a new event concept that incorporates Beverly's design expertise.",
    #             "dialogue": [
    #                 {
    #                     "Susan": "Hi Beverly, thanks for meeting with me. I've got an exciting new event concept that I think your design skills could really bring to life."
    #                 },
    #                 {
    #                     "Beverly": "Hi Susan! I'm always up for a new project. What do you have in mind?"
    #                 },
    #                 {
    #                     "Susan": "I'm planning a corporate gala and I think we could create a unique experience by integrating your innovative designs. What do you think about transforming the venue with a modern, interactive theme?"
    #                 },
    #                 {
    #                     "Beverly": "That sounds fantastic! I love the idea of making the space interactive. We could use some cutting-edge lighting and decor to really make it pop."
    #                 },
    #                 {
    #                     "Susan": "Exactly! I knew you'd have great ideas. Let's sketch out some plans and see how we can make this happen."
    #                 },
    #                 {
    #                     "Beverly": "I'm on board. Let's get to work!"
    #                 }
    #             ]
    #         },
    #         "scenario_2": {
    #             "background": "Susan Marquez values Kathryn Huber's feedback and believes it will be crucial for the success of the corporate gala she is planning. Feeling anxious about Kathryn's reaction to the new concept, Susan arranges a meeting to present the idea and gather feedback before finalizing the event plan.",
    #             "dialogue": [
    #                 {
    #                     "Susan": "Hi Kathryn, thank you for taking the time to meet with me. I wanted to get your feedback on the new concept for the corporate gala."
    #                 },
    #                 {
    #                     "Kathryn": "Hello Susan. I'm glad you reached out. I'm excited to hear about the new concept. What do you have?"
    #                 },
    #                 {
    #                     "Susan": "We're thinking of an interactive, modern theme with innovative design elements. Beverly has some fantastic ideas for transforming the venue."
    #                 },
    #                 {
    #                     "Kathryn": "That sounds intriguing. What kind of interactive elements are you considering?"
    #                 },
    #                 {
    #                     "Susan": "We're looking at advanced lighting setups and engaging decor that will encourage guests to interact with the environment. We want to create a memorable experience."
    #                 },
    #                 {
    #                     "Kathryn": "I like the direction you're heading. My main concern would be ensuring that the interactive elements align with our corporate values and goals. Have you thought about that?"
    #                 },
    #                 {
    #                     "Susan": "Absolutely. We plan to integrate our company's mission and branding throughout the design. Your feedback is vital to make sure we stay on track."
    #                 },
    #                 {
    #                     "Kathryn": "Great. I'll give it some thought and get back to you with detailed feedback. So far, it sounds promising."
    #                 }
    #             ]
    #         },
    #         "scenario_3": {
    #             "background": "Susan Marquez is confident in Lawrence Pierrelouis' catering skills and believes his culinary expertise is essential for the corporate gala's success. Feeling assured of Lawrence's ability, Susan meets with him to discuss and finalize the event menu.",
    #             "dialogue": [
    #                 {
    #                     "Susan": "Hi Lawrence, thanks for meeting with me. I'm excited to work with you on the gala. I know your culinary skills will be a highlight of the event."
    #                 },
    #                 {
    #                     "Lawrence": "Hey Susan! I'm looking forward to it. What are you thinking for the menu?"
    #                 },
    #                 {
    #                     "Susan": "I want to go with a sophisticated yet approachable menu. Something that appeals to a wide range of tastes but still feels special. What do you think?"
    #                 },
    #                 {
    #                     "Lawrence": "I can definitely work with that. How about we start with a selection of hors d'oeuvres that showcase fresh, seasonal ingredients?"
    #                 },
    #                 {
    #                     "Susan": "That sounds perfect. What about the main course options?"
    #                 },
    #                 {
    #                     "Lawrence": "For mains, we could do a choice of a classic beef tenderloin, a delicate fish dish, and a vegetarian option that highlights local produce."
    #                 },
    #                 {
    #                     "Susan": "I love it. And for dessert?"
    #                 },
    #                 {
    #                     "Lawrence": "We could offer a trio of mini desserts to give guests a variety of flavors to end their meal on a high note."
    #                 },
    #                 {
    #                     "Susan": "That's a fantastic idea. Let's finalize the details and make this menu unforgettable."
    #                 },
    #                 {
    #                     "Lawrence": "Absolutely. I'll get started on the prep work right away."
    #                 }
    #             ]
    #         },
    #         "scenario_4": {
    #             "background": "Susan Marquez, feeling the physical stress of her demanding job, believes that her friend Maria Dominguez's support will help her manage it better. Relieved to have someone to rely on, Susan contacts Maria to schedule regular therapy sessions.",
    #             "dialogue": [
    #                 {
    #                     "Susan": "Hi Maria, I hope you're doing well. I wanted to talk to you about scheduling some regular therapy sessions. The stress from work is really getting to me."
    #                 },
    #                 {
    #                     "Maria": "Hi Susan, I'm doing well, thanks for asking. I'm glad you reached out. I'd be happy to help you manage your stress. When are you available to start?"
    #                 },
    #                 {
    #                     "Susan": "I'm thinking we could start next week, maybe twice a week in the evenings? I really need to find a way to decompress."
    #                 },
    #                 {
    #                     "Maria": "That works for me. We can start with some relaxation techniques and physical therapy exercises to help you unwind."
    #                 },
    #                 {
    #                     "Susan": "That sounds perfect. I always feel better after our sessions. Thanks for being there for me."
    #                 },
    #                 {
    #                     "Maria": "Of course, Susan. I'm here to help. We'll get you feeling better in no time."
    #                 },
    #                 {
    #                     "Susan": "I really appreciate it. See you next week."
    #                 },
    #                 {
    #                     "Maria": "Looking forward to it. Take care until then."
    #                 }
    #             ]
    #         }
    #     }
    # )

    # mental_states_analysis_in_every_scenario=json.dumps({
    #             "scenario 1": {
    #                 "belief": "Susan believes that Beverly's innovative designs will enhance the event.",
    #                 "emotion": "Susan feels excited about the potential collaboration with Beverly.",
    #                 "intention": "Susan intends to propose a new event concept incorporating Beverly's designs.",
    #                 "action": "Susan schedules a meeting with Beverly to discuss the event concept.",
    #                 "influence": "Susan's belief in Beverly's skills influences her positive emotion and strong intention, leading her to take action."
    #             },
    #             "scenario 2": {
    #                 "belief": "Susan believes that Kathryn's feedback will be crucial for the event's success.",
    #                 "emotion": "Susan feels anxious about Kathryn's reaction to the new concept.",
    #                 "intention": "Susan intends to seek Kathryn's feedback before finalizing the event plan.",
    #                 "action": "Susan arranges a meeting with Kathryn to present the concept and gather feedback.",
    #                 "influence": "Susan's anxiety influences her intention to seek feedback, and her belief in the importance of this feedback drives her to take action."
    #             },
    #             "scenario 3": {
    #                 "belief": "Susan believes that Lawrence's catering skills are essential for the event.",
    #                 "emotion": "Susan feels confident in Lawrence's ability to deliver high-quality food.",
    #                 "intention": "Susan intends to discuss the event menu with Lawrence.",
    #                 "action": "Susan meets with Lawrence to go over the catering details.",
    #                 "influence": "Susan's confidence in Lawrence's skills boosts her intention to finalize the menu, leading to a proactive discussion."
    #             },
    #             "scenario 4": {
    #                 "belief": "Susan believes that Maria's support will help her manage event-related stress.",
    #                 "emotion": "Susan feels relieved knowing she can rely on Maria.",
    #                 "intention": "Susan intends to schedule regular therapy sessions with Maria.",
    #                 "action": "Susan contacts Maria to set up a schedule for therapy sessions.",
    #                 "influence": "Susan's belief in Maria's support alleviates her stress, positively influencing her intention and leading to concrete action."
    #             }
    #         })

    # analysis_of_mental_states_across_scenarios=json.dumps({
    #             "Belief": {
    #                 "Changed": "True",
    #                 "1": "Susan believes in Beverly's design skills.",
    #                 "2": "Susan believes in Kathryn's feedback importance.",
    #                 "3": "Susan believes in Lawrence's catering skills.",
    #                 "4": "Susan believes in Maria's support.",
    #                 "Reasons": "1→2: Feedback need; 2→3: Catering need; 3→4: Stress management need"
    #             },
    #             "Emotion": {
    #                 "Changed": "True",
    #                 "1": "Susan feels excited.",
    #                 "2": "Susan feels anxious.",
    #                 "3": "Susan feels confident.",
    #                 "4": "Susan feels relieved.",
    #                 "Reasons": "1→2: Anticipation of feedback; 2→3: Confidence in Lawrence; 3→4: Relief from stress support"
    #             },
    #             "Intention": {
    #                 "Changed": "True",
    #                 "1": "Susan intends to propose a concept.",
    #                 "2": "Susan intends to seek feedback.",
    #                 "3": "Susan intends to finalize the menu.",
    #                 "4": "Susan intends to schedule therapy.",
    #                 "Reasons": "1→2: Need for validation; 2→3: Need for finalization; 3→4: Need for stress management"
    #             }
    #         })
    # print(construct_question(
    #     complete_story=story,
    #     character_information=characters_profiles,
    #     mental_states_analysis_in_every_scenario=mental_states_analysis_in_every_scenario,
    #     analysis_of_mental_states_across_scenarios=analysis_of_mental_states_across_scenarios,
    # ))
    # generate_data()
    pipeline()
    #pipeline_only_question(6)
    #print(count_files())
