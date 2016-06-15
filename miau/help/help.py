def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="""
Hola! Soy Miau y esto es lo que puedes hacer ahora mismo conmigo:
/hola       Saluda al gato.
/petting    Acaricia al gato.
/help       Pide ayuda al gato.
/+1         Entrena al gato con refuerzo positivo.
/-1         Entrena al gato con refuerzo negativo.
""")
