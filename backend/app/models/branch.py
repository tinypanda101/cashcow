"""
Branch Model - Represents a branch in the organization

Connects with ATM and Technician Models
"""


#tells python to treat every type annotation as a string literal, allowing forward references to classest that are defined later
from __future__ import annotations


#Loading the TYPE_CHECKING constant from the typing modules which is used to indicate that certain imports are only needed for type checking and not at runtime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
#ORM = Object Relational Mapper
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from atm import ATM
    from technicians import Technician

class Branch(Base):
    #Table name for model
    __tablename__ = "branches"

    #fields
    id: Mapped[int] = mapped_column(primary_key=True) # Primary key, increases by itself. We do not touch it
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)

    #Relationships
    #No Outbound Relationships

    #Inbound Relationships are ATMs and Technicians
    #For every branch, there can be multiple ATMs and Technicians
    #when Inbound Relationship if the incoming is the many use lists
    atms: Mapped[list["ATM"]] = relationship(back_populates="branch")
    technicians: Mapped[list["Technician"]] = relationship(back_populates="branch")

    def __repr__(self) -> str:
        return f"Branch(id={self.id}, name={self.name!r}, location_region={self.location_region!r})"