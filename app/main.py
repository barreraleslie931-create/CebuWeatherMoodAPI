from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .mood import weather_to_mood
from .schemas import WeatherMoodResponse
from .services import WeatherService

app = FastAPI(
    title="Cebu Weather Mood API",
    description="Returns mood suggestions based on current weather (default: Cebu City, PH).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_service = WeatherService()

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/weather-mood", response_model=WeatherMoodResponse, tags=["mood"])
def get_weather_mood(
    city: str = Query(default=settings.city, description="City name (default: Cebu)"),
    country: str = Query(default=settings.country, description="Country code (default: PH)"),
    units: str = Query(default=settings.units, description="Units: standard|metric|imperial"),
):
    try:
        w = weather_service.fetch_current_weather(city=city, country=country, units=units)
        mood = weather_to_mood(w["weather"], w["description"])
        return WeatherMoodResponse(
            city=city,
            country=country,
            weather=w["weather"],
            description=w["description"],
            temperature=w["temperature"],
            units=units,
            mood=mood,
            source=w["source"],
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
