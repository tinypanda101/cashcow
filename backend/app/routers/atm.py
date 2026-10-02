"""
Endpoints for ATM related things
"""


from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.atm import ATMRead, ATMCreate, ATMUpdate
from app.dependencies import get_db, get_current_user, require_role
from app.models import ATM, ATMStatus, User, UserRole

#step 1: set up the router for endpoints
router = APIRouter(prefix="/atm", tags=["atm"])

#step 2: define the endpoints
#"" is what gets added to the url so /atm/"", response_model is one of the schemas we made


#Read all ATms and also can answer Question 1
@router.get("", response_model=list[ATMRead])
async def list_atms(
    #add a filter for cash level
    max_cash: Decimal | None = Query(
        default = None,
        ge = 0,
        le = 100,
        description = "Returns robots under this cash percentage"
    ),
    db: AsyncSession = Depends(get_db),

    _: User = Depends(get_current_user),
) -> list[ATM]:
    """
    Buisness question 1: Which active ATMs are operating below a 20% cash reserve across all branches?
    """

    statement = select(ATM)
    if max_cash is not None:
        statement = statement.where(ATM.cash_level < max_cash).where(ATM.status == ATMStatus.OPERATIONAL)
    statement = statement.order_by(ATM.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

#Get a specific ATM by ID
@router.get("/{atm_id}", response_model=ATMRead)
async def get_atm(
    atm_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ATM:
    statement =  await db.get(ATM, atm_id)
    if statement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ATM not found with the ID {atm_id}",
            )
    return statement

#Creates a new ATM (Only Admin can do this)
@router.post("", response_model = ATMRead, status_code= status.HTTP_201_CREATED)
async def create_atm(
    payload: ATMCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> ATM:
    atm = ATM(**payload.model_dump())
    db.add(atm)
    await db.commit()
    await db.refresh(atm)
    return atm

#Updates an existing ATM (Only Admin can do this)
@router.put("/{atm_id}", response_model = ATMRead)
async def update_atm(
    atm_id: int,
    payload: ATMUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> ATM:
    statement = await db.get(ATM, atm_id)
    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ATM not found with the ID {atm_id}"
        )
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(statement, key, value)

    await db.commit()
    await db.refresh(statement)
    return statement

#Deletes an existing ATM (Only Admin can do this)
@router.delete("/{atm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_atm(
    atm_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
):
    statement = await db.get(ATM, atm_id)
    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ATM not found with the ID {atm_id}"
        )
    await db.delete(statement)
    await db.commit()
    return None

