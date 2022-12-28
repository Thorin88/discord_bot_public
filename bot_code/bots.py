import discord
import responses # Our custom response handling function defintions

from discord.ext import commands

import numpy as np
import pandas as pd

import random
import os

# Functions used in the !kill command
from command_functions.bossing import get_supported_bosses, droppedItem
# Functions used in the !squirdle command
from command_functions.squirdle import guess_analysis, generate_guess, generate_squirdle_image

class KerapacV1(commands.Bot):

    data_base_filepath = "./data/"
    items_base_filepath = "./data/items/"

    # Squirdle
    squirdle_target_pman = None
    squirdle_attempts = 0
    gen_limit = 8

    def run_discord_bot(self):

        secret_data = {}
        with open("secrets/secrets.txt") as f:
            for line in f:
                (key, val) = line.split() # Splits on " " by default
                secret_data[key] = val

        # TODO - Load user data from data/user_data/
        # Bot will load in existing data, then update and reference the current object containing the
        # data. On shutdown, the data will be stored in the offline data file.

        # Since our class extends Bot(), we've already got the Bot() object to work with, self
        # bot = commands.Bot(command_prefix=self.command_prefix)

        # Called when the code is run, the actual call is self.event(on_ready()), so the discord API needs
        # to recognise our function name.
        @self.event
        async def on_ready(): # Called by the API when the bot starts to run
            print(str(self.user),"is running.")
            await self.status_update(str(self.user)+" is running.")
        # https://stackoverflow.com/questions/49446882/how-to-get-all-text-channels-using-discord-py

        @self.event
        async def on_message(message):

            # Check for commands first
            await self.process_commands(message)

            # Checking we aren't reading our own messages
            if message.author == self.user:
                return

            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            # Prevents this extra message handling code being run unnecessarily
            if user_message.startswith(self.command_prefix):
                # Command would already have been handled
                return

            print(username,"said","\""+user_message+"\"","in",channel)

            # Process non-command responses
            was_private = user_message.startswith("?")
            await self.send_message(message, is_private=was_private)

                                        ### Commands ###

        # Also have access to a !help

        help_str = "Repeats the parameters the user passed to the command"
        usage_str = "[ARGS]"
        # Repeats the parameters the user passed to the command
        @self.command(help=help_str, usage=usage_str)
        async def repeat(ctx, *args): # *args is a tuple, since its been packed

            await ctx.send(args)


        help_str = "Simulates defeating various Runescape 3 bosses. Currently supports the following bosses: "
        help_str += str(get_supported_bosses(base_filepath=self.items_base_filepath))

        usage_str = "boss_name number_of_kills"
        # Simulates defeating various Runescape 3 bosses 
        @self.command(help=help_str, usage=usage_str)
        async def kill(ctx, boss: str, kc: int):

            proc_boss = boss.lower()

            # Checking if boss is supported
            if proc_boss in get_supported_bosses(base_filepath=self.items_base_filepath):
                # await ctx.send("You want to defeat",boss)

                # Could possibly make this display a bit nicer, also uses raw link URLs
                # https://stackoverflow.com/questions/63100479/multiple-photos-in-discord-py-embed

                drops = droppedItem(proc_boss, kill_count=kc, base_filepath=self.items_base_filepath)
                print("Number of drops:",len(drops)) # Print this to discord too?
                for i, drop in enumerate(drops):
                    if i > 4: # Hard limit on drops displayed, to avoid spam
                        await ctx.send("You also received " + str(len(drops)-i) + " more drops, but they have not been shown")
                        break
                    file = discord.File(drop["filepath"])
                    await ctx.send(file=file, content="You got a " + drop["name"].replace("_"," ") + " drop!")

            else:
                await ctx.send("Sorry, I do not recognise that boss yet.")


        help_str = "Returns a random play on words of the word \"rizz\""
        usage_str = "None"
        # Returns a random play on words of the word "rizz"
        @self.command(help=help_str, usage=usage_str)
        async def rizz(ctx):

            filepath = self.data_base_filepath + "other/rizztionary.txt"
            if not os.path.exists(filepath):
                await ctx.send("Sorry, I don't have access to a rizztionary at the moment.")
                return
            with open(filepath, 'r') as rizztionary:
                lines = rizztionary.readlines()
                phrase = lines[random.choice(range(len(lines)))]
            await ctx.send(phrase)


        help_str = "Sends an appropriate image"
        usage_str = "None"
        # Heavily requested
        @self.command(help=help_str, usage=usage_str)
        async def grovyle(ctx):

            filepath = self.data_base_filepath + "other/gigachad.jpg"
            if not os.path.exists(filepath):
                await ctx.send("Sorry, I don't have access to a gigachad image.")
                return
            
            file = discord.File(filepath)
            await ctx.send(file=file)


        help_str = "Sends an appropriate image"
        usage_str = "None"
        # Squidgame !!
        @self.command(help=help_str, usage=usage_str)
        async def squidgame(ctx):

            filepath = self.data_base_filepath + "other/biden_squidgame.jpg"
            if not os.path.exists(filepath):
                await ctx.send("Sorry, I don't have access to a squidgame image.")
                return
            
            file = discord.File(filepath)
            await ctx.send(file=file)

        help_str = "Has Kerapac say a random line of dialogue from his Hard Mode encounter"
        usage_str = "None"
        # Has Kerapac say a random line of dialogue from his Hard Mode encounter
        @self.command(help=help_str, usage=usage_str)
        async def speak(ctx):

            filepath = self.data_base_filepath + "other/speech.txt"
            if not os.path.exists(filepath):
                await ctx.send("Sorry, I don't have access to my speech file.")
                return
            with open(filepath, 'r') as speech:
                lines = speech.readlines()
                phrase = lines[random.choice(range(len(lines)))]
            await ctx.send(phrase)


        help_str = "Allows the user to play Squirdle, a Pokemon guessing game"
        usage_str = "guess pokemon_to_guess : Guesses the Pokemon name or Pokedex ID provided\n"
        usage_str += "!squirdle new pokemon_to_guess : Starts a new game, as well as guessing\n"
        usage_str += "!squirdle genLimit max_gen : Sets the maximum generation guesses are generated from to max_gen"
        # Allows the user to play Squirdle, a Pokemon guessing game
        @self.command(help=help_str, usage=usage_str)
        async def squirdle(ctx, instruction, pokemon):

            max_attempts = 6

            supported_instructions = ["guess", "new", "genLimit"]

            if not (instruction in supported_instructions):
                await ctx.send("Sorry, I expected either `new` or `guess` before the pokemon name or PID.")
                return

            await ctx.send("This command can take a little while to run, please be patient with me.")

            if (instruction == "genLimit"):
                if not pokemon.isdigit():
                    await ctx.send("Expected a generation in the range [1,8].")
                    return
                pokemon = int(pokemon)
                if (pokemon > 8 or pokemon < 1):
                    await ctx.send("Expected a generation in the range [1,8].")
                    return
                self.gen_limit = pokemon
                await ctx.send("Generation Limit set to " + str(pokemon) + " .")
                return

            # Generate a new target Pokemon if asked, or if one does not currently exist.
            if (instruction == "new") or (self.squirdle_target_pman is None):
                self.squirdle_target_pman = generate_guess(max_gen=self.gen_limit)
                self.squirdle_attempts = 0
                await ctx.send("A new target Pokemon has been generated. Now processing your guess...")
            
            # Evaluating the guessed Pokemon
            if (instruction == "guess") or (instruction == "new"):
                results = guess_analysis(self.squirdle_target_pman, pokemon.lower())
                # Unable to find the provided Pokemon in the API data
                if results is None:
                    await ctx.send("Sorry, I did not recognise that Pokemon.")
                # The guess was correct
                elif results == True:
                    self.squirdle_target_pman = None
                    self.squirdle_attempts = 0
                    results_im_path = generate_squirdle_image(results)
                    await ctx.send(file=discord.File(results_im_path), content=pokemon + " was correct!")                   
                # The guess was a valid Pokemon, but not correct
                else:
                    self.squirdle_attempts += 1
                    results_im_path = generate_squirdle_image(results)
                    if self.squirdle_attempts >= max_attempts:
                        await ctx.send(file=discord.File(results_im_path), content = pokemon + " was incorrect! The correct anwser was " + str(self.squirdle_target_pman.name))
                        self.squirdle_target_pman = None
                        self.squirdle_attempts = 0
                    else:
                        await ctx.send(file=discord.File(results_im_path), content="\nAttempts Left: " + str(max_attempts - self.squirdle_attempts))

        # https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#parameters


        self.run(secret_data["token"])

    # Sends message to the current channel or the user, depending on value of is_private.
    # This function is called when non-command responses may be required by the bot.
    # @Inputs:
    # - message: The discord message object
    # - is_private: whether the message was private or not
    async def send_message(self, message, is_private):
        
        try:
            bot_response = responses.handles_response(message, is_private)

            if bot_response is None:
                return

            await message.author.send(bot_response) if is_private else await message.channel.send(bot_response)

        except Exception as e:
            print(e)

    # Makes the bot message the "bot-status" channel of all servers it is in, with the message intending
    # to be used as a status update of the bot.
    async def status_update(self, msg: str):
        text_channel_list = []
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == 'bot-status':
                    await channel.send(msg)

    # A placeholder function which cantains any clean up code that needs to be run when the bot
    # shutsdown.
    async def async_cleanup(self):
        print(self.user,"is shutting down...")
        await self.status_update(str(self.user) + " has shut down.")

    # Custom shutdown procedure, before bot.close() is called. Would allow for offline datastores to
    # be updated with new information the bot collected while running.
    async def close(self):

        await self.async_cleanup()
        print("Clean up finished.")
        # Call the offical close() function
        await super().close()
        print(self.user,"shutdown.")
        