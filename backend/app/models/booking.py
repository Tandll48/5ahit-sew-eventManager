from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Float, null
from app.database.session import Base
from app.enums.booking_state import Booking_State


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(Booking_State),default=Booking_State.IN_PROGRESS,nullable=False)
    total_price = Column(Float,nullable=True)
