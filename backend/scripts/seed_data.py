"""
Seed data for the app. Safe to run more than once.
 
To run: bash bin/seed.sh [--reset] [--yes]
"""
 
import argparse
import asyncio
import sys
 
from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
 
try:
    from app.config import settings
except ValidationError as e:
    missing = ", ".join(str(err["loc"][0]).upper() for err in e.errors())
    sys.exit(f"ERROR: Missing settings: {missing}. Set them in backend/.env")
 
from app.models import Base, User, Branch, Technician, ATM, ServiceCall, DiagnosticReport
from app.models import UserRole, ATMStatus, ServicePriority, ServiceStatus
from app.security import hash_password
 
 
BRANCHES = [
    Branch(id=1, name="Tampa Branch", location_region="Florida", capacity=100, supervisor_id=1),
    Branch(id=2, name="Orlando Branch", location_region="Florida", capacity=100, supervisor_id=1),
    Branch(id=3, name="New York Branch", location_region="New York", capacity=200, supervisor_id=1),
    Branch(id=4, name="Houston Branch", location_region="Texas", capacity=150, supervisor_id=1),
]
 
TECHNICIANS = [
    Technician(id=1, name="John Doe", branch_id=1),
    Technician(id=2, name="Jane Smith", branch_id=2),
    Technician(id=3, name="Bob Johnson", branch_id=3),
    Technician(id=4, name="Alice Brown", branch_id=4),
]
 
ATMS = [
    ATM(id=1, serial_number="ATM-001", model="CashNow!", status=ATMStatus.MAINTENANCE, cash_level=5, branch_id=1),
    ATM(id=2, serial_number="ATM-002", model="CashNow!", status=ATMStatus.OPERATIONAL, cash_level=30, branch_id=2),
    ATM(id=3, serial_number="MON-201", model="SpeedyCash", status=ATMStatus.OFFLINE, cash_level=10, branch_id=3),
    ATM(id=4, serial_number="MON-202", model="SpeedyCash", status=ATMStatus.IN_TRANSPORT, cash_level=80, branch_id=4),
]
 
SERVICE_CALLS = [
    ServiceCall(id=1, title="Low on Cash", priority=ServicePriority.MEDIUM, status=ServiceStatus.IN_PROGRESS, atm_id=1, technician_id=2),
    ServiceCall(id=2, title="Keypad Issue", priority=ServicePriority.CRITICAL, status=ServiceStatus.PENDING, atm_id=2, technician_id=1),
    ServiceCall(id=3, title="Power Outage", priority=ServicePriority.CRITICAL, status=ServiceStatus.FAILED, atm_id=3, technician_id=4),
    ServiceCall(id=4, title="Low on Cash", priority=ServicePriority.MEDIUM, status=ServiceStatus.COMPLETED, atm_id=4, technician_id=3),
]
 
DIAGNOSTIC_REPORTS = [
    DiagnosticReport(id=1, service_call_id=1, file_url="http://example.com/report1.pdf", notes="Low cash level detected"),
    DiagnosticReport(id=2, service_call_id=2, file_url="http://example.com/report2.pdf", notes="Keypad malfunction"),
    DiagnosticReport(id=3, service_call_id=3, file_url="http://example.com/report3.pdf", notes="Power outage reported, can't fix on our side"),
    DiagnosticReport(id=4, service_call_id=4, file_url="http://example.com/report4.pdf", notes="Cash level restored, sending back"),
]
 
USERS = [
    (1, "admin", UserRole.OPERATIONS_ADMIN),
    (2, "tech", UserRole.FIELD_TECHNICIAN),
    (3, "auditor", UserRole.AUDITOR),
]
 
TABLES = ["users", "branches", "technicians", "atms", "service_calls", "diagnostic_reports"]
 
 
async def check_connection(engine):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        if isinstance(e, DBAPIError) and e.__cause__ and e.__cause__.__cause__:
            e = e.__cause__.__cause__
        sys.exit(f"ERROR: Cannot connect to the database ({type(e).__name__}). "
                 "Check DATABASE_URL and that Postgres is running.")
 
 
async def seed(engine, reset):
    Session = async_sessionmaker(engine, expire_on_commit=False)
 
    async with Session() as session:
        conn = await session.connection()
        await conn.run_sync(Base.metadata.create_all)
 
        if reset:
            await session.execute(text(f"TRUNCATE {', '.join(TABLES)} RESTART IDENTITY CASCADE"))
 
        password_hash = hash_password(settings.seed_password)
        for user_id, username, role in USERS:
            existing = await session.scalar(select(User).where(User.username == username))
            if existing is None:
                session.add(User(id=user_id, username=username, hash_password=password_hash, role=role, is_active=True))
 
        for row in BRANCHES + TECHNICIANS + ATMS + SERVICE_CALLS + DIAGNOSTIC_REPORTS:
            await session.merge(row)
 
        # Seed rows use fixed ids, so move each id counter past them for new rows made in the app
        for table in TABLES:
            await session.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE(MAX(id), 0) + 1, false) FROM {table}"
            ))
 
        await session.commit()
 
 
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="delete ALL data, then reseed")
    parser.add_argument("--yes", action="store_true", help="skip the --reset confirmation")
    args = parser.parse_args()
 
    if not settings.seed_password or len(settings.seed_password) < 8:
        sys.exit("ERROR: SEED_PASSWORD must be set in backend/.env (8+ characters)")
 
    try:
        engine = create_async_engine(settings.database_url, connect_args={"timeout": 10})
    except Exception as e:
        sys.exit(f"ERROR: DATABASE_URL is not valid ({type(e).__name__})")
 
    try:
        await check_connection(engine)
 
        if args.reset and not args.yes:
            try:
                answer = input("This deletes ALL data in every table. Type 'reset' to continue: ")
            except EOFError:
                answer = ""
            if answer != "reset":
                sys.exit("Reset cancelled. Nothing was changed.")
 
        await seed(engine, args.reset)
        print("Seed complete.")
    except Exception as e:
        if isinstance(e, DBAPIError):
            e = e.orig
        sys.exit(f"ERROR: Seeding failed, nothing was saved. ({str(e).splitlines()[0]})")
    finally:
        await engine.dispose()
 
 
if __name__ == "__main__":
    asyncio.run(main())
 
