"""Role API routes.
Provides CRUD endpoints for roles.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.services.role_service import (
    create_role,
    get_role,
    list_roles,
    get_role_by_name,
    update_role,
    delete_role,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role_ep(payload: RoleCreate, db: Session = Depends(get_db)):
    existing = get_role_by_name(db, payload.name)
    if existing:
        raise HTTPException(status_code=400, detail="Role name already exists")
    role = create_role(db, payload)
    return role


@router.get("/", response_model=list[RoleRead])
def list_roles_ep(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_roles(db, skip=skip, limit=limit)


@router.get("/{role_id}", response_model=RoleRead)
def get_role_ep(role_id: int, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleRead)
def update_role_ep(role_id: int, payload: RoleUpdate, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role = update_role(db, role, payload)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_ep(role_id: int, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    delete_role(db, role)
    return None
