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


# def lower_case_dict(locations_dict):
#     lower_case_locations = dict((k.lower(), v) for k, v in locations_dict.items())
#     return lower_case_locations


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


def get_weather(town):
    town_lat = locations[town]["latitude"]
    town_long = locations[town]["longitude"]
    # make call to API to receive weather data
    weather_response = requests.get(f"{api_url}&lat={town_lat}&lon={town_long}")
    print(weather_response)


    if 200 <= weather_response.status_code <= 299:
        # convert the API data format to json (similar to python dictionary
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
        #print(weather_response.status_code)
        #print(weather_response.content)  # prints the content of the error message
        new_weather_response = json.loads(weather_response.content.decode('utf-8'))  #error message cast from b-type string to dictionary
        print(f"Error: {new_weather_response['cod']} - {new_weather_response['message']}")
    elif weather_response.status_code in BAD_RESPONSE_CODES_WE_CAN_DO_SOMETHING_ABOUT:
        print(weather_response.status_code)
        print(weather_response.content)  # prints the content of the error message
        new_weather_response = json.loads(weather_response.content.decode('utf-8'))
        print(f"Error: {new_weather_response['cod']} - {new_weather_response['message']}")
    elif 99 < weather_response.status_code < 200 or 300 < weather_response.status_code < 400 or 500 <= weather_response.status_code <= 599:
        raise Exception("Unsuccessful request.")


try:
    locations = load_json_to_dict()
except FileNotFoundError:
    cities_dict_to_json(locations)
    print("File not found. Using default locations.")

print("Welcome to our weather app!")

area = input("Please select location to view the current weather conditions: ").title()


if area in locations:
    get_weather(area)
else:
    print(f"Sorry this city is not on the list.\nIf you know the {area} latitude and longitude, please enter it now.")
    print()
    # TODO: CREATE FUNCTION TO GET NEW CITY LAT AND LONG (catch input errors if any)
    # TODO: CREATE FUNCTION TO CHECK RESPONSE STATUS
    # TODO: IF STATUS CODE OK: ADD NEW CITY ELSE DON'T ADD CITY
    area_latitude = input(f"{area} latitude: ")
    area_longitude = input(f"{area} longitude: ")
    # get response
    updated_cities_locations = add_city_to_dict(area, area_latitude, area_longitude, locations)
    cities_dict_to_json(updated_cities_locations)
    get_weather(area)
