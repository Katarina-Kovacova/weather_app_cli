import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()  # load variables from .env file
api_key = os.getenv("OPENWEATHER_API_KEY")  # save API key to a variable api_key

api_url = os.getenv("OPENWEATHER_URL")  # save API key to a variable api_key
api_url = f"{api_url}?appid={api_key}"  # save API link to a variable api


locations = {
    "High Barnet": {"latitude": 51.650341, "longitude": -0.195190},
    "Topolcany": {"latitude": 48.554499, "longitude": 18.179364},
    "San Francisco": {"latitude": 37.773972, "longitude": -122.431297},
    "Bratislava": {"latitude": 48.148598, "longitude": 17.107748},
    "Cairo": {"latitude": 29.95375640, "longitude": 31.53700030},
    }


# create function to convert_dict_to_json(locations_dict):  # function to convert cities dictionary to json file
def cities_dict_to_json(locations_dict):
    with open("cities.json", "w") as f:
        json.dump(locations_dict, f, indent=4)


# create function to load json file into python dictionary
def load_json_to_dict():
    with open("cities.json", "r") as file:
        cities_dictionary = json.load(file)
    return cities_dictionary


def add_city_to_dict(new_city, new_city_lat, new_city_long, cities_dict):  # add new city if not in locations dictionary
    new_city_lat_long = {"latitude": float(new_city_lat),
                         "longitude": float(new_city_long),
                         }
    cities_dict[new_city] = new_city_lat_long
    return cities_dict


print()


def get_weather(town):
    town_lat = locations[town]["latitude"]
    town_long = locations[town]["longitude"]
    weather_response = requests.get(f"{api_url}&lat={town_lat}&lon={town_long}") # make call to API to receive weather data
    status = weather_response.status_code

    if status == 400:
        print(f"Error {status} - Bad Request - missing parameters/ incorrect format paramenters/ values out of range.")
    elif status == 401:
        print(f"Error {status} - Unauthorised - access denied.")
    elif status == 404:
        print(f"Error {status} - Not found.")
    elif status == 429:
        print(f"Error {status} - Too many requests.")
    elif 499 < status < 600:
        print(f"Error {status} - Unexpected Error.")
    elif 99 < status < 200 and 300 < status < 400:
        raise Exception("Unsuccessful request.")
    else:

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


if __name__ == "__main__":
    try:
        locations = load_json_to_dict()
    except FileNotFoundError:
        cities_dict_to_json(locations)

    print("Welcome to our weather app!")
    print()
    area = input("Please select location to view the current weather conditions: ")
    print()

    if area in locations:
        try:
            get_weather(area)
        except KeyError:
            print("Unsuccessful request")
    else:
        print(f"Sorry this city is not on the list.\nIf you know the {area} latitude and longitude, please enter it now.")
        print()
        area_latitude = input(f"{area} latitude: ")
        area_longitude = input(f"{area} longitude: ")
        updated_cities_locations = add_city_to_dict(area, area_latitude, area_longitude, locations)
        cities_dict_to_json(updated_cities_locations)
        print()
        get_weather(area)















