from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class RoleRead(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
