
import asyncio
import boto3
from botocore.config import Config
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserRole, User
from app.dependencies import get_db, get_current_user, require_role

S3_BUCKET = "cashcow-diagnostics-binx"

router = APIRouter(prefix="/health", tags=["health"]
)


# Basic check to see if the API is running, doesnt check database connection
@router.get("", tags=["health"])
def health():
    return {"status": "ok"}


# Basic check to see if the database is reachable, doesnt check if the user has permission to access the database
@router.get("/ready", tags=["health"])
async def readiness(
    db: AsyncSession = Depends(get_db),
):
    try:
        await asyncio.wait_for(db.execute(select(1)), timeout=3)
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail={"status": "unavailable"})


    
s3_health = boto3.client("s3", config=Config(connect_timeout=2, read_timeout=2, retries={"total_max_attempts": 1}))
# More detailed check that requires Admin role to access
@router.get("/detail", tags=["health"])
async def health_detail(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(UserRole.OPERATIONS_ADMIN)),
    
):
    try:
        await asyncio.wait_for(db.execute(select(1)), timeout=3)
        database = "up"
    except Exception:
        database = "down"

    try:
        await asyncio.wait_for(asyncio.to_thread(s3_health.head_bucket, Bucket=S3_BUCKET), timeout=3)
        s3 = "up"
    except Exception:
        s3 = "down"

    return {"database": database, "s3": s3}
