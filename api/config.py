from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    google_api_key: str = ""
    supabase_url: str
    supabase_key: str
    llm_provider: Literal["anthropic", "google"] = "anthropic"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
