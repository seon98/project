"""Database engine and session configuration.
Creates SQLAlchemy engine from settings and provides SessionLocal factory.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # Needed for SQLite when using threads (e.g., FastAPI with uvicorn reload)
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, echo=settings.SQLALCHEMY_ECHO, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
