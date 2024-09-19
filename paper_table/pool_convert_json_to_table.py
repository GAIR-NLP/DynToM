import json
import csv

def convert_social_setting_to_table(json_file, table_file):
    """Convert social setting json file to table file

    Args:
        json_file (_type_): _description_
        table_file (_type_): _description_
    """
    with open(json_file, 'r',encoding="UTF-8") as f:
        data = json.load(f)
    with open(table_file, 'w',encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(['social setting type', 'locations'])
        for key, value in data["classfication"].items():
            for count in range(int(len(value)/6)+1):
                writer.writerow([key, ", ".join(value[count*6:count*6+6])])

def convert_surname_to_table(json_file, table_file):
    """Convert surname json file to table file

    Args:
        json_file (_type_): _description_
        table_file (_type_): _description_
    """
    with open(json_file, 'r',encoding="UTF-8") as f:
        data = json.load(f)
    with open(table_file, 'w',encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(['surname','value'])
        for key, value in data.items():
            for count in range(int(len(value)/8)+1):
                writer.writerow([key, ", ".join(value[count*8:count*8+8])])

def convert_occupa_to_table(json_file, table_file):
    """Convert occupa json file to table file

    Args:
        json_file (_type_): _description_
        table_file (_type_): _description_
    """
    with open(json_file, 'r',encoding="UTF-8") as f:
        data = json.load(f)
    with open(table_file, 'w',encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(['surname','value'])
        for key, value in data.items():
            for count in range(int(len(value)/8)+1):
                writer.writerow([key, ", ".join(value[count*8:count*8+8])])

def convert_name_to_table(json_file, table_file):
    """Convert name json file to table file

    Args:
        json_file (_type_): _description_
        table_file (_type_): _description_
    """
    boy=[]
    girl=[]
    with open(json_file, 'r',encoding="UTF-8") as f:
        data = csv.reader(f, delimiter='\t')
        count=0
        for row in data:
            if count==0:
                count+=1
                continue
            else:
                #print(row)
                boy.append(row[1])
                girl.append(row[2]) 
    with open(table_file, 'w',encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(['Gender','Name'])
        for key,value in enumerate([boy,girl]):
            for count in range(int(len(value)/8)+1): 
                writer.writerow([["man" if key == 0 else "woman"], ", ".join(value[count*8:count*8+8])])

if __name__ == '__main__':
    convert_occupa_to_table('synthesize_data/profile_data/occupations.json', 'paper_table/data/occupations.csv')