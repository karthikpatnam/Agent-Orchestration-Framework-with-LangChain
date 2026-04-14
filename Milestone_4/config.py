from pydantic_settings import BaseSettings  # type: ignore

class Settings(BaseSettings):
    ORS_API_KEY: str
    OPENWEATHER_API_KEY: str
    GOOGLE_API_KEY: str
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env

settings = Settings()
