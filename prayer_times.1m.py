#!/usr/bin/env /Users/abdullatif/swiftbar_folder/.venv/bin/python


from datetime import datetime, timedelta, date
import sys
from dotenv import load_dotenv
import requests
import os
import json


args = sys.argv
time_mode_24 = False
with open('/Users/abdullatif/swiftbar_folder/debug.txt', 'w') as f:
    f.write(str(sys.argv))
fileName = "/tmp/data.json"
if len(args) > 1:
    if args[1] == "am-pm":
        time_mode_24 = True
    if args[1] == "24-hour":
        time_mode_24 = False
    with open('/Users/abdullatif/swiftbar_folder/time.txt', 'w') as f:
        f.write(str(time_mode_24))
    sys.exit()


now = datetime.now().time().replace(microsecond=0)
day_in_the_week = datetime.now().strftime("%A")
todays_date = datetime.now().date()
load_dotenv()
API_KEY = os.getenv("API_KEY")


server_api = f"https://islamicapi.com/api/v1/prayer-time/?lat=30.1038551&lon=31.637056&api_key={API_KEY}&method=5"


def is_time_24():
    with open('/Users/abdullatif/swiftbar_folder/time.txt', 'r') as f:
        content = f.read().strip()

        if content == str(True):

            return True

    return False


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


# def make_a_notification(title, msg):

#     subprocess.run(
#         ["osascript", "-e", f'display notification "{msg}" with title "{title}" '])

def time_options(next_time, mode):

    if mode == False:

        return next_time

    time_transform_rate = timedelta(hours=12)
    if mode:
        datetime_next_time = datetime.strptime(next_time, "%H:%M")
        timedelta_time = timedelta(
            hours=datetime_next_time.hour, minutes=datetime_next_time.minute)

        if timedelta_time > time_transform_rate:
            new_time = timedelta_time-time_transform_rate


            return f"{new_time} Pm"
    str_next_time=next_time.strftime("%H:%M") 
    
    return f"{str_next_time} Am"


def time_comparison(client_time, api_times, prayers):
    isha = datetime.strptime(api_times[len(api_times)-1], "%H:%M").time()
    time_24_12 = is_time_24()

    for time in api_times:

        date_format_time = datetime.strptime(
            time, "%H:%M").time()

        if client_time < date_format_time:
            next_time = date_format_time.strftime("%H:%M")
            prayer_name = next(k for k, v in prayers.items() if v == time)
            if day_in_the_week.lower() == "friday" and prayer_name.lower() == "dhuhr":
                time = time_options(next_time, time_24_12)
                print(f"Jumaa - {next_time}")

                break
            time = time_options(next_time, time_24_12)
            print(f"{prayer_name} - {time}")

            print("---")
            print("pm-am | bash='/bin/bash' param1='-c' param2='/Users/abdullatif/swiftbar_folder/.venv/bin/python /Users/abdullatif/swiftbar_folder/prayer_times.1m.py am-pm' terminal=false")
            print("24-hour| bash='/bin/bash' param1='-c' param2='/Users/abdullatif/swiftbar_folder/.venv/bin/python /Users/abdullatif/swiftbar_folder/prayer_times.1m.py 24-hour' terminal=false")

            break

    if client_time > isha:
        tomorrow = date.today() + timedelta(days=1)
        prayer_time = get_tomorrow_fajr(tomorrow)
        time = time_options(prayer_time, time_24_12)
        print(f"Fajr — {time}")


get_prayer_times()
