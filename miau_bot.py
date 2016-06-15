from local_constants import TOKEN

from miau.petting import petting
from miau.help import help

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Miauuuu!!!")


start_handler = CommandHandler('hola', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help.help)
dispatcher.add_handler(help_handler)

petting_handler = CommandHandler('petting', petting.petting)
dispatcher.add_handler(petting_handler)

updater.start_polling()
updater.idle()
updater.stop()
