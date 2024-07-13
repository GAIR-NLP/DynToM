import json
import csv
import random

root_path = "/home/xiaoyang/projects/ToMValley"
race_list = [
    "American Indian",
    "Alaska Native",
    "Asian",
    "Native Hawaiian and Other Pacific Islander",
    "Black",
    "African American",
    "Hispanic",
    "Latino",
    "White",
]

social_setting_types = [
    "Transportation and Travel",
    "Accommodation and Residential",
    "Food and Beverage",
    "Shopping and Retail",
    "Entertainment and Leisure",
    "Education",
    "Health and Wellness",
    "Work and Office",
    "Military and Law Enforcement",
    "Places of Worship and Ceremony",
    "Nature and Outdoors",
    "Sport and Fitness",
    "Miscellaneous",
]


def load_profile_description_template(version="v1") -> str:
    """load the profile description template

    Args:
        version (v1): template version

    Returns:
        str: the template string
    """
    path = f"{root_path}/synthesize_data/prompt_template/character_template.json"
    with open(path) as f:
        d = json.load(f)

    return d[version]


def randm_element(elements: list) -> str:
    """return a random element from the given list

    Args:
        elements (list): the list of elements

    Returns:
        str: chosen random element
    """
    return random.choice(elements)


def read_given_name(gender: str) -> list[str]:
    """_summary_

    Args:
        gender (str): gender, man or woman

    Returns:
        list[str]: list of name of the chosen gender
    """
    path = f"{root_path}/synthesize_data/profile_data/100_given_name.csv"
    boy = []
    girl = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # print(row)
                boy.append(row[1])
                girl.append(row[2])
                line_count += 1

    # print(len(boy))
    return randm_element({"man": boy, "woman": girl}[gender])


def read_surname(race) -> list[str]:
    """_summary_

    Args:
        race (str): _description_

    Returns:
        list[str]: list of surname in the race
    """
    path = f"{root_path}/synthesize_data/profile_data/surname_list.json"
    with open(path) as f:
        d = json.load(f)

    # the keys in the dict is like: American Indian and Alaska Native
    # so we need to find the key that contains the given race
    all_keys = list(d.keys())
    for key in all_keys:
        if race in key:
            return randm_element(d[key])


def read_occupation(gender: str) -> list[str]:
    """_summary_

    Args:
        gender (str): gender: man or woman

    Returns:
        list[str]: list of occupation of the given gender
    """
    path = f"{root_path}/synthesize_data/profile_data/occupations.json"
    with open(path) as f:
        d = json.load(f)

    return randm_element(d[gender])


def read_education() -> list[str]:
    """_summary_

    Returns:
        list[str]: the education list
    """
    path = f"{root_path}/synthesize_data/profile_data/education.json"
    with open(path) as f:
        d = json.load(f)

    return randm_element(d["eductaion"])


def read_social_setting() -> list[str]:
    """_summary_

    Args:


    Returns:
        list[str]: the social setting list based on the setting type
    """
    path = f"{root_path}/synthesize_data/profile_data/social_setting.json"
    with open(path) as f:
        d = json.load(f)

    setting_type = randm_element(social_setting_types)

    return randm_element(d["classfication"][setting_type])


def read_race() -> str:
    """return the random race

    Returns:
        str: chosen random race
    """
    return randm_element(race_list)


def read_gender() -> str:
    """return the random race

    Returns:
        str: chosen random gender
    """
    return randm_element(["man", "woman"])


def read_personality() -> str:
    """return the random personality

    Returns:
        str: the chosen random personality
    """
    path = f"{root_path}/synthesize_data/profile_data/mbti.json"
    with open(path) as f:
        d = json.load(f)

    return randm_element(list(d.keys()))


def extract_basic_profile():
    """return tupple of
    (surname,given_name,gender, occupation, race, education,personality,social_setting)

    Returns:
    (surname,given_name,gender, occupation,race, education,personality,social_setting)
    """
    # level 1
    gender = read_gender()

    # social_setting_type = randm_element(social_setting_types)

    # level 2
    race = read_race()

    # level 1
    surname = read_surname(race)
    given_name = read_given_name(gender)
    occupation = read_occupation(gender)

    # level 2
    education = read_education()
    personality = read_personality()

    # social_setting = read_social_setting(social_setting_type)

    return (surname, given_name, gender, occupation, race, education, personality)


if __name__ == "__main__":
    print(extract_basic_profile())
    print(extract_basic_profile())
