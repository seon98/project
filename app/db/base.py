"""SQLAlchemy Declarative Base.
This module defines the Base class used by all ORM models.
Import all model modules here so Alembic's autogenerate can discover them.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models for metadata registration
# These imports ensure Base.metadata is aware of all tables
try:
    from app.models import organization, department, user, role  # noqa: F401
except Exception:
    # During some tooling or early import phases, models may not be available.
    # It's safe to ignore import errors here; runtime app and alembic will import them.
    pass
