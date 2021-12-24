from miau.points import PointsPersistence
import re
import random

# Data
pointsData = PointsPersistence.PointsPersistence()

def filter(message):
    words = re.split("\W+", message.text)
    for w in words:
        if pointsData.getWordPoints(w.lower()) != 0:
            return True
    return False

def points(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    words = re.split("\W+", text)
    words = map(lambda w : w.lower(), words)
    wordsPoints = [w for w in words if pointsData.getWordPoints(w) != 0]#filter(lambda x: pointsData.getWordPoints(x) != 0, words)
    w = random.choice(wordsPoints)
    p = pointsData.getWordPoints(w)
    sign = ''
    if p > 0:
        sign = '+'

    bot.sendMessage(chat_id, sign + str(p) + " para " + w)

def trainPlus1(bot, update, args):
    if len(args) > 0:
        word = args[0].lower()
        pointsData.addPoint(word)
        bot.sendMessage(update.message.chat_id, "Miauuu :)")

def trainMinus1(bot, update, args):
    if len(args) > 0:
        word = args[0].lower()
        pointsData.substractPoint(word)
        bot.sendMessage(update.message.chat_id, "Miauuu :(")
