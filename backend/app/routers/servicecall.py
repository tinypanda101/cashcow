"""
Service Call Router and Related Endpoints
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.schemas.servicecall import ServiceCallCreate, ServiceCallUpdate, ServiceCallRead
from app.models import ServiceCall, User, UserRole

router = APIRouter(prefix="/service-calls", tags=["service_calls"])


#Get all
@router.get("/", response_model=list[ServiceCallRead])
async def list_ServiceCalls(
    db: AsyncSession = Depends(get_db),
    
    _: User = Depends(get_current_user),
) -> list[ServiceCall]:
    statement = select(ServiceCall)
    statement = statement.order_by(ServiceCall.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

#Get by id
@router.get("/{ServiceCall_id}", response_model=ServiceCallRead)
async def get_ServiceCall(
    ServiceCall_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ServiceCall:
    statement =  await db.get(ServiceCall, ServiceCall_id)
    if statement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ServiceCall not found with the ID {ServiceCall_id}",
            )
    return statement

#Create tech
@router.post("/", response_model=ServiceCallRead)
async def create_ServiceCall(
    ServiceCall_data: ServiceCallCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> ServiceCall:
    serviceCall = ServiceCall(**ServiceCall_data.model_dump())
    db.add(serviceCall)
    await db.commit()
    await db.refresh(serviceCall)
    return serviceCall


#Update tech
@router.post("/{ServiceCall_id}", response_model=ServiceCallRead)
async def update_ServiceCall(
    ServiceCall_id: int,
    ServiceCall_data: ServiceCallUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> ServiceCall:
    serviceCall = await db.get(ServiceCall, ServiceCall_id)
    if not serviceCall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ServiceCall not found with the ID {ServiceCall_id}"
        )
    for key, value in ServiceCall_data.model_dump(exclude_unset=True).items():
        setattr(serviceCall, key, value)
    await db.commit()
    await db.refresh(serviceCall)
    return serviceCall

#Delete tech
@router.delete("/{ServiceCall_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ServiceCall(
    ServiceCall_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
):
    serviceCall = await db.get(ServiceCall, ServiceCall_id)
    if serviceCall is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ServiceCall not found with the ID {ServiceCall_id}",
        )
    await db.delete(serviceCall)
    await db.commit()
    return None