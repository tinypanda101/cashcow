"""
ATM Model - Represents an ATM in the organization

Connects with Branch and ServiceCall Models
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import ATMStatus

if TYPE_CHECKING:
    from branch import Branch
    from servicecall import ServiceCall


#Cash Level refers to percentages here not actual cash amounts so we want it between 0 and 100

class ATM(Base):
    __tablename__ = "atms"

    #Table level constraint to ensure cash_level is between 0 and 100
    __table_args__ = (
       CheckConstraint("cash_level BETWEEN 0 and 100", name= "cash_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True) #We want unique to prevent duplicate ATMs
    model: Mapped[str] = mapped_column(String(100))
    #status is an ENUM
    status: Mapped[ATMStatus] = mapped_column(
        SqlEnum(
            ATMStatus,
            name="atm_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default = ATMStatus.OPERATIONAL)
    cash_level: Mapped[Decimal] = mapped_column(Numeric(5,2))
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))

    #Relationships
    #Outbound relationship is branch, for every branch, there can be multiple ATMs
    branch: Mapped["Branch"] = relationship(back_populates="atms")

    #Inbound relationship is servicecall, for every ATM, there can be multiple service calls
    service_calls: Mapped[list["ServiceCall"]] = relationship(back_populates="atm")

    def __repr__(self) -> str:
        return f"ATM id={self.id} serial_number={self.serial_number!r}, model={self.model!r}, cash_level={self.cash_level!r}, branch_id={self.branch_id!r}"