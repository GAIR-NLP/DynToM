import os
import json


def test():
    folder="data/script/data"
    subfolders= os.listdir(folder)
    subfolders=[os.path.join(folder,subfolder) for subfolder in subfolders]
    
    fulls={}
    
    for subfolder in subfolders:
        story=os.path.join(subfolder,"story.json")
        with open(story,"r") as f:
             story=json.load(f)
        question=os.path.join(subfolder,"question_new.json")
        with open(question,"r") as f:
            question=json.load(f)
        fulls[subfolder.split('/')[-1]]={
            "stage":story,
            "question":question
        }
    
    with open("./test.json",'w') as f:
        json.dump(fulls,f,indent=4)
        
if __name__=="__main__":
    test()