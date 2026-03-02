from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Rolling Agent API"
    DATABASE_URI: str = "postgresql://pulsemarine:aC4rvDo46cKECzbyEtsw396JlwJzkgT3@dpg-d4apq3ripnbc73afi930-a.frankfurt-postgres.render.com/pulsemarine_k2ri"
    OPENROUTER_API_KEY: str = "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"

    class Config:
        env_file = ".env"

settings = Settings()
