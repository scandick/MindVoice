"""Configuration loader using environment variables."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Project settings loaded from .env file."""

    TELEGRAM_TOKEN: str  # TODO: Insert your Telegram bot token here
    OPENAI_API_KEY: str  # TODO: Insert your OpenAI API key here
    PAYMENT_PROVIDER_TOKEN: str  # TODO: Payment provider token for Telegram Payments
    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    FREE_TRIAL_DAYS: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
