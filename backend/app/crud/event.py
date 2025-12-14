from os import name
from sqlalchemy.orm import Session
from app.models.event import Event 
from app.schemas.event import EventBase, EventCreate, EventUpdate
from datetime import date, datetime
from app.crud.venue import get_venue
from sqlalchemy import func

def get_event_by_location_date(*,db:Session,date:datetime, venue_id:int, event_id:int = 0):
    return db.query(Event).filter(func.date(Event.date_time) == date.date(), Event.venue_id == venue_id, Event.id != event_id).first()

def create_event(*,db:Session,event:EventCreate, organizer_id:int):
    venue_db = get_venue(db=db, venue_id=event.venue_id)
    event_db = Event(
        name = event.name,
        description = event.description,
        date_time = event.date_time,
        available_tickets = venue_db.capacity,
        price_per_ticket = event.price_per_ticket,
        venue_id = event.venue_id,
        organizer_id = organizer_id
    )
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db

def get_event(*, db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(*, db: Session):
    return db.query(Event).all()

def get_events_by_venue(*, db: Session, venue_id: int):
    return db.query(Event).filter(Event.venue_id == venue_id).all()

def get_events_by_organizer(*, db: Session, organizer_id: int):
    return db.query(Event).filter(Event.organizer_id == organizer_id).all()

def get_organizer(*, db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    return event.organizer_id

def get_upcoming_events(*,db:Session):
    return db.query(Event).filter(Event.date_time > datetime.now()).all()

def get_past_events(*,db:Session):
    return db.query(Event).filter(Event.date_time < datetime.now()).all()

def update_event(*, db: Session, event_id: int, event: EventUpdate):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    db_event.name = event.name
    db_event.description = event.description
    db_event.date_time = event.date_time
    db_event.available_tickets = event.available_tickets
    db_event.price_per_ticket = event.price_per_ticket
    db_event.venue_id = event.venue_id
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(*, db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    db.delete(db_event)
    db.commit()
    return db_event

def get_upcoming_events_by_venue(*,db:Session,venue_id:int):
    return db.query(Event).filter(Event.date_time > datetime.now(), Event.venue_id == venue_id).all()