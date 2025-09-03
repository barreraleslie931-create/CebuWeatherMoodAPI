from pydantic import BaseModel

class WeatherMoodResponse(BaseModel):
    city: str
    country: str
    weather: str
    description: str
    temperature: float
    units: str
    mood: str
    source: str
