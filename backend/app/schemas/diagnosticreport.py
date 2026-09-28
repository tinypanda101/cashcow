"""
Diagnostic Report Schema
"""

import datetime

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
