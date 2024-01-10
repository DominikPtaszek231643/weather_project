import requests
from pprint import pprint

API_key = '6258e383fda86a1c201f5e3e76b0f99d'


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    pprint(weather_data
           )

    return weather_data


get_weather(API_key, 'Warsaw')














