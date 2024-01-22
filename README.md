The application utilizes an API to fetch real-time weather conditions from any location specified by the user. If the location is not listed, the user is asked to input its latitude and longitude details. If the details are correct, the location is added to the list of locations and its current weather conditions are displayed. 
If the user enters incorrect data, the location is not added to the list. A message notifying of incorrect data is displayed and the user has an option to re-enter correct data next time the application runs.
To run the app the following modules are required to be imported:

import os, 
from dotenv import load_dotenv, 
import requests, 
import json.

An Open Weather API key is required. This can be obtained from https://openweathermap.org/ by creating an account. 

