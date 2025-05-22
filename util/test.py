import json
import os

def test():
    folder="/Users/yangxiao/Desktop/nlp/poly project/ToM/DynToM/data/script/data"
    subfolders= os.listdir(folder)
    folders=[os.path.join(folder,subfolder) for subfolder in subfolders]
    
    for folder in folders:
        files=os.listdir(folder)
        for file in files:
            if "meta" in file:
                if os.path.exists(os.path.join(folder,file)):
                    os.remove(os.path.join(folder,file))

if __name__=="__main__":
    test()