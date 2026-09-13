from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env.
    """

    openai_api_key: str

    openai_model: str = "gpt-5.6-luna"
    openai_embedding_model: str = "text-embedding-3-small"

    database_url: str = (
        f"sqlite:///{PROJECT_ROOT / 'data' / 'enterprise.db'}"
    )

    knowledge_base_dir: str = str(
        PROJECT_ROOT / "data" / "knowledge_base"
    )

    faiss_index_dir: str = str(
        PROJECT_ROOT / "data" / "index"
    )

    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached application settings instance.
    """
    return Settings()


settings = get_settings()