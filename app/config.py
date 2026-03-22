from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Explicitly load the .env file
load_dotenv()

class Settings(BaseSettings):
    # These fields are required; if missing in .env, the app will raise an error
    DATABASE_URL: str
    SECRET_KEY: str
    
    # These fields have default values for easier development
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configure Pydantic to read from .env and ignore variables not defined here
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # This prevents the ValidationError when system vars exist
    )

# Instantiate settings once to be used throughout the application
settings = Settings()