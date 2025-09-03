import requests
from typing import Dict, Any
from .config import settings

class WeatherService:
    def __init__(self):
        self.provider = settings.weather_provider.lower().strip()

    def fetch_current_weather(self, city: str, country: str, units: str) -> Dict[str, Any]:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city},{country}",
            "appid": settings.weather_api_key,
            "units": units,
        }
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code != 200:
            try:
                detail = resp.json()
            except Exception:
                detail = {"message": resp.text}
            raise RuntimeError(f"Weather API error ({resp.status_code}): {detail.get('message', 'Unknown error')}")
        data = resp.json()
        main = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        temp = float(data["main"]["temp"])
        return {
            "weather": main,
            "description": description,
            "temperature": temp,
            "source": "openweathermap",
        }
