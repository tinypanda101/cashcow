"""
Diagnostic Reports Model

This is connected to Service Call, For every Service Call, there can be at least one Diagnostic Report.
"""

#Need annotations from future and typechecking from typing
from __future__ import annotations
#Need datatime due to file uploads wanting timestamp
from datetime import datetime
from typing import TYPE_CHECKING

#Need sqlAlchemy stuff
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

#need base
from .base import Base

if TYPE_CHECKING:
    #import the foreignkey models
    #Should just be servicecall
    from servicecall import ServiceCall

class DiagnosticReport(Base):
    __tablename__ = "diagnostic_reports"

    #model
    id: Mapped[int] = mapped_column(primary_key=True)
    service_call_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_calls.id"))
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    #server_default = func.now() sets the default value of the created_at column to the current timetamp when a new record is inserted into database
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    #relationships
    #For every Service Call, there can be multiple Diagnostic Reports so Service is 1 and Diagnostic is many
    service_call: Mapped["ServiceCall"] = relationship(back_populates="diagnostic_reports")

    #functions
    def __repr__(self):
        return f"<DiagnosticReport(id={self.id}, service_call_id={self.service_call_id}, file_url={self.file_url!r})>"
    
