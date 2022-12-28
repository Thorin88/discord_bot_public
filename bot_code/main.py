from bots import KerapacV1 # Our custom bot

from scraper import scrape

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run the Kerapac discord bot')
    parser.add_argument('--cold-start', action='store_true',
                        help='Whether to try and scrape required data before running the bot')
    args = parser.parse_args()

    if (args.cold_start):
        scrape()

    bot = KerapacV1("!")
    bot.run_discord_bot()