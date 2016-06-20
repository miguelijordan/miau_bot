import re           # Regular expression operations
import pickle       # Python object serialization
from telegram import ForceReply

TROLLS_FILEPATH = "miau/troll/resources/trolls.dat"
TROLLS_FILEPATH2 = "miau/troll/resources/trolls2.dat"
MENU, AWAIT_REGEX, AWAIT_ANSWER, AWAIT_MANAGE = range(4)

# States are saved in a dict that maps chat_id -> state
state = dict()
# Sometimes you need to save data temporarily
context = dict()

# persistence methods
def saveTrolls(trolls):
    with open(TROLLS_FILEPATH, 'wb') as file:
        pickle.dump(trolls, file)

def loadTrolls():
    try:
        with open(TROLLS_FILEPATH, 'rb') as file:
            trolls = pickle.load(file)
        return trolls
    except EOFError:
        return {}

trolls = loadTrolls()
def troll(bot, update):
    text = update.message.text
    for pattern in trolls.keys():
        if re.search(pattern, text):
            answer = trolls[pattern]
            bot.sendMessage(chat_id=update.message.chat_id, text=answer)
            return None

def filter(message):
    text = message.text
    for pattern in trolls.keys():
        if re.search(pattern, text) is not None:
            return True
    return False

def filter_user(message):
    return  message.from_user.first_name == "José Miguel" or \
            message.from_user.first_name == "Gustavo" or \
            message.from_user.first_name == "Alberto" or \
            message.from_user.first_name == "Álvaro Manuel"

def filter_input_define_troll(message):
    user_id =   message.from_user.id
    s = state.get(user_id, MENU)
    return s == AWAIT_REGEX or s == AWAIT_ANSWER

def filter_input_manage_troll(message):
    user_id = message.from_user.id
    s = state.get(user_id, MENU)
    return s == AWAIT_MANAGE

# Example handler. Will be called on the /set command and on regular messages
def define_troll(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_state = state.get(chat_id, MENU)
    user_name = update.message.from_user.first_name

    if filter_user(update.message):
        if user_state == MENU:
            state[user_id] = AWAIT_REGEX  # set the state
            bot.sendMessage(chat_id,
                            text="Please enter your regex",
                            reply_markup=ForceReply())

def entered_input(bot, update):
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

        global trolls
        trolls[pattern] = answer
        saveTrolls(trolls)

        del state[user_id]
        del context[user_id]

        bot.sendMessage(chat_id, text="Miauuu :)")

def delete_troll(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    chat_state = state.get(user_id, MENU)

    # Check if we are waiting for input
    if chat_state == AWAIT_MANAGE:
        trolls_list = context[user_id]
        regex_id = update.message.text
        try:
            regex_id = int(regex_id)
        except ValueError:
            regex_id = -1

        if regex_id >= 0 and regex_id < len(trolls_list):
            trolls_list.pop(regex_id)

            # Save trolls (we have to pass from list to dict)
            i = iter(trolls_list)
            trolls = dict(i)
            saveTrolls(trolls)

            bot.sendMessage(chat_id, text="Miauuu :)")
        else:
            bot.sendMessage(chat_id, text="Miauuu :(")

        del state[user_id]
        del context[user_id]

def manage_trolls(bot, update):
    if filter_user(update.message):
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        user_state = state.get(chat_id, MENU)
        user_name = update.message.from_user.first_name

        trolls = loadTrolls()
        if len(trolls) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="Nothing to manage :)")
            return

        trolls_list = list(trolls.items())
        results = ""
        for i in range(len(trolls_list)):
            results += str(i) + ": " + trolls_list[i][0] + " -> " + trolls_list[i][1] + "\n"

        context[user_id] = trolls_list
        bot.sendMessage(chat_id=update.message.chat_id, text=results)

        if user_state == MENU:
            state[user_id] = AWAIT_MANAGE  # set the state
            bot.sendMessage(chat_id,
                text="Please select id of regex to delete it or anything else to do nothing",
                reply_markup=ForceReply())
