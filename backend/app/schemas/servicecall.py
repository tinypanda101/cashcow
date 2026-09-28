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

class ServiceCallUpdate(ServiceCallBase):
    pass

class ServiceCallRead(ServiceCallBase):
    id: int

    model_config = ConfigDict(from_attributes=True)