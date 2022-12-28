import requests
import pandas as pd

from pathlib import Path

# Couldn't find a great way to query item IDs from item names, so using manually found IDs.
# @Inputs:
# - item_id: The ID of the item to scrape
# - item_name: The name to give this item
# - base_savepath: The base location to store the item image in
# @Returns
# - The item name with spaces replaced by underscores, and the filename the image was stored at
def get_item_rs3(item_id, item_name, base_savepath):
    
    proc_item_name = item_name.replace(" ", "_")
     
    url = "https://services.runescape.com/m=itemdb_rs/obj_sprite.gif?id="+str(item_id)

    filename = base_savepath + proc_item_name + '.png'
    # Don't scrape file unnecessarily
    if Path(filename).exists():
        print(filename,"already exists, skipped.")
        return proc_item_name, filename
    
    img_data = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    
    return proc_item_name, filename

# Couldn't find a great way to query item IDs from item names, so using manually found IDs.
# @Inputs:
# - item_ids: List of IDs of the item to scrape
# - item_names: The names to give these items
# - drop_rate: List of decimal values representing the probability that an item drops
# - boss: String indicating the boss the !kill command will associate these items with
# - items_filepath: The base location to store the item images in
# @Returns
# - A summary dataframe of the data stored, also prints the filename of this dataframe
def get_items_rs3(item_ids: list, item_names: list, drop_rate: list, boss=None, items_filepath="./data/items/") -> None:
    
    assert len(item_ids) == len(item_names) and len(drop_rate) == len(item_ids), "The lists provided need to be of equal length"
    
    to_get = zip(item_ids, item_names, drop_rate)
    
    extra_filepath = ""
    if boss is not None:
        extra_filepath = boss + "/"
    base_filepath = items_filepath + extra_filepath
    # Make the directories if not present
    Path(base_filepath).mkdir(parents=True, exist_ok=True)
    
    data_collected = []
    for ID, name, dr in to_get:
        proc_name, file = get_item_rs3(ID, name, base_filepath)
        print(proc_name,"image saved to",file)
        
        data_collected.append([ID, proc_name, file, dr])
        
    df = pd.DataFrame(data_collected, columns=["id","name","filepath","drop_rate"])
    # display(df)
    csv_savepath = base_filepath + "lookup_data.csv"
    df.to_csv(csv_savepath, index=False)
    print("Summary CSV saved to",csv_savepath)
    return df