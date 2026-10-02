"""
User and Auth Schema
"""

from pydantic import BaseModel, ConfigDict, Field

from app.models import UserRole


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(UserBase):
    username: str | None = Field(default = None, max_length=100, min_length=2)
    role: UserRole | None = None
    password: str | None = Field(default=None, min_length=6, max_length=100)



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"