"""
 Branch Schema

 The main benefit of schemas is that they are tied to the API not the database which allows for more flexible and maintainable API/database design.
"""

from pydantic import BaseModel, ConfigDict, Field

#Default schema that others can build off (if some need very specialized they also can do BaseModel)
class BranchBase(BaseModel):
    name: str = Field(min_length = 2, max_length = 50)
    location_region: str = Field(min_length = 2, max_length = 100)
    capacity: int = Field(ge = 0)
    supervisor_id: int



class BranchCreate(BranchBase):
    """
    Shape of the Request Body for Creating a Branch
    Builds off of BranchBase (ie adds the additional fields required for creating)
    """


class BranchRead(BranchBase):
    """
    Shape of the Response Body for Reading a Branch
    Builds off of BranchBase (ie includes all fields)
    """
    id: int

    #This allows the model to be instantiated from ORM attributes
    model_config = ConfigDict(from_attributes=True)
