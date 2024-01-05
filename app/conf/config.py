from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")
    dsn: str
    database: str

@lru_cache(maxsize=None)
def get_database_settings():
        return DatabaseSettings()
