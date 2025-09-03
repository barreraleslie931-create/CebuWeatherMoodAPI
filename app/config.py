from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    weather_api_key: str
    weather_provider: str = "openweathermap"
    city: str = "Cebu"
    country: str = "PH"
    units: str = "metric"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
