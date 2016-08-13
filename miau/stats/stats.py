from miau.regexs import RegexsPersistence

from telegram.emoji import Emoji
import datetime

STATIC_STATS = [ ('ID','@miiaauu_bot'),
                 ('Name','Miau'),
                 ('Specie','feline ' + Emoji.CAT_FACE),
                 ('Sex','male'),
                 ('Weight','4.69 kg'),
                 ('Height','0.5 m'),
                 ('Length','30 cm ' + Emoji.FACE_WITH_STUCK_OUT_TONGUE_AND_WINKING_EYE),
                 ('Owner','Josemi')]

START_EXECUTION_TIME = datetime.datetime.now()

def getAge():
    now = datetime.datetime.now()
    age = now - START_EXECUTION_TIME # seconds
    days = age.days
    hours, remainder = divmod(age.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return str(days) + "d " + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s."

def getConversationPower():
    regexs = RegexsPersistence.RegexsPersistence()
    return len(regexs.getRegexs())

def formatStats(stats):
    message = ""
    for s in stats:
        message += s[0] + ": " + s[1] + "\n"
    return message

def stats(bot, update):
    stats = [] + STATIC_STATS
    stats.append(('CP (Conversation Power)',str(getConversationPower())))
    stats.append(('Age',getAge()))

    message = formatStats(stats)
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
