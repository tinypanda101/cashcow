"""
Service Call Router and Related Endpoints
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, case, func, cast, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.schemas.servicecall import DiscrepancyRead, ServiceCallCreate, ServiceCallUpdate, ServiceCallRead, CompletionRatio, ServiceCallStatusUpdate
from app.models import ServiceCall, User, UserRole, ATM, ServicePriority, Technician, ServiceStatus

router = APIRouter(prefix="/service_calls", tags=["service_calls"])


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

#Question 2: How many ATMs are assigned to field technicians who are NOT co-located at the same physical branch?
@router.get("/discrepancies", response_model=list[DiscrepancyRead])
async def get_colocation_discrepancies(
    priority: ServicePriority | None = Query(
        default = None,
        description = "Only return discrepancies for the specified priority",
    ),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[DiscrepancyRead]:

    statement = (
        select(
            ServiceCall.id.label("servicecall_id"),
            ServiceCall.title,
            ATM.branch_id.label("atm_branch_id"),
            Technician.branch_id.label("technician_branch_id"),
        )
        .join(ATM, ServiceCall.atm_id == ATM.id)
        .join(Technician, ServiceCall.technician_id == Technician.id)
        .where(ATM.branch_id != Technician.branch_id)
    )

    #if filter was provided:
    if priority is not None:
        statement = statement.where(ServiceCall.priority == priority)

    statement = statement.order_by(ServiceCall.id)

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

#Question 3: What is the service call completion/failure ratio broken down by ATM model?
@router.get("/completion_ratio", response_model=list[CompletionRatio])
async def get_completion_ratio(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    completed = func.sum(case((ServiceCall.status == ServiceStatus.COMPLETED, 1), else_=0)).label("completed_count")
    failed = func.sum(case((ServiceCall.status == ServiceStatus.FAILED, 1), else_=0)).label("failed_count")

    statement = (
        select(
            ATM.model,
            func.count(ServiceCall.id).label("total_calls"),
            completed.label("completed_count"),
            failed.label("failed_count"),
            func.round(cast(completed,Numeric) / func.nullif(completed + failed, 0), 2).label("ratio"),
        )
        .join(ATM, ServiceCall.atm_id == ATM.id)
        .group_by(ATM.model)
        .order_by(ATM.model)
    )

    result = await db.execute(statement)
    return [dict(row) for row in result.mappings().all()]

@router.patch("/{service_call_id}/status", response_model=ServiceCallRead)
async def update_service_call_status(
    service_call_id: int,
    payload: ServiceCallStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.OPERATIONS_ADMIN, UserRole.FIELD_TECHNICIAN)
    ),
) -> ServiceCall:
    service_call = await db.get(ServiceCall, service_call_id)
    if service_call is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"ServiceCall not found with the ID {service_call_id}")

    # Technicians may only change calls assigned to them
    if current_user.role == UserRole.FIELD_TECHNICIAN:
        tech = await db.scalar(
            select(Technician).where(Technician.user_id == current_user.id)
        )
        if tech is None or service_call.technician_id != tech.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                "You can only update service calls assigned to you")

    service_call.status = payload.status
    await db.commit()
    await db.refresh(service_call)
    return service_call



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

#Create
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


#Update 
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

#Delete
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



