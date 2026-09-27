"""
Service Call Model
"""

#imports
#need __future__ stuff, TYPE_CHECKING, sqlAlchemy, .base
from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
#"as" renames it to avoid conflicts with other Enums
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .enums import ServicePriority, ServiceStatus

if TYPE_CHECKING:
    #import the foreignkey models
    from atm import ATM
    from technicians import Technician
    from diagnosticreport import DiagnosticReport

#model itself
class ServiceCall(Base):
    __tablename__ = "service_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    #enum so its different
    priority: Mapped[ServicePriority] = mapped_column(
        SQLEnum(ServicePriority, name = "service_priority", values_callable=lambda obj: [e.value for e in obj]),
    )
    status: Mapped[ServiceStatus] = mapped_column(
        SQLEnum(ServiceStatus, name = "service_status", values_callable=lambda obj: [e.value for e in obj]),
    )
    atm_id: Mapped[int] = mapped_column(Integer, ForeignKey("atms.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))

    #Relationships
    #relationships are put on both sides for any connections, ie this side only has atm and technicains but diagnosticreport needs service call id so it also needs a relationship
    #The "one" side of the one to many will be singular, the "many" side will be plural
    #ie for every ATM, there can be multiple service calls
    atm : Mapped["ATM"] = relationship(back_populates="service_calls")
    #for every technician, there can be multiple service calls
    technician : Mapped["Technician"] = relationship(back_populates="service_calls")

    #For every service call there can be multiple diagnostic reports which makes this one different than the ones above because now the service call is the "one" side of the relationship
    #notice how diagnosticreport is a list and service_call is singular
    diagnostic_reports: Mapped[list["DiagnosticReport"]] = relationship(back_populates="service_call")


    #functions
    #stuff like the __repr__ (tostring), and then the base functions to answer the questions
    def __repr__(self) -> str:
        return f"<ServiceCall(id={self.id}, title='{self.title!r}', priority={self.priority.value}, status={self.status.value}, atm_id={self.atm_id}, technician_id={self.technician_id})>"

    #mark completed, failed, etc will be put here later
