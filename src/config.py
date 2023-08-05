import secrets
from typing import Any, Optional
from pydantic import AnyUrl, BaseSettings, validator


class PostgresDsn(AnyUrl):
    allowed_schemes = {"postgresql+psycopg2",
                       "postgresql", "postgresql+asyncpg"}
    user_required = True


class Settings(BaseSettings):
    POSTGRES_SERVER: str = "0.0.0.0"
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "postgres"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USERNAME"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"


settings = Settings()
