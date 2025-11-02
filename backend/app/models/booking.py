from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from app.database.session import Base

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_date = Column(DateTime, nullable=False)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
