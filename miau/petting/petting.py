import os
import random

RESOURCES_DIR = "miau/petting/resources/"

def petting(bot, update):
    n = len(os.listdir(RESOURCES_DIR))
    i = random.randint(1,n)
    audio = open(RESOURCES_DIR + "miau" + str(i) + ".ogg", "rb")
    bot.sendVoice(chat_id=update.message.chat_id, voice=audio)
