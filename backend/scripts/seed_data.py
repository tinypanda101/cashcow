"""
Some seed data for the app so we can test things

To run: \backend
python -m scripts.seed_data.py
"""

import asyncio

from app.database import AsyncSessionLocal
from app.models import User,Branch, Technician, ServiceCall, ATM, DiagnosticReport
from app.models import UserRole, ServicePriority, ServiceStatus, ATMStatus
from app.security import hash_password

# Seeds user data
async def seed_users():
    async with AsyncSessionLocal() as session:
        session.add_all([
            User(username = "admin", hash_password = hash_password("admin123"), role = UserRole.OPERATIONS_ADMIN),
            User(username = "tech", hash_password = hash_password("tech123"), role = UserRole.FIELD_TECHNICIAN),
            User(username = "auditor", hash_password = hash_password("auditor123"), role = UserRole.AUDITOR),
            
        ])
        session.add_all([
            #Branches
            Branch(name = "Tampa Branch", location_region = "Florida", capacity = 100, supervisor_id = 1),
            Branch(name = "Orlando Branch", location_region = "Florida", capacity = 100, supervisor_id = 1),
            Branch(name = "New York Branch", location_region = "New York", capacity = 200, supervisor_id = 1),
            Branch(name = "Houston Branch", location_region = "Texas", capacity = 150, supervisor_id = 1),
        
            #Technicians
            Technician(name = "John Doe", branch_id = 1),
            Technician(name = "Jane Smith", branch_id = 2),
            Technician(name = "Bob Johnson", branch_id = 3),
            Technician(name = "Alice Brown", branch_id = 4),
        
        
            #ATMs #cash_level is percentage
            ATM(serial_number = "ATM-001", model = "CashNow!", status = ATMStatus.MAINTENANCE, cash_level = 5, branch_id = 1),
            ATM(serial_number = "ATM-002", model = "CashNow!", status = ATMStatus.OPERATIONAL, cash_level = 30, branch_id = 2),
            ATM(serial_number = "MON-201", model = "SpeedyCash", status = ATMStatus.OFFLINE, cash_level = 10, branch_id = 3),
            ATM(serial_number = "MON-202", model = "SpeedyCash", status = ATMStatus.IN_TRANSPORT, cash_level = 80, branch_id = 4),
        
        
            #Service Calls
            ServiceCall(title = "Low on Cash", priority = ServicePriority.MEDIUM, status = ServiceStatus.IN_PROGRESS, atm_id = 1, technician_id = 2),
            ServiceCall(title = "Keypad Issue", priority = ServicePriority.CRITICAL, status = ServiceStatus.PENDING, atm_id = 2, technician_id = 1),
            ServiceCall(title = "Power Outage", priority = ServicePriority.CRITICAL, status = ServiceStatus.FAILED, atm_id = 3, technician_id = 4),
            ServiceCall(title = "Low on Cash", priority = ServicePriority.MEDIUM, status = ServiceStatus.COMPLETED, atm_id = 4, technician_id = 3),
        
            #Diagnostic Reports
            DiagnosticReport(service_call_id = 1, file_url = "http://example.com/report1.pdf", notes = "Low cash level detected"),
            DiagnosticReport(service_call_id = 2, file_url = "http://example.com/report2.pdf", notes = "Keypad malfunction"),
            DiagnosticReport(service_call_id = 3, file_url = "http://example.com/report3.pdf", notes = "Power outage reported, can't fix on our side"),
            DiagnosticReport(service_call_id = 4, file_url = "http://example.com/report4.pdf", notes = "Cash level restored, sending back"),
                    
        ])
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_users())
   
