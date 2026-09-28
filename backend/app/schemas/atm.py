"""
ATM Pydantic Schema
"""
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import ATMStatus

class ATMBase(BaseModel):
    serial_number: str = Field(min_length=1, max_length = 50)
    model: str = Field(min_length=1, max_length=100)
    cash_level: Decimal = Field(ge = 0, le = 100)
    branch_id: int
    status: ATMStatus = ATMStatus.OFFLINE # Default status for a new ATM


#Two additional classes that can build upon this
class ATMCreate(ATMBase):
    """
    Shape of the Request Body for Creating an ATM
    Builds off of ATMBase (ie adds the additional fields required for creating)
    """

class ATMRead(ATMBase):
    """
    Shape of the Response Body for Reading an ATM
    Builds off of ATMBase (ie includes all fields)
    """
    id: int

    #This allows the model to be instantiated from ORM attributes
    model_config = ConfigDict(from_attributes=True)
