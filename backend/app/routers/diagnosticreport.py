"""
Diagnostic Report Router and Related Endpoints
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.schemas.diagnosticreport import DiagnosticReportRead, DiagnosticReportUpdate, DiagnosticReportCreate
from app.models import DiagnosticReport, User, UserRole

router = APIRouter(prefix="/diagnostic-reports", tags=["diagnostic_reports"])


#Get all
@router.get("/", response_model=list[DiagnosticReportRead])
async def list_DiagnosticReports(
    db: AsyncSession = Depends(get_db),
    
    _: User = Depends(get_current_user),
) -> list[DiagnosticReport]:
    statement = select(DiagnosticReport)
    statement = statement.order_by(DiagnosticReport.id)

    result = await db.execute(statement)
    return list(result.scalars().all())

#Get by id
@router.get("/{DiagnosticReport_id}", response_model=DiagnosticReportRead)
async def get_DiagnosticReport(
    DiagnosticReport_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DiagnosticReport:
    statement =  await db.get(DiagnosticReport, DiagnosticReport_id)
    if statement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"DiagnosticReport not found with the ID {DiagnosticReport_id}",
            )
    return statement

#Create tech
@router.post("/", response_model=DiagnosticReportRead)
async def create_DiagnosticReport(
    DiagnosticReport_data: DiagnosticReportCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> DiagnosticReport:
    diagnosticreport = DiagnosticReport(**DiagnosticReport_data.model_dump())
    db.add(diagnosticreport)
    await db.commit()
    await db.refresh(diagnosticreport)
    return diagnosticreport


#Update tech
@router.post("/{DiagnosticReport_id}", response_model=DiagnosticReportRead)
async def update_DiagnosticReport(
    DiagnosticReport_id: int,
    DiagnosticReport_data: DiagnosticReportUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
) -> DiagnosticReport:
    diagnosticreport = await db.get(DiagnosticReport, DiagnosticReport_id)
    if not diagnosticreport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"DiagnosticReport not found with the ID {DiagnosticReport_id}"
        )
    for key, value in DiagnosticReport_data.model_dump(exclude_unset=True).items():
        setattr(diagnosticreport, key, value)
    await db.commit()
    await db.refresh(diagnosticreport)
    return diagnosticreport

#Delete tech
@router.delete("/{DiagnosticReport_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_DiagnosticReport(
    DiagnosticReport_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
):
    diagnosticreport = await db.get(DiagnosticReport, DiagnosticReport_id)
    if diagnosticreport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"DiagnosticReport not found with the ID {DiagnosticReport_id}",
        )
    await db.delete(diagnosticreport)
    await db.commit()
    return None


