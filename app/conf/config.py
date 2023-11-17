from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    environment: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.prod", env_prefix="DB_")
    dsn: str
    database: str
    collection: str

class DevelopmentDatabaseSettings(DatabaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev", env_prefix="DB_")
    dsn: str
    database: str
    collection: str

@lru_cache(maxsize=None)
def get_database_settings():
    settings = Settings()
    if settings.environment == "development":
        return DevelopmentDatabaseSettings()
    elif settings.environment == "production":
        return DatabaseSettings()
    else:
        raise ValueError(f"Invalid environment name ('{settings.environment}').")
