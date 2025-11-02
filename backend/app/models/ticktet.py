from sqlalchemy import Column, Integer, ForeignKey
from app.database.session import Base

class Ticket(Base):
    __tablename__ = "tickets"

    seat_number = Column(Integer, primary_key=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True, nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
