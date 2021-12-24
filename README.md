# miau_bot
The Miau Telegram bot

# Requirements
- Python 3+
- Telegram (it also requires a bot TOKEN from Telegram)
- Mongo DB


# Usage
To launch the bot:
python3 miau_bot.py

## Dependencies
This project requires the following third-parties modules:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) Not just a Python wrapper around the Telegram Bot API.
The main dependency for the Telegram Bot API.
- [pymongo](https://pypi.python.org/pypi/pymongo) Python driver for MongoDB <http://www.mongodb.org>.
It is used for persistence.
- [tabulate](https://pypi.python.org/pypi/tabulate) Pretty-print tabular data.
It is used to print the ranking in the jankenpon command.
- [python-weather-api](https://code.google.com/archive/p/python-weather-api/) (DEPRECATED!) A python wrapper around the Yahoo! Weather, Weather.com and NOAA APIs.
It is used by the weather command.
(This library is deprecated and will be replaced by [python-forecast.io](https://github.com/ZeevG/python-forecast.io) or other similar.)
