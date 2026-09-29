"""
Service Call Schema
"""

from pydantic import BaseModel, ConfigDict, Field

from app.models import ServicePriority, ServiceStatus


class ServiceCallBase(BaseModel):
    title: str = Field(min_length = 2, max_length = 100)
    priority: ServicePriority = ServicePriority.MEDIUM
    status: ServiceStatus = ServiceStatus.PENDING
    atm_id: int
    technician_id: int

class ServiceCallCreate(ServiceCallBase):
    pass

class ServiceCallUpdate(BaseModel):
    id: int | None = None
    title: str | None= Field(default=None, min_length = 2, max_length = 100)
    priority: ServicePriority | None= None
    status: ServiceStatus |None= None
    atm_id: int | None
    technician_id: int | None
    model_config = ConfigDict(from_attributes=True)

class ServiceCallRead(ServiceCallBase):
    id: int

    model_config = ConfigDict(from_attributes=True)