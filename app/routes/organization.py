"""Organization API routes.
Provides CRUD endpoints for organizations (and simple department listing later).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
    OrganizationWithRelations,
)
from app.services.organization_service import (
    create_organization,
    get_organization,
    get_organization_with_relations,
    list_organizations,
    get_organization_by_name,
    update_organization,
    delete_organization,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_org(payload: OrganizationCreate, db: Session = Depends(get_db)):
    # Ensure unique name
    existing = get_organization_by_name(db, payload.name)
    if existing:
        raise HTTPException(status_code=400, detail="Organization name already exists")
    org = create_organization(db, payload)
    return org


@router.get("/", response_model=list[OrganizationRead])
def list_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_organizations(db, skip=skip, limit=limit)


@router.get("/{org_id}", response_model=OrganizationRead)
def get_org(org_id: int, db: Session = Depends(get_db)):
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.put("/{org_id}", response_model=OrganizationRead)
def update_org(org_id: int, payload: OrganizationUpdate, db: Session = Depends(get_db)):
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    org = update_organization(db, org, payload)
    return org


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_org(org_id: int, db: Session = Depends(get_db)):
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    delete_organization(db, org)
    return None



@router.get("/{org_id}/detail", response_model=OrganizationWithRelations)
def get_org_detail(org_id: int, db: Session = Depends(get_db)):
    org = get_organization_with_relations(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
