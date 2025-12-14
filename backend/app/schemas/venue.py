from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VenueBase(BaseModel):
    name:str = Field(...)
    address:str = Field(...)
    capacity: int = Field(...)

class VenueInDB(VenueBase):
    id: int = Field(...)
    inactive_since: Optional[datetime]

    class Config:
        from_attributes = True

class Venue(VenueInDB):
    pass