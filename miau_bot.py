from miau.constants import auth

from miau.petting import petting
from miau.help import help
from miau.points import points
from miau.jankenpon import jankenpon
from miau.jajejijoju import jajejijoju
from miau.weather import weather
from miau.regexs import regexs
from miau.stats import stats

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler

import logging


updater = Updater(token=auth.TOKEN)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Miauuuu!!!")

start_handler = CommandHandler('hola', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help.help)
dispatcher.add_handler(help_handler)

dispatcher.add_handler(CommandHandler('stats', stats.stats))

petting_handler = CommandHandler('petting', petting.petting)
dispatcher.add_handler(petting_handler)

weather_handler = CommandHandler('weather', weather.weather)
dispatcher.add_handler(weather_handler)
#job_queue.put(weather.weather_timed, 86400, next_t=22500)

jankenpon_handler = CommandHandler('jankenpon', jankenpon.jankenpon, pass_args=True)
dispatcher.add_handler(jankenpon_handler)

dispatcher.add_handler(CommandHandler('regex', regexs.defineRegex))

dispatcher.add_handler(CommandHandler('manageregexs', regexs.manageRegexs, pass_args=True))

trainPlus1_hanlder = CommandHandler('+1', points.trainPlus1, pass_args=True)
dispatcher.add_handler(trainPlus1_hanlder)

trainMinus1_hanlder = CommandHandler('-1', points.trainMinus1, pass_args=True)
dispatcher.add_handler(trainMinus1_hanlder)

jajejijoju_handler = MessageHandler([jajejijoju.filter], jajejijoju.jajejijoju)
dispatcher.add_handler(jajejijoju_handler)

# filter for define regexs command
dispatcher.add_handler(MessageHandler([regexs.filterInputDefineRegex], regexs.enteredRegex))
# filter for manage regexs command
dispatcher.add_handler(MessageHandler([regexs.filterInputManageRegexs], regexs.deleteRegex))
# filter for regexs functionality
dispatcher.add_handler(MessageHandler([regexs.filterPattern], regexs.regex))

points_handler = MessageHandler([points.filter], points.points)
dispatcher.add_handler(points_handler)

updater.start_polling()
updater.idle()
updater.stop()
