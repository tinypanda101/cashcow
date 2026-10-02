"""
Technician Router and Related Endpoints
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.schemas.technicians import TechnicianRead,TechnicianCreate, TechnicianUpdate
from app.models import Technician, User, UserRole

router = APIRouter(prefix="/technician", tags=["Technician"])


#Get all
@router.get("/", response_model=list[TechnicianRead])
async def list_technicians(
    db: AsyncSession = Depends(get_db),
    
    _: User = Depends(get_current_user),
) -> list[Technician]:
    statement = select(Technician)
    statement = statement.order_by(Technician.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

#Get by id
@router.get("/{technician_id}", response_model=TechnicianRead)
async def get_technician(
    technician_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Technician:
    statement =  await db.get(Technician, technician_id)
    if statement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Technician not found with the ID {technician_id}",
            )
    return statement

#Create tech
@router.post("/", response_model=TechnicianRead)
async def create_technician(
    technician_data: TechnicianCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> Technician:
    technician = Technician(**technician_data.model_dump())
    db.add(technician)
    await db.commit()
    await db.refresh(technician)
    return technician


#Update tech
@router.put("/{technician_id}", response_model=TechnicianRead)
async def update_technician(
    technician_id: int,
    technician_data: TechnicianUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> Technician:
    technician = await db.get(Technician, technician_id)
    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Technician not found with the ID {technician_id}"
        )
    for key, value in technician_data.model_dump(exclude_unset=True).items():
        setattr(technician, key, value)
    await db.commit()
    await db.refresh(technician)
    return technician

#Delete tech
@router.delete("/{technician_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technician(
    technician_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
):
    technician = await db.get(Technician, technician_id)
    if technician is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Technician not found with the ID {technician_id}",
        )
    await db.delete(technician)
    await db.commit()
    return None