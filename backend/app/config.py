"""
Centralized settings for the app
This will read real env variables from a .env file
"""

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    #Default will be local host but .env should override it when AWS is setup
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/cashcow"


    #No default value because a wrong key will cause a silent error
    secret_key: str

    #Default will be local host but .env should override it when AWS is setup
    frontend_origin: str = "http://localhost:5173"

    seed_password: str | None = None

    #Tells pydantic-settings to actually read from backend/.env and fill these fields from it
    model_config = SettingsConfigDict(env_file=".env")


#without the .env file setting values , this will raise an error
settings = Settings()