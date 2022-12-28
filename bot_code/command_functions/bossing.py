import os
import pandas as pd
import random

# Returns the names of bosses that have item data stored for them, with these
# being names of directories located at the base_filepath provided.
def get_supported_bosses(base_filepath=""):
    
    toReturn = []
    for p in os.listdir(base_filepath):
        to_test = base_filepath + p
        if os.path.isdir(to_test) and not p.startswith('.'):
            toReturn.append(p)
    return toReturn

# @Inputs
# - boss: Name of the boss to defeat
# - kill_count: The number of kills to simulate
# - base_filepath: Path to the item data that has been scraped (see scraping.ipynb)
# @Returns
# - list of DF rows containing information about the item dropped.
def droppedItem(boss, kill_count=1, base_filepath=""):

    if kill_count > 300:
        kill_count = 300
    if kill_count < 1:
        kill_count = 1
    
    csv_filepath=base_filepath + boss + "/lookup_data.csv"
    data = pd.read_csv(csv_filepath)
    
    # display(data)
    
    row_num = data.shape[0]
    row_idxs = range(row_num+1)
    
    drop_rates = list(data["drop_rate"])
    # Assumes sum of drop_rates <= 1
    new_drs = drop_rates + [1-sum(drop_rates)]
    
    drops = []
    chosen_indexs = random.choices(row_idxs, weights=new_drs, k=kill_count)
    for i in chosen_indexs:
        if i != row_num:
            row_chosen = data.iloc[i]
            drops.append(row_chosen)
    
    return drops