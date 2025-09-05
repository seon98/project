from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Department(Base):
    """Department entity belonging to an Organization.
    Supports hierarchical parent-child relationships (e.g., divisions/teams).
    """

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="departments")
    parent: Mapped[Optional["Department"]] = relationship(remote_side="Department.id", back_populates="children")
    children: Mapped[List["Department"]] = relationship(back_populates="parent")
    users: Mapped[List["User"]] = relationship(back_populates="department")


# Note: Relationships use string-based references to avoid circular imports.
