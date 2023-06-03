from typing import Union

import geocoder
import requests
from dotenv import dotenv_values
from prettytable import PrettyTable

# Environment variables
env = dotenv_values(".env")


def fetch_weather_data(lat: Union[float, str], lon: Union[float, str]):
    url = "https://ai-weather-by-meteosource.p.rapidapi.com/current"
    query_string = {
        "lat": lat,
        "lon": lon,
        "timezone": "auto",
        "language": "en",
        "units": "auto",
    }
    headers = {
        "X-RapidAPI-Key": env.get("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": env.get("RAPIDAPI_HOST"),
    }
    data = requests.get(url, headers=headers, params=query_string).json()
    return data


def extract_required_fields(data: dict):
    try:
        fields = {
            "latitude": data["lat"],
            "longitude": data["lon"],
            "icon": {
                "name": data["current"]["icon"],
                "num": data["current"]["icon_num"],
            },
            "humidity": data["current"]["humidity"],
            "temperature": data["current"]["temperature"],
            "visibility": data["current"]["visibility"],
            "wind": data["current"]["wind"],
        }
        return fields
    except KeyError:
        print("That field does not exist in the data!")


def get_current_location() -> Union[tuple[str, str], None]:
    # Get my current location
    location = geocoder.ip("me")
    if location is not None:
        # Get the latitude and longitude from my location
        latitude = location.lat
        longitude = location.lng
        return (latitude, longitude)
    return None


def generate_table_data(data: dict) -> None:
    table = PrettyTable()
    table.field_names = [
        key.title() for key, value in data.items() if not isinstance(value, dict)
    ]
    table.add_row([value for value in data.values() if not isinstance(value, dict)])
    return table


if __name__ == "__main__":
    try:
        print("Here is your current weather data...")
        lat, lng = get_current_location()
        raw_data = fetch_weather_data(lat=lat, lon=lng)
        cooked_data = extract_required_fields(raw_data)
        data = generate_table_data(cooked_data)
        print(data)
    except Exception as e:
        # Log the error to the file system and print some helpful information to the user
        with open("./error.txt", "w+") as f:
            f.write(str(e))
        print("Something went wrong...!")
