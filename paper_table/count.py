import json

def count_removed_story():
    """count the number of removed stories in the experiment.log file
    """
    path="util/logging/experiment.log"
    with open(path) as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            if "ERROR" in line:
                count += 1
    
    print(count)


def count_length_questions():
    """count the number of questions in the questions.csv file
    """
    length=0
    for id in range(50,1150):
        path=f"synthesize_data/script/data/trial{id}/question.json"
    
        with open(path) as f:
            dicts=json.load(f)
            for key,value in dicts.items():
                question=value["question"]
                options=" ".join(value["options"])
                length+=len(question.split(" "))
                length+=len(options.split(" "))
            
            
        
    print(length/(1100*71))
    
def count_length_story():
    """count the length of story
    """
    length=0
    for id in range(50,1150):
        path=f"synthesize_data/script/data/trial{id}/story.json"
    
        with open(path) as f:
            dicts=json.load(f)
            story=json.dumps(dicts["story"])
            length+=len(story.split(" "))
            
            
        
    print(length/(1100))
    
if __name__ == "__main__":
    count_length_story()