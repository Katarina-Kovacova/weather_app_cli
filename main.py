import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()  # load variables from .env file
api_key = os.getenv("OPENWEATHER_API_KEY")  # save API key to a variable api_key

api_url = os.getenv("OPENWEATHER_URL")  # save API key to a variable api_key
api_url = f"{api_url}?appid={api_key}"  # save API link to a variable api

BAD_RESPONSE_CODES_WE_CANNOT_DO_ANYTHING_ABOUT = (400, 401, 404, 429)
BAD_RESPONSE_CODES_WE_CAN_DO_SOMETHING_ABOUT = (500, 501, 502, 503)

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


# function returns the weather response on an API call for a new city that is not listed
def get_weather_response(town_latit, town_longit):
    city_weather_response = requests.get(f"{api_url}&lat={town_latit}&lon={town_longit}")
    return city_weather_response


# function to add new city if not in locations dictionary
def add_city_to_dict(new_city, new_city_latitude, new_city_longitude, cities_dict):
    new_city_lat_long = {"latitude": float(new_city_latitude),
                         "longitude": float(new_city_longitude),
                         }
    cities_dict[new_city] = new_city_lat_long
    return cities_dict


# function to obtain city weather data
def get_weather(town):
    town_lat = locations[town]["latitude"]
    town_long = locations[town]["longitude"]
    # make call to API to receive weather data
    weather_response = requests.get(f"{api_url}&lat={town_lat}&lon={town_long}")

    if 200 <= weather_response.status_code <= 299:
        # convert the API data format to json (similar to python dictionary)
        town_weather = weather_response.json()
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
    elif weather_response.status_code in BAD_RESPONSE_CODES_WE_CANNOT_DO_ANYTHING_ABOUT:
        # error message cast from b-type string to dictionary
        new_weather_response = json.loads(weather_response.content.decode('utf-8'))
        print(f"Error: {new_weather_response['cod']} - {new_weather_response['message']}")
    elif weather_response.status_code in BAD_RESPONSE_CODES_WE_CAN_DO_SOMETHING_ABOUT:
        print(weather_response.status_code)
        print(weather_response.content)  # prints the content of the error message
        new_weather_response = json.loads(weather_response.content.decode('utf-8'))
        print(f"Error: {new_weather_response['cod']} - {new_weather_response['message']}")
    elif 99 < weather_response.status_code < 200 or 300 < weather_response.status_code < 400 or \
            500 <= weather_response.status_code <= 599:
        raise Exception("Unsuccessful request.")


# function returns user input for new city latitude
def new_city_lat():
    while True:
        try:
            new_city_latitude = float(input("Please enter the city latitude as a decimal number: "))
            break
        except ValueError:
            print("Please only enter decimal numbers.")
    return new_city_latitude


# function returns user input for new city longitude
def new_city_long():
    while True:
        try:
            new_city_longitude = float(input("Please enter the city longitude as a decimal number: "))
            break
        except ValueError:
            print("Please only enter decimal numbers.")
    return new_city_longitude


# locations will be loaded from .json file if .json file exists. If not, the default location dictionary will be used
try:
    locations = load_json_to_dict()
except FileNotFoundError:
    cities_dict_to_json(locations)
    print("File not found. Using default locations.")

print("Welcome to our weather app!")
area = input("Please select location to view the current weather conditions: ").title()

"""
check if area is listed, the weather conditions are fetched and printed
if city is not listed, user inputs new city latitude and longitude. 
If response successful, city is added to .json and weather conditions are displayed.
If response unsuccessful, user gets a "Unsuccessful request message and to re-enter correct data."
"""
if area in locations:
    get_weather(area)

else:
    print(f"Sorry this city is not on the list.\nIf you know the {area} latitude and longitude, please enter it now.")
    print()
    area_latitude = new_city_lat()
    area_longitude = new_city_long()
    new_area_response = get_weather_response(area_latitude, area_longitude)
    if 200 <= new_area_response.status_code <= 299:
        updated_cities_locations = add_city_to_dict(area, area_latitude, area_longitude, locations)
        cities_dict_to_json(updated_cities_locations)
        get_weather(area)
    else:
        print("Unsuccessful request. Please check you have entered the correct info and try again.")

