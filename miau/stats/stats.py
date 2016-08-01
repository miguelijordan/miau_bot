from miau.regexs import RegexsPersistence

STATIC_STATS = [ ('ID','@miiaauu_bot'),
                 ('Name','Miau'),
                 ('Specie','feline'),
                 ('Sex','male'),
                 ('Weight','4.69 kg'),
                 ('Height','0.69 m'),
                 ('Length','30 cm'),
                 ('Owner','Josemi')]

def formatStats(stats):
    message = ""
    for s in stats:
        message += s[0] + ": " + s[1] + "\n"
    return message

def getConversationPower():
    regexs = RegexsPersistence.RegexsPersistence()
    return len(regexs.getRegexs())

def stats(bot, update):
    stats = STATIC_STATS
    stats.append(('CP (Conversation Power)',str(getConversationPower())+' regexs'))


    message = formatStats(stats)
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
