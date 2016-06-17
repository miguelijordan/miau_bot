JA = "jajaja"
JE = "jejeje"
JI = "jijiji"
JO = "jojojo"
JU = "jujuju"
JAJEJIJOJU = [JA, JE, JI, JO, JU]

TRANSITIONS = { (0, JA): (1, JE),
                (0, JE): (4, JI),
                (0, JI): (7, JO),
                (0, JO): (10, JU),
                (0, JU): (13, JA),

                (1, JI): (2, None),
                (2, JO): (3, None),
                (3, JU): (0, None),

                (4, JO): (5, None),
                (5, JU): (6, None),
                (6, JA): (0, None),

                (7, JU): (8, None),
                (8, JA): (9, None),
                (9, JE): (0, None),

                (10, JA): (11, None),
                (11, JE): (12, None),
                (12, JI): (0, None),

                (13, JE): (14, None),
                (14, JI): (15, None),
                (15, JO): (0, None)}

current_state = 0

def sendLaugh(bot, message, text):
    bot.sendMessage(chat_id=message.chat_id, text=text)

def sendMinus1(bot, message):
    bot.sendMessage(chat_id=message.chat_id, text="-1 para " + message.from_user.first_name)

def process(bot, message, state, word):
    if word not in JAJEJIJOJU:
        word = None

    if (state, word) in TRANSITIONS:
        new_state, text = TRANSITIONS[(state, word)]
        if text is not None:
            sendLaugh(bot, message, text)
        return new_state
    else:
        sendMinus1(bot, message)
        return 0

def filter(message):
    word = message.text.rstrip().lower()
    return (current_state == 0 and word in JAJEJIJOJU) or current_state != 0

def jajejijoju(bot, update):
    text = update.message.text
    word = text.rstrip().lower()
    global current_state
    current_state = process(bot, update.message, current_state, word)
