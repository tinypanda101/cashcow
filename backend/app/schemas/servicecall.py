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
    title: str | None = Field(default=None, min_length=2, max_length=100)
    priority: ServicePriority | None = None
    status: ServiceStatus | None = None
    atm_id: int | None = None
    technician_id: int | None = None

class ServiceCallRead(ServiceCallBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class DiscrepancyRead(BaseModel):
    """
    Shape of the Response Body for Reading Location Discrepancies between ATMs and Field Technicians
    """
    servicecall_id: int
    title: str
    atm_branch_id: int
    technician_branch_id: int

    model_config = ConfigDict(from_attributes=True)

class CompletionRatio(BaseModel):
    """
    Shape of the Response Body for Reading Service Call Completion/Failure Ratios by ATM Model
    """
    model: str
    total_calls: int
    completed_count: int
    failed_count: int
    ratio: float | None
    
class ServiceCallStatusUpdate(BaseModel):
    status: ServiceStatus