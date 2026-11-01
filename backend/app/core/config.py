"""Application settings.

pydantic-settings reads values from environment variables (and an optional
.env file), validates their types, and exposes them as a typed object.
This keeps secrets out of the code: rule #3 in PLAN.md.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Sri Lanka Travel API"
    environment: str = "development"

    # Async SQLAlchemy URL. Inside Docker the host is the service name "db".
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tour_sri"

    # Comma-separated list of origins allowed to call the API from a browser.
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Create settings once and reuse them (cached)."""
    return Settings()


settings = get_settings()

