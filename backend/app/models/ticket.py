from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database.session import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    seat_number = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=True)