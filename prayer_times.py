#!/usr/bin/env python3
from dotenv import load_dotenv
import requests
import os
from datetime import datetime, timedelta, date
now = datetime.now().time().replace(microsecond=0)

load_dotenv()
API_KEY = os.getenv("API_KEY",)


server_api = f"https://islamicapi.com/api/v1/prayer-time/?lat=30.1038551&lon=31.637056&api_key={API_KEY}&method=5"


def get_prayer_times():
    # fetch = requests.get(
    #     server_api)

    jsoned_data = {
        "code": 200,
        "status": "success",
        "data": {
            "times": {
                "Fajr": "04:04",
                "Sunrise": "05:27",
                        "Dhuhr": "11:54",
                        "Asr": "15:28",
                        "Sunset": "18:21",
                        "Maghrib": "18:21",
                        "Isha": "19:39",
                        "Imsak": "03:54",
                        "Midnight": "23:54",
                        "Firstthird": "22:03",
                        "Lastthird": "01:45"
            },
            "date": {
                "readable": "15 Apr 2026",
                "timestamp": "1776211200",
                "hijri": {
                            "date": "1447-10-27",
                            "format": "YYYY-MM-DD",
                    "day": "27",
                    "weekday": {
                                    "en": "Wednesday",
                                    "ar": "الأربعاء"
                    },
                    "month": {
                        "number": 10,
                        "en": "Shawwal",
                        "ar": "شَوَّال",
                        "days": 29
                    },
                    "year": "1447",
                            "designation": {
                        "abbreviated": "AH",
                        "expanded": "Anno Hegirae"
                    },
                    "holidays": [],
                    "adjustedHolidays": [],
                    "method": "UAQ",
                    "shift": 0
                },
                "gregorian": {
                    "date": "2026-04-15",
                            "format": "YYYY-MM-DD",
                            "day": "15",
                    "weekday": {
                        "en": "Wednesday"
                    },
                    "month": {
                        "number": 4,
                        "en": "April"
                    },
                    "year": "2026",
                            "designation": {
                        "abbreviated": "AD",
                        "expanded": "Anno Domini"
                    }
                }
            },
            "qibla": {
                "direction": {
                    "degrees": 137.79,
                    "from": "North",
                    "clockwise": "true"
                },
                "distance": {
                    "value": 1265.66,
                    "unit": "km"
                }
            },
            "prohibited_times": {
                "sunrise": {
                    "start": "05:27",
                    "end": "05:42"
                },
                "noon": {
                    "start": "11:44",
                    "end": "11:54"
                },
                "sunset": {
                    "start": "18:06",
                    "end": "18:21"
                }
            },
            "timezone": {
                "name": "Africa/Cairo",
                "utc_offset": "+02:00",
                        "abbreviation": "EET"
            }
        }
    }
    data = jsoned_data["data"]
    times = data["times"]
    needed_data_keys = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
    kept_values = {key: times[key] for key in needed_data_keys}
    values = list(kept_values.values())

    values.sort()

    time_comparison(now, values, kept_values)


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
    print(api_times)
    isha = datetime.strptime(api_times[len(api_times)-1], "%H:%M").time()

    for time in api_times:

        date_format_time = datetime.strptime(time, "%H:%M").time()

        if client_time < date_format_time:
            next_time = date_format_time
            prayer_name = next(k for k, v in prayers.items() if v == time)
            print(next_time, prayer_name, "cats")
            break

    if client_time > isha:
        tomorrow = date.today() + timedelta(days=1)
        print(get_tomorrow_fajr(tomorrow))
        print("fajr prayer brother ")

# print(type(current_time))


get_prayer_times()
