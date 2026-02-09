"""Application configuration loaded from environment variables."""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings with env-var support."""

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"

    database_url: str = "sqlite+aiosqlite:///./jee_coach.db"

    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = True

    # CORS: comma-separated allowed origins (use "*" for dev, specific domain for prod)
    cors_origins: str = "*"

    syllabus_path: str = "data/syllabus.json"
    notes_dir: str = "data/notes"

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
