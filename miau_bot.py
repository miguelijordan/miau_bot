from local_constants import TOKEN

from miau.petting import petting
from miau.help import help
from miau.points import points
from miau.jankenpon import jankenpon
from miau.jajejijoju import jajejijoju
from miau.weather import weather
from miau.troll import troll

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler

import logging


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Miauuuu!!!")

start_handler = CommandHandler('hola', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help.help)
dispatcher.add_handler(help_handler)

petting_handler = CommandHandler('petting', petting.petting)
dispatcher.add_handler(petting_handler)

weather_handler = CommandHandler('weather', weather.weather)
dispatcher.add_handler(weather_handler)
#job_queue.put(weather.weather_timed, 86400, next_t=22500)

jankenpon_handler = CommandHandler('jankenpon', jankenpon.jankenpon, pass_args=True)
dispatcher.add_handler(jankenpon_handler)

troll_handler = MessageHandler([troll.filter], troll.troll)
dispatcher.add_handler(troll_handler)

# Troll command
updater.dispatcher.add_handler(CommandHandler('troll', troll.define_troll))
# The pattern
updater.dispatcher.add_handler(MessageHandler([troll.filter_input], troll.entered_input))

jajejijoju_handler = MessageHandler([jajejijoju.filter], jajejijoju.jajejijoju)
dispatcher.add_handler(jajejijoju_handler)

trainPlus1_hanlder = CommandHandler('+1', points.trainPlus1, pass_args=True)
dispatcher.add_handler(trainPlus1_hanlder)

trainMinus1_hanlder = CommandHandler('-1', points.trainMinus1, pass_args=True)
dispatcher.add_handler(trainMinus1_hanlder)

pointsPlus1_handler = MessageHandler([points.filterPlus1], points.plus1)
dispatcher.add_handler(pointsPlus1_handler)

pointsMinus1_handler = MessageHandler([points.filterMinus1], points.minus1)
dispatcher.add_handler(pointsMinus1_handler)

updater.start_polling()
updater.idle()
updater.stop()
