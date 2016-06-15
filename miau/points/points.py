import os

PLUS1_FILEPATH = "miau/points/resources/plus1.dat"
MINUS1_FILEPATH = "miau/points/resources/minus1.dat"

def getStrings(filepath):
    with open(filepath, 'r') as file:
        strings = file.readlines()
    return list(map(str.rstrip, strings))

def filter(text, strings):
    words = text.split(" ")
    matchings = list(set(strings) & set(words))
    return matchings

def filterPlus1(message):
    strings = getStrings(PLUS1_FILEPATH)
    matching = filter(message.text, strings)
    return matching != []

def filterMinus1(message):
    strings = getStrings(MINUS1_FILEPATH)
    matching = filter(message.text, strings)
    return matching != []

def plus1(bot, update):
    text = update.message.text
    strings = getStrings(PLUS1_FILEPATH)
    matching = filter(text, strings)

    word = matching[0]
    bot.sendMessage(chat_id=update.message.chat_id, text="+1 para " + word)

def minus1(bot, update):
    message = update.message.text
    strings = getStrings(MINUS1_FILEPATH)
    matching = filter(message, strings)

    word = matching[0]
    bot.sendMessage(chat_id=update.message.chat_id, text="-1 para " + word)
