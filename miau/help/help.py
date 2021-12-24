def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="""
Hola! Soy Miau y esto es lo que puedes hacer ahora mismo conmigo:
/hola - Saluda al gato.
/stats - Muestra información básica del gato.
/petting - Acaricia al gato.
/jankenpon - Juega con el gato.
/weather - Pregunta al gato por el tiempo que hace.
/+1 - Entrena al gato con refuerzo positivo.
/-1 - Entrena al gato con refuerzo negativo.
/help - Pide ayuda al gato.
""")
