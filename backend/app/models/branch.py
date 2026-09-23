"""
Branch Model - Represents a branch in the organization
"""


#tells python to treat every type annotation as a string literal, allowing forward references to classest that are defined later
from __future__ import annotations


#Loading the TYPE_CHECKING constant from the typing modules which is used to indicate that certain imports are only needed for type checking and not at runtime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
#ORM = Object Relational Mapper
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import base

if TYPE_CHECKING:
    #put forigen key models here

class Branch(base):
    #Table name for model
    __tablename__ = "branches"

    #fields
    id: Mapped[int] = mapped_column(primary_key=True) # Primary key, increases by itself. We do not touch it
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)

    #Create relationships (ie bc ATM has branch_Id it needs to be related to Branch, etc)
    #need to spend time understanding this i still dont really get it
    #copying from robopulse this would be ATM and Technicians both bc of branchid (id here)

    def __repr__(self) -> str:
        return f"Branch(id={self.id}, name={self.name!r}, location_region={self.location_region!r})"