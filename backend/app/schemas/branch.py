"""
 Branch Schema

 The main benefit of schemas is that they are tied to the API not the database which allows for more flexible and maintainable API/database design.
"""

from pydantic import BaseModel

#Default schema that others can build off (if some need very specialized they also can do BaseModel)
class BranchBase(BaseModel):
    id: int
    name: str
    location: str
