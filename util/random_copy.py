import random
import os,json
import shutil

def copy(numbers):
    copy_list=random.choices(range(50,1050), k=numbers)
    
    base_folder="synthesize_data/script/data/trial"
    
    
    for i in copy_list:
        shutil.copytree(base_folder+str(i), "multi_hop/data/trial"+str(i))
def delete_():
    for folder, subs, files in os.walk("multi_hop/data"):
        for filename in files:
            path_=os.path.join(folder, filename)
            if 'level' in path_ :
                os.remove(path_)

def process():
    for folder, subs, files in os.walk("multi_hop/data"):
        for filename in files:
            path_=os.path.join(folder, filename)
            if 'level1new' in path_:
                with open(path_, "r", encoding="UTF-8") as f:
                    data = json.load(f)
                for key, value in data.items():
                    if 'type' in key:
                        if len(data[key])>=1:
                            data[key]=data[key][0].lower()
                with open(path_, "w", encoding="UTF-8") as f:
                    json.dump(data, f, indent=4)
    
if __name__ == "__main__":
    delete_()