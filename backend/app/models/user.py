from sqlalchemy import Column, String, DateTime, Boolean
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_organizer = Column(Boolean, nullable=False, default=False)
    phone_number = Column(String, nullable=True)
