"""
User Model - for RBAC
"""

#still need annotations from future but not typechecking
from __future__ import annotations

#sqlalchemy and .orm
from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import UserRole

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", values_callable=lambda obj: [e.value for e in obj]),
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    #functions
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username!r}', role={self.role.value})>"