# services/weather_service.py
import requests
import re

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_weather(self, slots: dict, **kwargs) -> str:
        city = slots.get("city")
        
        if not city:
            return "Which city do you want the weather for?"
        
        if not self.api_key:
            return "Weather API key not configured."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=8)
            data = response.json()
            
            if data.get("cod") != 200:
                return f"Sorry, I couldn't find weather for {city}."
            
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The weather in {city} is {desc} with a temperature of {temp}°C."
        except Exception as e:
            return f"I couldn't reach the weather service: {e}"