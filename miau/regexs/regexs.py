import re                                   # Regular expression operations
import pickle                               # Python object serialization
import math                                 # Mathematical functions
import random                               # Generate pseudo-random numbers
from telegram import ForceReply
from miau.regexs import RegexsPersistence
from miau.constants import constants


MENU, AWAIT_REGEX, AWAIT_ANSWER, AWAIT_MANAGE = range(4)

# States are saved in a dict that maps chat_id -> state
state = dict()
# Sometimes you need to save data temporarily
context = dict()
# Data
regexs = RegexsPersistence.RegexsPersistence()

def isUserAllowed(first_name):
    return first_name in constants.ALLOWED_USERS

def filterPattern(message):
    return regexs.getMatchingRegexs(message.text) != []

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
    error = False

    # Check if we are waiting for input
    if chat_state == AWAIT_REGEX:
        state[user_id] = AWAIT_ANSWER

        # Save the user id and the answer to context
        context[user_id] = update.message.text
        bot.sendMessage(chat_id, "Please enter your answer", reply_markup=ForceReply())

    elif chat_state == AWAIT_ANSWER:
        pattern = context.get(user_id, None)
        answer = update.message.text

        try:
            regexs.addRegex({'pattern':pattern, 'answer':answer})
        except:
            bot.sendMessage(chat_id, "Miauuu :( Error in the regex.")
            error = True

        del state[user_id]
        del context[user_id]

        if not error:
            bot.sendMessage(chat_id, "Miauuu :)")

def defineRegex(bot, update):
    """ Define a new regex -> answer """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    user_state = state.get(chat_id, MENU)

    if isUserAllowed(user_name):
        if user_state == MENU:
            state[user_id] = AWAIT_REGEX  # set the state
            bot.sendMessage(chat_id, "Please enter your regex", reply_markup=ForceReply())

def deleteRegex(bot, update):
    """ Receive the id of the regex to delete """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_state = state.get(user_id, MENU)

    # Check if we are waiting for input
    if chat_state == AWAIT_MANAGE:
        regexs_list = context[user_id]
        regex_id = update.message.text
        try:
            regex_id = int(regex_id)
        except ValueError:
            regex_id = -1

        if regex_id >= 0 and regex_id < len(regexs_list):
            regex = regexs_list[regex_id]
            regexs.deleteRegex(regex)

            bot.sendMessage(chat_id, text="Miauuu :)")
        else:
            bot.sendMessage(chat_id, text="Miauuu :(")

        del state[user_id]
        del context[user_id]

def _showRegexs(bot, chat_id, regexs):
    message = ""
    i = 0
    for regex in regexs:
        m = str(i) + ": " + regex['pattern'] + " -> " + regex['answer'] + "\n"
        if len(message) + len(m) <= constants.MAX_MESSAGE_LENGTH:
            message += m
        else:
            bot.sendMessage(chat_id, message)
            message = m
        i += 1
    bot.sendMessage(chat_id, message)

def manageRegexs(bot, update, args):
    """ Manage the regexs as a list """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_state = state.get(chat_id, MENU)
    user_name = update.message.from_user.first_name
    if isUserAllowed(user_name):
        if len(args) == 0:
            regexs_list = regexs.getRegexs()                # manage all the regexs
        else:
            expr = ' '.join(args)
            regexs_list = regexs.getMatchingRegexs(expr)    # manage filtered regexs

        if len(regexs_list) == 0:
            bot.sendMessage(chat_id, "Nothing to manage :)")
            return
        else:
            _showRegexs(bot, chat_id, regexs_list)

        if user_state == MENU:
            context[user_id] = regexs_list
            state[user_id] = AWAIT_MANAGE  # set the state
            bot.sendMessage(chat_id, "Please select id of regex to delete it or anything else to do nothing", reply_markup=ForceReply())

def regex(bot, update):
    """ Return the answers according to the matching text """
    chat_id = update.message.chat_id
    text = update.message.text
    matchings = regexs.getBestMatchingRegexs(text)
    answer = random.choice(matchings)['answer']              # if multiple matchings get a random answer
    bot.sendMessage(chat_id, answer)
