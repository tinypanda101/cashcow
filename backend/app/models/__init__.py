"""
Lets us write:
from app.models import Robot,Facility
instead of 
from app.models.robot import Robot
from app.models.facility imnport Facility
"""

from .enums import *
from .atm import ATM
from .branch import Branch
from .diagnosticreport import DiagnosticReport
from .servicecall import ServiceCall
from .technicians import Technician
from .user import User
from .base import Base

__all__ = [
    "Base",
    "ServiceStatus", "ServicePriority", "UserRole", "ATMStatus",
    "ATM", "Branch", "DiagnosticReport", "ServiceCall", "Technician", "User"
]