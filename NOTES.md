# Notes

This file contains personal notes I made about this project, can be ignored.

Followed the following guide: https://www.youtube.com/watch?v=hoDLj0IzZMU, https://discordpy.readthedocs.io/en/stable/quickstart.html

# TODO

More flexible command handling by making use of an existing parsing API:

https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#parameters

**Scraping tools notebook could later be moved to a function that the bot can use, as part of an ETL pipeline process.**

Add colours/prices to drop messages

Check if the commands helper API has an auto command list generator

Improve error messages for malformed command usage

Limit drop displays in some way

Speed up squirdle? Dont create the whole object? Query the api specifcally instead?

Add command descriptions to show up in the help command

add some slash commands? message.content.startswith('/commandName'):

Possibly eventually moving onto a CI/CD pipeline that the bot can be updated via, like airflow.

# Bugs

Squirdle: Deoxys as a string does not work, deoxys-attack also does not work. Maybe extend validation checks in squirdle.py?

# Stuff Learnt

In the Docs links, replacing stable with the version of the `discord` module will bring up the correct documentation.

`MESSAGE CONTENT INTENT` needs to be turned on in `applications/.../bot` to be able to see message contents

Can temporarily remove a file, to allow it to be ignored, by using

`git rm --cached filename` before committing.

Python decorators: https://realpython.com/primer-on-python-decorators/. These decarators can be thought of as taking a function object as input, and then adding some functionality around the function, before calling the function at some point. The decorator is a function that accepts a function, then defining and returning a wrapper function.

@decorator
def my_func(to_wrap)

is syntactic sugar for my_func = decorator(my_func), where decorator is already defined

Discord documentation, such as how messages are formulated: https://discord.com/developers/docs/intro

Discord Python documentation, such as the properties of the objects passed to the bot's functions, and the functions available to define, like on_ready(): https://discordpy.readthedocs.io/en/stable/api.html

https://stackoverflow.com/questions/51234778/what-are-the-differences-between-bot-and-client

## Docker + Docker Best Practices

Dockerfile setup: https://www.youtube.com/watch?v=0UG2x2iWerk. Also contains a template ignore file and how to port forward an application so that it works in Docker. Right at the end contains info on running a container in the background, and how to access a container via the terminal (eg to check files are correct ect)

`pip freeze > requirements.txt` can be used to create a requirements file, if only pip has been used to install things. Eg in when a venv was used.

Keep code out of home directory, so that docker can copy it without hitting the .git files

Made a lot of notes in the Dockerfile. Closing the desktop app when running the containers is a big help in avoiding the PC becoming unresponsive.

## Github actions

https://git-scm.com/book/en/v2/Git-Basics-Tagging

https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions