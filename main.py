import os
from dotenv import load_dotenv
import requests

load_dotenv()  # load variables from .env file
api_key = os.getenv("API_KEY")  # save API key to a variable api_key

api_url = os.getenv("API_URL")  # save API key to a variable api_key
api_url = f"{api_url}?appid={api_key}"  # save API link to a variable api


locations = {
    "High Barnet": {"latitude": 51.650341, "longitude": -0.195190},
    "Topolcany": {"latitude": 48.554499, "longitude": 18.179364},
    "San Francisco": {"latitude": 37.773972, "longitude": -122.431297},
    "Bratislava": {"latitude": 48.148598, "longitude": 17.107748},
    "Cairo": {"latitude": 29.95375640, "longitude": 31.53700030},
    }


def get_weather(town):
    if town in locations:
        town_lat = locations[town]["latitude"]
        town_long = locations[town]["longitude"]
        weather_response = requests.get(f"{api_url}&lat={town_lat}&lon={town_long}") # make call to API to receive weather data
        town_weather = weather_response.json() # convert the API data format to json (similar to python dictionary
        country = town_weather["sys"]["country"]
        country_location = town_weather["name"]
        town_current_weather_condition = town_weather["weather"][0]["description"]
        town_current_temperature = round((town_weather["main"]["temp"]) - 273.15, 2)
        town_min_temperature = round((town_weather["main"]["temp_min"]) - 273.15, 2)
        town_max_temperature = round((town_weather["main"]["temp_max"]) - 273.15, 2)
        town_wind = town_weather["wind"]["speed"]
        town_humidity = town_weather["main"]["humidity"]
        town_complete_data = {
            "country:": country,
            "location:": country_location,
            "current_weather_condition:": town_current_weather_condition,
            "current temperature (Celsius):": town_current_temperature,
            "minimum temperature (Celsius)": town_min_temperature,
            "maximum temperature (Celsius)": town_max_temperature,
            "wind (m/s):": town_wind,
            "humidity (%):": town_humidity,
        }
        for key, value in town_complete_data.items():
            print(key, value)
        print()
    else:
        print("Ensure correct spelling or town is included in the list of locations.")

get_weather("Topolcany")
get_weather("High Barnet")
get_weather("San Francisco")











