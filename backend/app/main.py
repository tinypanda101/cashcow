"""
cd backend
fastapi dev app/main.py
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.routers import auth, atm, branch, technicians,servicecall, diagnosticreport, health
from app.config import settings



app = FastAPI(
    title = "CashCow Command Center",
    description = "API for managing CashCow operations",
    version = "0.1.0"
)

FRONTEND_ORIGIN = settings.frontend_origin


app.add_middleware(
    CORSMiddleware, 
    allow_origins=[FRONTEND_ORIGIN], 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True
)

#this is where routers go
app.include_router(auth.router)
app.include_router(atm.router)
app.include_router(branch.router)
app.include_router(technicians.router)
app.include_router(servicecall.router)
app.include_router(diagnosticreport.router)
app.include_router(health.router)

##Endpoint to check the version number
@app.get("/version", tags=["health"])
async def version() -> dict[str, str]:
    return {"version": app.version}


#Exceptions go here 