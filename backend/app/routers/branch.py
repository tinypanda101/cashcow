"""
Branch Router and Related Endpoints
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.schemas.branch import BranchCreate, BranchRead, BranchUpdate, MaintenanceFlag, SupervisorCheck, TechnicianActiveCalls
from app.models import Branch, User, UserRole, ATM, ATMStatus, Technician, ServiceCall, ServiceStatus


router = APIRouter(prefix="/branch", tags=["Branch"])

#GET
@router.get("/", response_model=list[BranchRead])
async def list_branches(
    db: AsyncSession = Depends(get_db),
    
    _: User = Depends(get_current_user),
) -> list[Branch]:
    statement = select(Branch)
    statement = statement.order_by(Branch.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

#Question 4: Which branches have more than 30% of their ATMs currently flagged for maintenance?
@router.get("/maintenance", response_model=list[MaintenanceFlag])
async def maintenance_flags(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    maintenance_count = func.sum(case((ATM.status == ATMStatus.MAINTENANCE, 1), else_=0))
    total_atms = func.count(ATM.id)
    maintenance_percentage = maintenance_count * 100 / total_atms

    statement = (
        select(
            Branch.id.label("branch_id"),
            Branch.name.label("branch_name"),
            total_atms.label("total_atms"),
            maintenance_count.label("maintenance_count"),
            maintenance_percentage.label("maintenance_percentage")
        )
        .join(ATM, ATM.branch_id == Branch.id)
        .group_by(Branch.id, Branch.name)
        .having(maintenance_percentage > 30)
        .order_by(Branch.id)
    )
    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

#Quesation 5: How many technicians reporting to a specific Regional Operations Supervisor have active service calls assigned to them?
@router.get("/supervisor", response_model=SupervisorCheck)
async def regional_supervisor_check(
    supervisor_id: int = Query(..., description = "Regional Supervisor's ID (Branch.supervisor_id)."),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    statement = (
        select(
            Technician.id.label("technician_id"),
            Technician.name.label("technician_name"),
            func.count(ServiceCall.id).label("active_mission_count"),
        )
        .join(Branch, Branch.id == Technician.branch_id)
        .join(ServiceCall, ServiceCall.technician_id == Technician.id)
        .where(
            Branch.supervisor_id == supervisor_id,
            ServiceCall.status.in_([ServiceStatus.PENDING, ServiceStatus.IN_PROGRESS])
        )
        .group_by(Technician.id, Technician.name)
        .order_by(Technician.id)
    )
    result = await db.execute(statement)
    technicians = [TechnicianActiveCalls(**row) for row in result.mappings().all()]

    return SupervisorCheck(
        supervisor_id=supervisor_id,
        technician_count=len(technicians),
        technician=technicians,
    )


#Get by id
@router.get("/{branch_id}", response_model=BranchRead)
async def get_branch(
    branch_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Branch:
    statement =  await db.get(Branch, branch_id)
    if statement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch not found with the ID {branch_id}",
            )
    return statement

#Create a new branch
@router.post("/", response_model=BranchRead)
async def create_branch(
    branch_data: BranchCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> Branch:
    branch = Branch(**branch_data.model_dump())
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch

#Updates a brnach (only admin like the others)
@router.post("/{branch_id}", response_model=BranchRead)
async def update_branch(
    branch_id: int,
    branch_data: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> Branch:
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch not found with the ID {branch_id}"
        )
    for key, value in branch_data.model_dump(exclude_unset=True).items():
        setattr(branch, key, value)
    await db.commit()
    await db.refresh(branch)
    return branch

#Delete a branch
@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch(
    branch_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
):
    branch = await db.get(Branch, branch_id)
    if branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Branch not found with the ID {branch_id}",
        )
    await db.delete(branch)
    await db.commit()
    return None