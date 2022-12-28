# bot_code

This directory contains the the code for the bot.

## `main.py`

The driver code for the bot.

## `bots.py`

Contains the core bot code, including defining its commands.

## `command_functions/`

Contains files that define functions used by some of the bot's commands.

## `data/`

Contains data that the bot collects and/or uses.

## `scraping/`

Contains functions that have been developed to scrape data for the bots data stores.

## `scraper.py`

The driver for the code within `scraping/`. Code can be added to this file to scrape more data for the `!kill` command.

## `responses.py`

Contains code that is run when the bot needs to process non-command messages.

## `secrets/`

Contains various information that should not be visible on Github.

## `experiments.ipynb`

A notebook that has been used to prototype code which was then moved over to the main code base. Developing in the notebook was much faster than having to run the bot each time.

