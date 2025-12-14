from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.event import Event

class TicketBase(BaseModel):
    seat_number: int = Field(..., gt=0)
    booking_id: int = Field(...)

class TicketInDBBase(TicketBase):
    ticket_id: int

    class Config:
        from_attributes = True

class Ticket(TicketInDBBase):
    event: Event
