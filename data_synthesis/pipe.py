# TODO: Add more relationships based on the professions

# TODO: Take workplace into account

# TODO: Use LM to generate the graph, role, relationships from zero.

# Note: There are two stage in the pipeline, stage1 generates the professions, stage2 generates the relationships. But the stage1 not works well, given that stage2 relies to stage1 (Stage1 should assgin reasonable profession to adapt the relationships). 
# Update: Add stage3 to adjust the relationships.

# TODO: Optimize the detail of the prompts

# TODO: Define the degree of "familiar" in the relationships (what is the threshold of "familiar" / having a relationship)

# Note: Maybe we don't need to generate the graph at first, gpt can do it, no matter it's step-by-step or all at once.

from openai import OpenAI
import os
from dotenv import load_dotenv
from collections import defaultdict, deque
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from icecream import ic
import random
import re


load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# gpt-4o-2024-05-13
def generate_text(prompt, temperature = 0.8, model = "gpt-4-turbo-2024-04-09"):
    success = False
    while not success:
        try:
            messages = [{"role": "user", "content": f"{prompt}"}]
            response = client.chat.completions.create(model=model,
            messages=messages,
            temperature=temperature)
            success = True
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
    return response.choices[0].message.content

WS = nx.watts_strogatz_graph(15, 4, 0.3)
# pos = nx.random_layout(WS)
pos = nx.circular_layout(WS)

edges = list(WS.edges())
print(f"number of edges: {len(edges)}")
print(f"edges:\n{edges}")
print(f"desnity of graph: {nx.density(WS)}")
print(f"degree of nodes:\n{WS.degree()}")

# nx.draw(WS, pos, with_labels=True, node_size=300, node_color='lightgray', edge_color='gray')
# plt.show()

def find_cliques(graph):
    cliques = list(nx.find_cliques(graph))
    return cliques

def find_disjoint_cliques(graph):
    cliques = find_cliques(graph)
    cliques = sorted(cliques, key=len, reverse=True) 
    selected_nodes = set()
    disjoint_cliques = []
    
    for clique in cliques:
        if not any(node in selected_nodes for node in clique):
            disjoint_cliques.append(clique)
            selected_nodes.update(clique)
    
    return disjoint_cliques

families = find_disjoint_cliques(WS)
for family in families:
    print(family)
    
lonely_nodes = [node for node in WS.nodes() if node not in set.union(*[set(family) for family in families])]

num_colors = len(families) + len(lonely_nodes)
colors = cm.rainbow(np.linspace(0, 1, num_colors))

node_colors = {}
for i, family in enumerate(families):
    for node in family:
        node_colors[node] = colors[i]

color_index = len(families)
for node in lonely_nodes:
    node_colors[node] = colors[color_index]
    color_index += 1

# nx.draw(WS, pos, with_labels=True, node_size=300, node_color=[node_colors[node] for node in WS.nodes()], edge_color='black')
# plt.show()

def assign_roles(family):
    if len(family) == 2:
        roles = ['wife', 'husband']
    elif len(family) == 3:
        roles = ['father', 'mother', 'child']
    elif len(family) == 4:
        roles = ['father', 'mother', 'child1', 'child2']
    elif len(family) == 5:
        roles = ['grandfather', 'grandmother', 'father', 'mother', 'child']

    random.shuffle(roles)
    return dict(zip(family, roles))

family_list = []

for i, family in enumerate(families):
    family_list.append(assign_roles(family))

for node in lonely_nodes:
    family_list.append({node: 'alone'})

print(family_list, 
"------------------------------------------------------------------------------------------", sep='\n')

prompt_template1 = """
{}
The graph above is a diagram of social relationships, where each point represents a person, and each person has a profession. 
###
The following are the members of each family:
{}
###
The available professions include(some professions may not be used, and you can use other professions if needed): 
{}
###
Please assign a profession to each individual, ensuring that the distribution of professions reflects a typical societal structure and can accommodate the relationships in the given graph. This task should be completed in three steps:
Step 1: Provide a plausible distribution of professions.
Step 2: Explain in detail: how you can assign professions to conform to the relationships in the given graph. 
Step 3: Assign the professions to each individual. Present the result of Step 3 in JSON format (avoid including additional information such as annotations) and enclose it in a json code block. For example:
```json
{{
    "0":"profession of 0",
    "1":"profession of 1",
    ...
}}
```
"""

# If possible, remove the Step 2 in prompt_template1

def get_professions(edges, family_list, available_professions):
    prompt = prompt_template1.format(edges, family_list, available_professions)
    print(prompt, 
    "------------------------------------------------------------------------------------------", sep='\n')
    response = generate_text(prompt)
    print(response, 
    "------------------------------------------------------------------------------------------", sep='\n')
    try:
        professions_dict = json.loads(response.split('```json')[1].split('```')[0])
        return professions_dict
    except Exception as e:
        print(f"An error occurred: {e}")
    
available_professions = ['priest', 'policeman', 'doctor', 'nurse', 'teller', 'office worker(white-collar worker)', 'factory worker(blue collar worker)', 'teacher', 'student', 'coach', 'cashier', 'lifeguard', 'cook', 'waiter/waitress']



professions_dict = get_professions(edges, family_list, available_professions)
print(professions_dict, 
    "------------------------------------------------------------------------------------------", sep='\n')
print("Step1 done")

