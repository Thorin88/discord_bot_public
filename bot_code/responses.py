import string

# This file handles non-command responses

def handles_response(message, is_private) -> str:

    # Preprocess the message in some way, eg to lower case
    p_msg = message.content.lower()

    # Now stripping punctuation
    p_msg = p_msg.translate(str.maketrans('', '', string.punctuation)) # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    print(p_msg)

    # Remember not to use capitals in the if cases, due to preprocessing
    acc_msg_greeting = ["hey","hi","heya","hello"]
    if p_msg in acc_msg_greeting:
        return "Hello, "+str(message.author)+"!"

    if p_msg.endswith("what"):
        return "ford"
    # if msg_len

    # if p_msg == "!help":
    #     return "This should be a `!help` handle..."