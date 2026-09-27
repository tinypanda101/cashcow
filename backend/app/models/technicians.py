"""
Technician Model, (not in initial Data Architecture but needed)

Connects with ServiceCall and Branch models
"""

#need annotations from future and typechecking from typing
from __future__ import annotations
from typing import TYPE_CHECKING

#sqlalchemy stuff and .orm stuff
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

#need base from .base
from .base import Base

if TYPE_CHECKING:
    #put foriegn key models here
    from servicecall import ServiceCall
    from branch import Branch

class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id")) #foreign key


    # Relationships
    #Outbound relationship is branch, for every branch, there can be multiple technicians
    branch: Mapped["Branch"] = relationship(back_populates="technicians")

    #Inbound relationship is service_calls for every tech there can be multiple service calls
    service_calls: Mapped[list["ServiceCall"]] = relationship(back_populates="technician")

    # Functions
    def __repr__(self) -> str:
        return (f"Technician(id={self.id}, name='{self.name!r}', branch_id={self.branch_id})")