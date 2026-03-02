"""Application settings via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from env. DATABASE_URL must use asyncpg: postgresql+asyncpg://..."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        extra="ignore",
    )

    BOT_TOKEN: str
    DATABASE_URL: str  # async URL, e.g. postgresql+asyncpg://user:pass@host:port/db
    SECRET_KEY: str
    MINI_APP_URL: str = "https://t.me/your_bot/app"  # WebApp URL for /start button
    ENV: str = "dev"
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    INIT_DATA_MAX_AGE_MINUTES: int = 10
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    RATE_LIMIT_SEARCH_REQUESTS: int = 30
    RATE_LIMIT_APPLY_REQUESTS: int = 10
    PAGINATION_MAX_LIMIT: int = 50
    LOG_JSON: bool = False
    LOG_LEVEL: str = "INFO"

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """
        Synchronous URL for Alembic.

        If DATABASE_URL uses +asyncpg, swap to +psycopg; otherwise return as is.
        """
        url = self.DATABASE_URL
        if "+asyncpg" in url:
            return url.replace("+asyncpg", "+psycopg")
        return url


settings = Settings()
