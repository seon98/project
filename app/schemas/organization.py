from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# ========== Department Schemas ==========
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Department name")
    organization_id: int | None = None
    parent_id: int | None = None


class DepartmentCreate(DepartmentBase):
    organization_id: int


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    parent_id: Optional[int] = None


class DepartmentRead(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ========== Organization Schemas ==========
class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Organization name")
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None


class OrganizationRead(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class OrganizationWithRelations(OrganizationRead):
    departments: List[DepartmentRead] = []
