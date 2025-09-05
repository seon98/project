from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Organization(Base):
    """Organization entity representing a company/hospital/public institution."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    departments: Mapped[List["Department"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    users: Mapped[List["User"]] = relationship(back_populates="organization")


# Note: Relationships use string-based references to avoid circular imports.
