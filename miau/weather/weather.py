import pywapi

MALAGA_CITY_CODE = "SPXX0052"

# Images
SHOWERS_IMG = "miau/weather/resources/w1_showers.png"
CLOUDY_IMG = "miau/weather/resources/w2_cloudy.png"
PARTLY_SUNNY_IMG = "miau/weather/resources/w3_partly_sunny.png"
MOSTLY_SUNNY_IMG = "miau/weather/resources/w4_mostly_sunny.png"
SUNNY_IMG = "miau/weather/resources/w5_sunny.png"

# Text from weather.com
FAIR = "fair"
MOSTLY_CLOUDY = "mostly cloudy"
PARTLY_CLOUDY = "partly cloudy"
CLOUDY = "cloudy"
MOSTLY_SUNNY = "mostly sunny"
PARTLY_SUNNY = "partly sunny"
SUNNY = "sunny"
LIGHT_RAIN = "light rain"
THUNDERSTOMS = "thunderstoms"   # PM or AM
SCATTERED_THUNDERSTOMS = "scattered thunderstoms"   # PM or AM
SHOWERS = "showers"             # PM or AM

# Map Text -> Image
WEATHERS = {THUNDERSTOMS: SHOWERS_IMG,
            SCATTERED_THUNDERSTOMS: SHOWERS_IMG,
            SHOWERS: SHOWERS_IMG,

            LIGHT_RAIN: CLOUDY_IMG,
            CLOUDY: CLOUDY_IMG,
            MOSTLY_CLOUDY: CLOUDY_IMG,

            PARTLY_CLOUDY: PARTLY_SUNNY_IMG,
            PARTLY_SUNNY: PARTLY_SUNNY_IMG,

            MOSTLY_SUNNY: MOSTLY_SUNNY_IMG,
            FAIR: MOSTLY_SUNNY_IMG,

            SUNNY: SUNNY_IMG,
            }

def weather(bot, update):
    weather_com_result = pywapi.get_weather_from_weather_com(MALAGA_CITY_CODE)
    weather_text = weather_com_result['current_conditions']['text']

    # Filter the text
    weather_text = weather_text.lower()
    if weather_text.startswith('PM ') or weather_text.startswith('AM '):
        weather_text = weather_text[3:]

    if weather_text in WEATHERS:
        image_weather = WEATHERS[weather_text]
        image = open(image_weather, "rb")
        bot.sendPhoto(chat_id=update.message.chat_id, photo=image)
