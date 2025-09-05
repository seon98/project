"""Service layer for Role operations."""
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


def create_role(db: Session, data: RoleCreate) -> Role:
    role = Role(name=data.name, description=data.description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role(db: Session, role_id: int) -> Role | None:
    return db.get(Role, role_id)


def get_role_by_name(db: Session, name: str) -> Role | None:
    stmt = select(Role).where(Role.name == name)
    return db.execute(stmt).scalar_one_or_none()


def list_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
    stmt = select(Role).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_role(db: Session, role: Role, data: RoleUpdate) -> Role:
    if data.name is not None:
        role.name = data.name
    if data.description is not None:
        role.description = data.description
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role: Role) -> None:
    db.delete(role)
    db.commit()
