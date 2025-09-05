"""Service layer for User operations."""
from hashlib import sha256
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def _hash_password(raw: str) -> str:
    # NOTE: For real applications use passlib/bcrypt or Argon2. This is for demo/testing only.
    return sha256(raw.encode("utf-8")).hexdigest()


def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=_hash_password(data.password),
        is_active=data.is_active,
        organization_id=data.organization_id,
        department_id=data.department_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.is_active is not None:
        user.is_active = data.is_active
    if data.department_id is not None:
        user.department_id = data.department_id
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
