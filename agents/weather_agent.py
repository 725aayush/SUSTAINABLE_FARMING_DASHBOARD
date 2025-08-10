import requests
import time
from config import WEATHER_API_KEY

def update_weather(city, weather_data):
    try:
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        )
        data = response.json()
        
        weather_data.update({
            "temp": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind": data["current"]["wind_kph"]
        })
    except Exception as e:
        print(f"Weather API Error: {e}")

def start_weather_agent(weather_data, interval=60):
    from config import DEFAULT_CITY
    
    while True:
        update_weather(DEFAULT_CITY, weather_data)
        time.sleep(interval)