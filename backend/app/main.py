"""
cd backend
fastapi dev app/main.py
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.routers import auth
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


@app.get("/health")
def health():
    return {"status": "ok"}

##Endpoint to check the version number
@app.get("/version", tags=["health"])
async def version() -> dict[str, str]:
    return {"version": app.version}


#Exceptions go here 