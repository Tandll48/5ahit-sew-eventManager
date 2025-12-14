from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.enums.booking_state import Booking_State
from app.schemas.ticket import Ticket

class BookingBase(BaseModel):
    user_id: int = Field(...)

class BookingInDB(BaseModel):
    booking_id: int
    booking_date: datetime
    status: Booking_State
    total_price: float

    class Config:
        from_attributes = True

class Booking(BookingInDB):
    tickets: List[Ticket] = []