prompt_template2 = """
{}
The graph above is a diagram of social relationships, where each point represents a person, and each person has a profession. The edges in the diagram represent relationships between people. A pair of individuals can have multiple relationships, such as being both colleagues and spouses.
###
The following are the members of each family:
{}
###
The known professions of the people are as follow:
{}
###
The possible relationships between people include (just for reference, you can use other relationships as well):
{}
###
Your task is using this diagram to build a complete social relationship graph to reflect the social relations among all the people in a small town, simulating a real social scenario:
1. Assign a string to each edge to denote the relationship between the two individuals linked by that edge. This string can signify either a single or multiple relationships.
2. The relationship must be specific, such as familial relationships detailed to parent-child, spouses.
3. If two people are connected by an edge, they must be familiar with each other directly; friends of friends or just neighbors do not count as direct relationship.
4. The relationship should be consistent with the professions, ages, and workplaces of both individuals. 
5. If two individuals cannot be assigned a reasonable relationship, please use 'None' to represent the relationship between them. But you should try to avoid this situation.
6. Assgin family relationships firstly, followed by work relationships, and finally social and other relationships.
7. Output the result in a JSON format (avoid including additional information such as annotations) and enclose it in a JSON code block. The key is the edge containing points and professions, and the value is the realistic relationship between the two point (take their profession into account). For example:
```json
{{
    \"(0-teacher,1-student)\": "teacher-student",
    \"(1-policeman,2-lifeguard)\": "friend",
    ...
}}
```
"""

possible_relationships = ['parent-child', 'spouse', 'sibling', 'colleague', 'friend', 'classmate', 'teacher-student', 'doctor-patient', 'employer-employee', 'business partners']
# ['family', 'work', 'social', 'other']
# 'landlord-tenant'

prompt = prompt_template2.format(edges, family_list, professions_dict, possible_relationships)
response = generate_text(prompt)
try:
    relationship_dict = json.loads(response.split('```json')[1].split('```')[0])
    print(relationship_dict, 
    "------------------------------------------------------------------------------------------", sep='\n')
except Exception as e:  
    print(f"An error occurred: {e}")
    
print("Step2 done")

G = nx.Graph()
cnt = 0
for edge, relationship in relationship_dict.items():
    if relationship != 'None':
        node1, node2 = map(int, re.findall(r'\d+', edge))
        G.add_edge(node1, node2, relationship=relationship)
    else:
        print(f"None relationship between {edge}")
        cnt += 1
        
edges = list(G.edges())

nx.draw(G, pos, with_labels=False, node_size=300, node_color = [node_colors[node] for node in G.nodes()], edge_color='black')
professions_dict = {int(k): v for k, v in professions_dict.items()}
nx.draw_networkx_labels(G, pos, labels=professions_dict)
edge_labels = nx.get_edge_attributes(G, 'relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()


prompt_template3 = """
{}
The graph above is a diagram of social relationships, where each point represents a person, and each person has a profession. The edges in the diagram represent relationships between people. 
###
The known professions of the people are as follow:
{}
###
The relationships between people are as follow(need to be revised):
{}
###
Your task is to adjust the social relationship graph to better reflect the professions, age and workplace of the individuals, finally acquire a complete and realistic social relationship diagram. You should at least add {} new relationships to the graph (to make the graph completed). And you can remove or modify the existing relationships if necessary.
Note:
1. The relationship must be specific, such as familial relationships detailed to parent-child, spouses.
2. If two people are connected by an edge, they must be familiar with each other directly; friends of friends or just neighbors do not count as direct relationship. 
3. Don't remove any family relationships.

Please follow the two steps to complete the task:
Step 1: Analyze the current relationships piece by piece and identify the relationships that need to be added, removed, or modified . Please consider from three perspetives: profession, workplace, and age. 

Step 2: Adjust the relationships accordingly and output the result in a JSON format (avoid including additional information such as annotations) and enclose it in a JSON code block. The key is the edge containing points and professions, and the value is the realistic relationship between the two point (take their profession into account). Don't make the relationships too complex. 
For example:
```json
{{
    \"(0-teacher,1-student)\": "teacher-student",
    \"(1-policeman,2-lifeguard)\": "friend"
    ...
}}
```
"""


# For instance, a 'colleague' or 'classmate' relationship between an adult and a student is not allowed. Two people in different workplaces or with distinct profession cannot be 'colleagues', eg. teacher and policeman cannot be colleagues. But two people in the same workplace or with similar profession can be 'colleagues' or 'acquaintances'. And two person with the similar age can be friends (if they have no other relations).


prompt = prompt_template3.format(edges, family_list, professions_dict, relationship_dict, cnt + 5)
response = generate_text(prompt)
try:
    adjusted_relationship_dict = json.loads(response.split('```json')[1].split('```')[0])
    print(adjusted_relationship_dict, 
    "------------------------------------------------------------------------------------------", sep='\n')
except Exception as e:  
    print(f"An error occurred: {e}")
   
   
G = nx.Graph() 
cnt = 0
for edge, relationship in adjusted_relationship_dict.items():
    if relationship != 'None':
        node1, node2 = map(int, re.findall(r'\d+', edge))
        G.add_edge(node1, node2, relationship=relationship)
    else:
        print(f"None relationship between {edge}")
        cnt += 1
    
nx.draw(G, pos, with_labels=False, node_size=300, node_color = [node_colors[node] for node in G.nodes()], edge_color='black')

# professions_dict = {int(k): re.sub(r'\(.*?\)', '', v) for k, v in professions_dict.items()}
professions_dict = {int(k): f"{k}:{v}" for k, v in professions_dict.items()}
nx.draw_networkx_labels(G, pos, labels=professions_dict)
edge_labels = nx.get_edge_attributes(G, 'relationship')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
    
print("Step3 done")

# python3.11 data_synthesis/pipe.py > Data/diagram/pipeline_output.txt
