import argilla as rg
from tqdm import tqdm
import os

client = rg.Argilla(
        api_url=None,
        api_key=None,
    )

script_id=[60,62,65,70,71,73,75,94,95,102,110,112,129,130]
for i in tqdm(script_id):
    dataset = client.datasets(name=f"ToMValley_Human_Evaluation_script{i}")
    path=f"/human_evaluation/data/script{i}/"
    if not os.path.exists(path):
        os.makedirs(path)

    dataset.to_disk(path=path)

dataset = client.datasets(name=f"ToMValley_Data_Quality_Evaluation")
path=f"/human_evaluation/data/meta/"
if not os.path.exists(path):
        os.makedirs(path)

dataset.to_disk(path=path)