from sqlalchemy import Column, String, Integer
from app.database.session import Base

class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String,unique=True ,nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
