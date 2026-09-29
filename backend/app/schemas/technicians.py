"""
Technician Schema
"""

from pydantic import BaseModel, ConfigDict, Field

class TechnicianBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    branch_id: int

class TechnicianCreate(TechnicianBase):
    pass

class TechnicianUpdate(BaseModel):
    id: int | None = None
    name: str | None = Field(default=None, min_length=2, max_length=100)
    branch_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

class TechnicianRead(TechnicianBase):
    id: int

    model_config = ConfigDict(from_attributes=True)