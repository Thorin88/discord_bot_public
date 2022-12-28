# Should be always be run from the root directory
from scraping.item_scraping import get_items_rs3

# Scrapes data that the bot uses.

def scrape():
    
    # Data for the !kill command

    # New data can be provided in the form:
    # get_items_rs3([list of item IDs],
    #               [list the item names],
    #               [list of item drop rates],
    #               name of the boss of associate the items with (can be existing or new))

    # Kerapac items
    get_items_rs3([51096, 51812, 51770,
                51776, 51779, 51782,
                51862],
                ["Greater Concentrated blast ability codex","Scripture of Jas","Kerapac's wrist wraps",
                "Fractured Armadyl symbol", "Fractured stabilisation gem", "Staff of Armadyl's fractured shaft",
                "Kerapac's mask piece"],
                [449/259200, 449/259200, 449/259200,
                1/450, 1/450, 1/450,
                1/1500]
                ,boss="kerapac")

    # Raksha items
    get_items_rs3([51094, 51096, 51086,
                51098, 48083, 48087,
                51084,
                51102],
                ["Greater Ricochet ability codex","Greater Chain ability codex","Shadow spike",
                "Divert ability codex", "Laceration boots", "Blast diffusion boots",
                "Fleeting boots",
                "Broken shackle"],
                [1/500, 1/500, 1/500,
                1/500, 1/200, 1/200,
                1/200,
                1/1000]
                ,boss="raksha")

if __name__ == '__main__':

    scrape()