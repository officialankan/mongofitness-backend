from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")
    environment: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="DB_")
    dsn: str
    database: str
    collection: str

@lru_cache(maxsize=None)
def get_database_settings():
    return DatabaseSettings()

@lru_cache(maxsize=None)
def get_settings():
    return Settings()
