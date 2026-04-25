#!/usr/bin/env /Users/abdullatif/swiftbar_folder/venv/bin/python
# echo "☀️ My Plugin"
# echo "---"

# This item has a submenu — hovering/clicking it reveals options to the side
# echo "Appearance"
# echo "-- Disable Dark Mode | bash='osascript -e \"tell app \"System Events\" to tell appearance preferences to set dark mode to false\"' terminal=false refresh=true"
# echo "-- Enable Dark Mode  | bash='osascript -e \"tell app \"System Events\" to tell appearance preferences to set dark mode to true\"' terminal=false refresh=true"
from datetime import datetime, timedelta, date
import sys
from dotenv import load_dotenv
import requests
import os
import json
args = sys.argv
fileName = "tmp/data.json"

now = datetime.now().time().replace(microsecond=0)
day_in_the_week = datetime.now().strftime("%A")
todays_date = datetime.now().date()
load_dotenv()
API_KEY = os.getenv("API_KEY")


server_api = f"https://islamicapi.com/api/v1/prayer-time/?lat=30.1038551&lon=31.637056&api_key={API_KEY}&method=5"


def get_cached_data():

    if not os.path.exists(fileName):
        return None
    with open(fileName, "r") as file:
        data = json.load(file)

        return data


def get_prayer_times():
    cached_data = get_cached_data()
    if cached_data:
        date = cached_data["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        if date_obj == todays_date:

            kept_values = cached_data["values"]
            values = list(kept_values.values())
            print(values, kept_values)
            time_comparison(now, values, kept_values)
            return
    fetch = requests.get(
        server_api)

    jsoned_data = fetch.json()
    data = jsoned_data["data"]
    times = data["times"]
    needed_data_keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    kept_values = {key: times[key] for key in needed_data_keys}
    values = list(kept_values.values())

    values.sort()
    write_new_file_data(kept_values, todays_date)
    time_comparison(now, values, kept_values)


def write_new_file_data(values, date):
    qouta = {"values": values, "date": str(date)}
    with open(fileName, "w") as file:

        json.dump(qouta, file)


def get_tomorrow_fajr(date):
    server_api = f"https://islamicapi.com/api/v1/prayer-time/?lat=30.1038551&lon=31.637056&date={date}&api_key={API_KEY}&method=5"
    fetch = requests.get(
        server_api)

    jsoned_data = fetch.json()
    data = jsoned_data["data"]
    times = data["times"]
    prayer_time = times["Fajr"]
    return prayer_time


def time_comparison(client_time, api_times, prayers):
    isha = datetime.strptime(api_times[len(api_times)-1], "%H:%M").time()

    for time in api_times:

        date_format_time = datetime.strptime(
            time, "%H:%M").time()

        if client_time < date_format_time:
            next_time = date_format_time.strftime("%H:%M")
            prayer_name = next(k for k, v in prayers.items() if v == time)
            if day_in_the_week.lower() == "friday" and prayer_name.lower() == "dhuhr":
                print(f"Friday - {next_time}")
                break
            print(f"{prayer_name} - {next_time}")
            break

    if client_time > isha:
        tomorrow = date.today() + timedelta(days=1)
        prayer_time = get_tomorrow_fajr(tomorrow)
        print(f"Fajr — {prayer_time}") 
        print(
            f"---")
        print("pm-am")
        print("24-hhours")


get_prayer_times()
