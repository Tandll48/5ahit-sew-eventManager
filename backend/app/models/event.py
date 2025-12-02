from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from app.database.session import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    available_tickets = Column(Integer, nullable=False)
    price_per_ticket = Column(Float, nullable=False)
