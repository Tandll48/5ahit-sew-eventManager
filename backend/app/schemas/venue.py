from pydantic import BaseModel, Field

class VenueBase(BaseModel):
    name:str = Field(...)
    address:str = Field(...)
    capacity: int = Field(...)

class VenueInDB(VenueBase):
    id: int = Field(...)

    class Config:
        from_attributes = True

class Venue(VenueInDB):
    pass