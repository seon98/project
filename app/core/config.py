"""Application configuration using environment variables.
Supports SQLite by default and easily switchable to PostgreSQL.
"""
from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    # Application metadata for OpenAPI
    APP_NAME: str = "ERP Backend"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = (
        "ERP system skeleton for public institutions and hospitals using FastAPI, "
        "SQLAlchemy, and Alembic."
    )

    # Database URL: default to local SQLite file
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./erp.db" if os.getenv("GITHUB_ACTIONS") is None else "sqlite:///:memory:"
    )

    # If using SQLite, we need check_same_thread=False
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
