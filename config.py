from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# This line tells Python to look for the .env file
load_dotenv()

class Settings(BaseSettings):
    # These names must match exactly what you wrote in the .env file
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        env_file = ".env"

# We create one 'settings' object to use everywhere
settings = Settings()