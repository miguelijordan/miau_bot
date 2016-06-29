from miau.points import PointsPersistence

# Data
points = PointsPersistence.PointsPersistence()

def filter(message):
    return points.getWordPoints(message.text) != 0
    
def points(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    p = points.getWordPoints(text)
    sign = ''
    if p > 0:
        sign = '+'
    elif p < 0:
        sign = '-'        
        
    bot.sendMessage(chat_id, sign + str(p) + " para " + word)

def trainPlus1(bot, update, args):
    if len(args) > 0:
        word = ' '.join(args)
        points.addPoint(word)
        bot.sendMessage(update.message.chat_id, "Miauuu :)")

def trainMinus1(bot, update, args):
    if len(args) > 0:
        word = ' '.join(args)
        points.substractPoint(word)
        bot.sendMessage(update.message.chat_id, "Miauuu :(")
