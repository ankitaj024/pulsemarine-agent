import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PulseMarine Agent API"
    DATABASE_URI: str = "postgresql://pulsemarine:aC4rvDo46cKECzbyEtsw396JlwJzkgT3@dpg-d4apq3ripnbc73afi930-a.frankfurt-postgres.render.com/pulsemarine_k2ri"
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()
