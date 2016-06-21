import re           # Regular expression operations
import pickle       # Python object serialization
from telegram import ForceReply
from miau.utils import Persistence

DATA_FILEPATH = "miau/regexs/resources/regexs.dat"
MENU, AWAIT_REGEX, AWAIT_ANSWER, AWAIT_MANAGE = range(4)
ALLOWED_USERS = ["José Miguel", "Gustavo", "Alberto", "Álvaro Manuel"]

# Persistence mechanism
persistence = Persistence.Persistence(DATA_FILEPATH)

# States are saved in a dict that maps chat_id -> state
state = dict()
# Sometimes you need to save data temporarily
context = dict()
# Data
regexs = persistence.load()

def isUserAllowed(first_name):
    return first_name in ALLOWED_USERS

def filter(message):
    text = message.text
    for pattern in regexs.keys():
        if re.search(pattern, text) is not None:
            return True
    return False

def filterInputDefineRegex(message):
    user_id =  message.from_user.id
    chat_state = state.get(user_id, MENU)
    return chat_state == AWAIT_REGEX or chat_state == AWAIT_ANSWER

def filterInputManageRegexs(message):
    user_id = message.from_user.id
    chat_state = state.get(user_id, MENU)
    return chat_state == AWAIT_MANAGE

def enteredRegex(bot, update):
    """ Receive the new regex and answer """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_state = state.get(user_id, MENU)

    # Check if we are waiting for input
    if chat_state == AWAIT_REGEX:
        state[user_id] = AWAIT_ANSWER

        # Save the user id and the answer to context
        context[user_id] = update.message.text
        bot.sendMessage(chat_id,
                        text="Please enter your answer",
                        reply_markup=ForceReply())

    elif chat_state == AWAIT_ANSWER:
        pattern = context.get(user_id, None)
        answer = update.message.text

        regexs[pattern] = answer
        persistence.save(regexs)

        del state[user_id]
        del context[user_id]

        bot.sendMessage(chat_id, text="Miauuu :)")

def deleteRegex(bot, update):
    """ Receive the id of the regex to delete """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_state = state.get(user_id, MENU)

    # Check if we are waiting for input
    if chat_state == AWAIT_MANAGE:
        data_list = context[user_id]
        regex_id = update.message.text
        try:
            regex_id = int(regex_id)
        except ValueError:
            regex_id = -1

        if regex_id >= 0 and regex_id < len(data_list):
            data_list.pop(regex_id)

            # Save regexs (we have to pass from list to dict)
            i = iter(data_list)
            data = dict(i)
            persistence.save(data)
            global regexs
            regexs = data

            bot.sendMessage(chat_id, text="Miauuu :)")
        else:
            bot.sendMessage(chat_id, text="Miauuu :(")

        del state[user_id]
        del context[user_id]

def defineRegex(bot, update):
    """ Define a new regex -> answer """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_state = state.get(chat_id, MENU)

    if isUserAllowed(update.message.from_user.first_name):
        if user_state == MENU:
            state[user_id] = AWAIT_REGEX  # set the state
            bot.sendMessage(chat_id,
                            text="Please enter your regex",
                            reply_markup=ForceReply())

def manageRegexs(bot, update):
    """ Manage the regexs as a list """
    if isUserAllowed(update.message.from_user.first_name):
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        user_state = state.get(chat_id, MENU)

        if len(regexs) == 0:
            bot.sendMessage(chat_id, text="Nothing to manage :)")
            return

        data_list = list(regexs.items())
        results = ""
        for i in range(len(data_list)):
            results += str(i) + ": " + data_list[i][0] + " -> " + data_list[i][1] + "\n"

        bot.sendMessage(chat_id=update.message.chat_id, text=results)

        if user_state == MENU:
            context[user_id] = data_list
            state[user_id] = AWAIT_MANAGE  # set the state
            bot.sendMessage(chat_id,
                            text="Please select id of regex to delete it or anything else to do nothing",
                            reply_markup=ForceReply())

def regex(bot, update):
    """ Return the answers according to the matching text """
    text = update.message.text
    for pattern in regexs.keys():
        if re.search(pattern, text):
            answer = regexs[pattern]
            bot.sendMessage(update.message.chat_id, text=answer)
