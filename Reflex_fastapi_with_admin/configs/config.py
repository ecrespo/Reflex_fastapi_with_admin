from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from Reflex_fastapi_with_admin.utils.LoggerSingleton import logger


class Settings(BaseSettings):
    # Define the attributes of the Settings class
    DATABASE_FILE: str
    ENGINE_URI: str
    SECRET: str

    # Load the settings from the .env file
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    """
        This function returns an instance of the Settings class.
        It uses the lru_cache decorator to cache the result,
        so that subsequent calls do not have to re-instantiate the Settings class.
    """
    return Settings()


# Get the settings
settings = get_settings()

# Assign the settings to variables
DATABASE_FILE = settings.DATABASE_FILE
ENGINE_URI = settings.ENGINE_URI
SECRET = settings.SECRET
# Log that the settings have been loaded
logger.info("Settings loaded")
