"""
Enum types shared across the app

The benefits is that typos will be caught at compile
"""

from enum import Enum

#For cashcow enums will be: ATMStatus, ServicePriority, ServiceStatus, and later on UserRole (when RBAC is added)

class ATMStatus(str,Enum):
    OPERATIONAL = "Operational"
    IN_TRANSPORT = "In-Transport"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"

class ServicePriority(str,Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    CRITICAL = "Critical"

class ServiceStatus(str,Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class UserRole(str,Enum):
    OPERATIONS_ADMIN = "Operations Admin" #Everything
    FIELD_TECHNICIAN = "Field Technician" #Status changes and upload files
    AUDITOR = "Auditor" #Read only
