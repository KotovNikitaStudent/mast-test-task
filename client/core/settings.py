from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    PAGINATION_LIMIT: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def server_url(self) -> str:
        return f"http://{self.APP_HOST}:{self.APP_PORT}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
