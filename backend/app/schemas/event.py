from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.venue import Venue
from app.schemas.user import User

class EventBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5)
    date_time: datetime
    price_per_ticket: float = Field(...)
    venue_id: int

class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    available_tickets: int = Field(..., ge=0)

class EventInDBBase(EventBase):
    id: int
    venue: Venue
    organizer: User
    available_tickets: int = Field(..., ge=0)
    organizer_id: int

    class Config:
        from_attributes = True

class Event(EventInDBBase):
    pass