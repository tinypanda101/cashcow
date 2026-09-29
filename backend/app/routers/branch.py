"""
Branch Router and Related Endpoints
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.schemas.branch import BranchCreate, BranchRead, BranchUpdate
from app.models import Branch, User, UserRole

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