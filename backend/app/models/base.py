"""
Shared declarative base for every ORM model to inherit from instead of one in every file
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass