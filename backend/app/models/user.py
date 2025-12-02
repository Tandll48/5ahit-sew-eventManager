from sqlalchemy import Column, String, DateTime, Boolean, Integer
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_organizer = Column(Boolean, nullable=False, default=False)
    phone_number = Column(String, unique=True,nullable=True)
