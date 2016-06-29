import re                                   # Regular expression operations

data = WordsChatPersistence()

def showData(bot, update):
    users = data.getUsers()

    # user_name = update.message.from_user.first_name
    # if isUserAllowed(user_name):
    #     chat_id = update.message.chat_id
    #     user_id = update.message.from_user.id
    #     user_state = state.get(chat_id, MENU)
    #
    #     allRegexs = regexs.getRegexs()
    #     if len(allRegexs) == 0:
    #         bot.sendMessage(chat_id, "Nothing to manage :)")
    #         return
    #     else:
    #         _showRegexs(bot, chat_id, allRegexs)
    #
    #     if user_state == MENU:
    #         context[user_id] = allRegexs
    #         state[user_id] = AWAIT_MANAGE  # set the state
    #         bot.sendMessage(chat_id, "Please select id of regex to delete it or anything else to do nothing", reply_markup=ForceReply())

def storeData(bot, update):
    text = update.message.text
    user = update.message.from_user.id

    words = re.split('\W+', text)
    for w in words:
        data.addWord({'user':user, 'word':w})
