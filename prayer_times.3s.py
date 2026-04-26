#!/usr/bin/env /Users/abdullatif/swiftbar_folder/.venv/bin/python

import platform
from datetime import datetime, timedelta, date
import sys
from dotenv import load_dotenv
import requests
import os
import json
import subprocess

running_os = platform.system()
print(os)

args = sys.argv
time_mode_24 = True

fileName = "/tmp/data.json"
if len(args) > 1:
    if args[1] == "am-pm":
        time_mode_24 = False
        with open('/Users/abdullatif/swiftbar_folder/debug.txt', 'w') as f:
            f.write(str(sys.argv))
    if args[1] == "24-hour":
        time_mode_24 = True
        with open('/Users/abdullatif/swiftbar_folder/debug.txt', 'w') as f:
            f.write(str(sys.argv))
    sys.exit()

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


def make_a_notification(title, msg):

    subprocess.run(
        ["osascript", "-e", f'display notification "{msg}" with title "{title}" '])


def time_comparison(client_time, api_times, prayers):
    isha = datetime.strptime(api_times[len(api_times)-1], "%H:%M").time()

    for time in api_times:

        date_format_time = datetime.strptime(
            time, "%H:%M").time()

        if client_time < date_format_time:
            next_time = date_format_time.strftime("%H:%M")
            prayer_name = next(k for k, v in prayers.items() if v == time)
            if day_in_the_week.lower() == "friday" and prayer_name.lower() == "dhuhr":
                print(f"Jumaa - {next_time}")
                make_a_notification(
                    f"Salah Jumaa - {next_time}.", "Jumaa prayer.")
                break
            print(f"{prayer_name} - {next_time}")
            make_a_notification(
                f"Salah {prayer_name} - {next_time}.", f"{prayer_name} prayer.")

            print("---")
            print("pm-am | bash='/bin/bash' param1='-c' param2='/Users/abdullatif/swiftbar_folder/.venv/bin/python /Users/abdullatif/swiftbar_folder/prayer_times.py am-pm' terminal=false")
            print("24-hour| bash='/bin/bash' param1='-c' param2='/Users/abdullatif/swiftbar_folder/.venv/bin/python /Users/abdullatif/swiftbar_folder/prayer_times.py 24-hour' terminal=false")

            break

    if client_time > isha:
        tomorrow = date.today() + timedelta(days=1)
        prayer_time = get_tomorrow_fajr(tomorrow)
        print(f"Fajr — {prayer_time}")
        make_a_notification(
            f"Salah Fajr - {prayer_time}.", "Fajr prayer.")


get_prayer_times()
