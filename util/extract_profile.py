import json
import csv
import random

root_path = "/home/xiaoyang/ToMValley"


def read_given_name():
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
    return {"man": boy, "woman": girl}


def read_surname():
    path = f"{root_path}/synthesize_data/profile_data/surname_list.json"
    with open(path) as f:
        d = json.load(f)

    return d


def read_occupation():
    path = f"{root_path}/synthesize_data/profile_data/occupations.json"
    with open(path) as f:
        d = json.load(f)

    return d


def read_education():
    path = f"{root_path}/synthesize_data/profile_data/education.json"
    with open(path) as f:
        d = json.load(f)

    return d


def read_social_setting():
    path = f"{root_path}/synthesize_data/profile_data/social_setting.json"
    with open(path) as f:
        d = json.load(f)

    return d


def extract_basic_profile(gender: str, race: str):
    """return tupple of
    (surname,given_name,gender, race, occupation, education)

    Args:
        gender (str): _description_
        race (str): _description_
    """
    given_name_dict = read_given_name()
    surname_dict = read_surname()
    occupation_dict = read_occupation()
    education_dict = read_education()
    # social_setting = read_social_setting()

    given_name_list = given_name_dict[gender]
    given_name = random.choice(given_name_list)

    full_race = ""
    for race_ in list(surname_dict.keys()):
        if race in race_:
            full_race = race_
            break
    surname = random.choice(surname_dict[full_race])

    occupation = random.choice(occupation_dict[gender])

    education = random.choice(education_dict["eductaion"])

    return (surname, given_name, gender, race, occupation, education)


if __name__ == "__main__":
    print(extract_basic_profile("woman", "Latino"))
