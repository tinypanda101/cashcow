"""
Diagnostic Report Schema
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class DiagnosticReportBase(BaseModel):
    file_url: str
    notes: str
    timestamp: datetime

class DiagnosticReportCreate(DiagnosticReportBase):
    pass

class DiagnosticReportRead(DiagnosticReportBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class DiagnosticReportUpdate(BaseModel):
    id: int | None = None
    file_url: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)
