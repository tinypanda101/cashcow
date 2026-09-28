"""
Technician Schema
"""

from pydantic import BaseModel, ConfigDict, Field

class TechnicianBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    branch_id: int

class TechnicianCreate(TechnicianBase):
    pass

class TechnicianUpdate(TechnicianBase):
    pass

class TechnicianRead(TechnicianBase):
    id: int

    model_config = ConfigDict(from_attributes=True)