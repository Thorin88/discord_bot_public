
import random
import os

import pokebase as pb

# Pokemon generation can sometimes result in partially complete objects, this wrapper
# aims to detect some of these to avoid problems in higher up calls.
# @Inputs
# - pman_like: A integer pokedex ID, or string representing a Pokemon name
# @Returns:
# - A pokemon object, or None if there were issues with generation
def gen_pman_wrapper(pman_like):
    
    pman = pb.pokemon(pman_like)
    if not hasattr(pman, "types"):
        return None
    
    return pman

# @Inputs
# - max_gen: The highest Pokemon generation to pool Pokemon from 
# @Returns:
# - A random Pokemon object from the generation range specified
def generate_guess(max_gen=4):
    
    pman = gen_pman_wrapper(random.choice(range(1,gen_to_id(max_gen)+1)))
    print("The Pokemon to guess is",pman.name)
    
    return pman

# @Inputs
# - pman_id: The Pokedex ID to convert 
# @Returns:
# - The generation this Pokedex ID belongs to
def id_to_gen(pman_id):
    
    if pman_id <= 151:
        return 1
    elif pman_id <= 251:
        return 2
    elif pman_id <= 386:
        return 3
    elif pman_id <= 493:
        return 4
    elif pman_id <= 649:
        return 5
    elif pman_id <= 721:
        return 6
    elif pman_id <= 809:
        return 7
    elif pman_id <= 905:
        return 8

# @Inputs
# - gen: An integer representing a Pokemon generation  
# @Returns:
# - The highest Pokedex ID that is in this generation
def gen_to_id(gen):
    
    if gen == 1:
        return 151
    elif gen == 2:
        return 251
    elif gen == 3:
        return 386
    elif gen == 4:
        return 493
    elif gen == 5:
        return 649
    elif gen == 6:
        return 721
    elif gen == 7:
        return 809
    elif gen == 8:
        return 905
    
# @Inputs
# - t: A numerical value out of the Squirdle results attributes
# - g: A numerical value out of the Squirdle results attributes
# @Returns:
# - A string representing the comparison between the values
def compare(t, g):
    
    if g > t:
        return "lower"
    elif g < t:
        return "higher"
    return "green"

# @Inputs
# - target_pman: A Pokemon object, the Pokemon to guess
# - guessed_pman_name: A string, or Pokedex ID, that was the Pokemon guessed
# @Returns:
# - If guessed_pman_name could not be converted to a pokemon object, None.
# - If guess was correct, True
# - If guess was incorrect, a dictionary representing the hints to display
def guess_analysis(target_pman, guessed_pman_name):
    
    if guessed_pman_name.isdigit():
        guessed_pman_name = int(guessed_pman_name)

    guessed_pman = gen_pman_wrapper(guessed_pman_name)
    if guessed_pman is None:
        return None
    
    if guessed_pman.name == target_pman.name:
        return True
    
    target_types = list(map(lambda t: t.type, target_pman.types))
    guessed_types = list(map(lambda t: t.type, guessed_pman.types))
    
    if len(target_types) < 2:
        target_types.append(pb.type_("none"))
    if len(guessed_types) < 2:
        guessed_types.append(pb.type_("none"))
    
    type_result = ["", ""]
    
    for i, t_type_obj in enumerate(target_types):
        for j, g_type_obj in enumerate(guessed_types):
            
            t_type = t_type_obj.name
            g_type = g_type_obj.name
            
            if i == j and t_type == g_type:
                type_result[j] = "green"
            elif i != j and t_type == g_type:
                type_result[j] = "yellow"
            elif type_result[j] != "green" and type_result[j] != "yellow": # Don't override yellows
                type_result[j] = "red"
    
    target_gen, target_height, target_weight = id_to_gen(target_pman.id), target_pman.height, target_pman.weight
    guessed_gen, guessed_height, guessed_weight = id_to_gen(guessed_pman.id), guessed_pman.height, guessed_pman.weight
    
    results = {}
    results["gen"] = compare(target_gen, guessed_gen)
    results["type1"] = type_result[0]
    results["type2"] = type_result[1]
    results["height"] = compare(target_height, guessed_height)
    results["weight"] = compare(target_weight, guessed_weight)
    
    return results

# Functions to generate the results image

import cv2
import matplotlib.pyplot as plt
import numpy as np

# @Inputs
# - response: A attribute from the results returned from guess_analysis()
# - squirdle_base_filepath: The base location for the squirdle data store
# @Returns:
# - The image representing this response
def get_squirdle_image(response, squirdle_base_filepath):

    im_path = squirdle_base_filepath + response + ".png"
    im = cv2.imread(im_path, cv2.IMREAD_COLOR)

    return im

# @Inputs
# - im: The image to place text on
# - text: The text to place on the image
# - position: The position to place the text
# @Returns:
# - The image with the text placed on it
def add_text(im, text, position):

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = position
    fontScale              = 0.5
    fontColor              = (255,255,255)
    thickness              = 1
    lineType               = 2
    
    im = cv2.putText(im,text,
                              bottomLeftCornerOfText, 
                              font, 
                              fontScale,
                              fontColor,
                              thickness,
                              lineType)
    
    return im
    
# @Inputs
# - results: The results returned from guess_analysis()
# @Returns:
# - A filepath to an image that has been generated to represent the hints provided
def generate_squirdle_image(results):
    
    # Needed instead of just results due to results being different data types
    if results == True:
        results = {'gen': 'green', 'type1': 'green', 'type2': 'green', 'height': 'green', 'weight': 'green'}

    squirdle_base_filepath = "./data/squirdle/"
    
    collected_ims = []
    for k, r in results.items():
        
        im = get_squirdle_image(r, squirdle_base_filepath)
        blank_im = np.zeros((im.shape[0], im.shape[1]//3, 3), dtype=im.dtype)
        
        collected_ims.append(blank_im)
        collected_ims.append(im)
    
    collected_ims.append(blank_im)
    
    # Adding padding between images
    combined_im = np.concatenate(tuple(collected_ims),axis=1)
    # Padding top and bottom of image
    blank_im = np.zeros((combined_im.shape[0]//2, combined_im.shape[1], 3), dtype=combined_im.dtype)
    combined_im = np.concatenate((blank_im,combined_im,blank_im),axis=0)
    
    # Convert to RGB for imshow() to display
    # combined_im = cv2.cvtColor(combined_im, cv2.COLOR_BGR2RGB)
    
    combined_im_path = squirdle_base_filepath + "results.png"
    
    for k, pos in zip(results.keys(),[(38,20),(116,20),(200,20),(288,20),(372,20)]):
        if "type" in k:
            k = k[:4] + " " + k[4:]
        combined_im = add_text(combined_im, k.capitalize(), pos)

    cv2.imwrite(squirdle_base_filepath + "results.png", combined_im)
    
    return combined_im_path