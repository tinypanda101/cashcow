"""
Password Hashing and JWT helper functions
"""

import os
from datetime import datetime, timedelta, timezone
from app.config import settings

import bcrypt
import jwt

import hashlib
import secrets

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#Takes plain text as input and returns a hashed password
def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")
#Takes a hashed and a plain text as input and returns a boolean indicating if they match
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

#Creates a JWT token (JWT = Json Web Token)
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    #To_encode is a copy of the input data dictionary, which is used to create payload of jwt
    to_encode = data.copy()
    

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)




#Decodes a JWT token and returns payload
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def hash_refresh_token(refresh_token: str) -> str:
   return hashlib.sha256(token.encode("utf-8")).hexdigest()