# Dockerfile is a blueprint for building images, images are templates for containers

# Best practice to keep the code in an isolated location, to allow for a simple copy
# and ensuring minimal data is copied (eg .git is not included). Can also use a docker ignore
# file placed in the build context directory. A build’s context is the set of files located
# at the PATH or URL specified as the positional argument to the build command. So in our case
# we are running all these commands, like COPY, positioned at the root directory. (eg copying
# ./bot_code/)

# BaseImage
FROM python:3.6

# Move files to container
# If only 1 file, can use ADD

# Creates this directory in the container.
WORKDIR /code

# Generate a requirements file with pip freeze > requirements.txt. But, can cause pip trouble, so best
# to use a minimal list of modules you know are needed.

# Needed for cv2
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# Copy this file over to the container
COPY ./requirements.txt /code/requirements.txt

# The cache part here is good practice, can save time when rebuilding images since takes up
# less of Docker's cache
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy over code to be in the container/build
COPY ./bot_code /code/bot_code

# Move to where we want to run the code from
WORKDIR /code/bot_code

# Forces printing to reach the terminal immediately
ENV PYTHONUNBUFFERED 1
# The command that is executed when the container is started. A list forming the command
CMD ["python", "./main.py", "--cold-start"]

### Building + Running ###

# In terminal:
# docker build -t nameOfImage directory
# So in this case:
# docker build -t kerapac-v1 .

# The directory specified refers to the directory that our first command in this file is related to

# -i and -t to allow for ctrl + C to terminate the container (via this signal reaching the code)
# docker run --name kerapac-v1-container -it kerapac-v1

# docker stop kerapac-v1-container

### Other Info ###
# - Changes to files means that the image needs to be rebuilt
# - run arguements, -i for interaction, -t for sudo terminal, -d for detached process where you
# can then access the terminal of the container via the desktop app (CSI button)
# Unresponsive docker can be helped by opening powershell and running wsl --shutdown.