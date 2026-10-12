from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Loaded from environment variables / .env. Values come from
    https://my.telegram.org -> API development tools.
    """

    model_config = SettingsConfigDict(env_file=PROJECT_DIR / ".env", env_file_encoding="utf-8")

    telegram_api_id: int
    telegram_api_hash: str
    telegram_session_path: Path = PROJECT_DIR / "state" / "session"


def get_settings() -> Settings:
    settings = Settings()  # type: ignore[call-arg]  # fields come from env/.env, not kwargs
    settings.telegram_session_path.parent.mkdir(parents=True, exist_ok=True)
    return settings
