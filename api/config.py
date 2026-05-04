from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Literal
import os


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    google_api_key: str = ""
    supabase_url: str
    supabase_key: str
    llm_provider: Literal["anthropic", "google"] = "anthropic"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )


@lru_cache()
def get_settings():
    return Settings()
