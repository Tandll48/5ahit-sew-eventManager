from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.session import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    venue_id = Column(String, ForeignKey("venues.id"), nullable=False)
    organizer_email = Column(String, ForeignKey("users.email"), nullable=False)
