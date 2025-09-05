"""Service layer for Organization operations."""
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


def create_organization(db: Session, data: OrganizationCreate) -> Organization:
    org = Organization(name=data.name, description=data.description)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def get_organization(db: Session, org_id: int) -> Organization | None:
    return db.get(Organization, org_id)


def get_organization_with_relations(db: Session, org_id: int) -> Organization | None:
    """Load organization with related collections for detailed view."""
    stmt = (
        select(Organization)
        .options(
            selectinload(Organization.departments)
        )
        .where(Organization.id == org_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_organization_by_name(db: Session, name: str) -> Organization | None:
    stmt = select(Organization).where(Organization.name == name)
    return db.execute(stmt).scalar_one_or_none()


def list_organizations(db: Session, skip: int = 0, limit: int = 100) -> list[Organization]:
    stmt = select(Organization).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_organization(db: Session, org: Organization, data: OrganizationUpdate) -> Organization:
    if data.name is not None:
        org.name = data.name
    if data.description is not None:
        org.description = data.description
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def delete_organization(db: Session, org: Organization) -> None:
    db.delete(org)
    db.commit()
