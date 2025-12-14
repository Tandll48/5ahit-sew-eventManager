from sqlalchemy import DateTime, Null
from sqlalchemy.orm import Session
from app.models.venue import Venue
from app.schemas.venue import VenueBase
from datetime import datetime

def create_venue(*, db:Session, venue:VenueBase):
    db_venue = Venue(
        address = venue.address,
        name = venue.name,
        capacity = venue.capacity
    )
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

def get_venue_by_address(*, db:Session, address:str, venue_id:int = 0):
    return db.query(Venue).filter(Venue.address == address, Venue.id != venue_id).first()

def get_venue(db:Session, venue_id:int):
    return db.query(Venue).filter(Venue.id == venue_id).first()

def get_venues(*,db:Session):
    return db.query(Venue).all()

def update_venue(*,db:Session,id:int, venue:VenueBase):
    db_venue = get_venue(db=db,venue_id=id)
    db_venue.address = venue.address
    db_venue.name = venue.name
    db_venue.capacity = venue.capacity
    db.commit()
    db.refresh(db_venue)
    return db_venue

def delete_venue(*, db:Session, id:int):
    db_venue = get_venue(db=db,venue_id=id)
    db_venue.inactive_since = datetime.now()
    db.commit()
    db.refresh(db_venue)
    return db_venue

def activate_venue(*, db:Session, id:int):
    db_venue = get_venue(db=db,venue_id=id)
    db_venue.inactive_since = None
    db.commit()
    db.refresh(db_venue)
    return db_venue