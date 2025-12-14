import pytest
from datetime import datetime, timedelta
from app.schemas.event import EventCreate, EventUpdate
import app.crud.event as crud

def test_create_event(db, test_venue, test_admin):
    event_data = EventCreate(
        name="Concert",
        description="Test Concert",
        date_time=datetime.utcnow() + timedelta(days=1),
        price_per_ticket=50.0,
        venue_id=test_venue.id
    )
    event = crud.create_event(db=db, event=event_data, organizer_id=test_admin.id)
    assert event.name == "Concert"
    assert event.venue_id == test_venue.id
    assert event.available_tickets == test_venue.capacity

def test_get_event(db, test_event):
    event = crud.get_event(db=db, event_id=test_event.id)
    assert event.id == test_event.id

def test_get_events(db, test_event):
    events = crud.get_events(db=db)
    assert any(e.id == test_event.id for e in events)

def test_get_events_by_venue(db, test_event, test_venue):
    events = crud.get_events_by_venue(db=db, venue_id=test_venue.id)
    assert any(e.id == test_event.id for e in events)

def test_get_events_by_organizer(db, test_event, test_admin):
    events = crud.get_events_by_organizer(db=db, organizer_id=test_admin.id)
    assert any(e.id == test_event.id for e in events)

def test_update_event(db, test_event):
    update_data = EventUpdate(
        name="Updated Concert",
        description="Updated description",
        date_time=test_event.date_time + timedelta(days=1),
        available_tickets=150,
        price_per_ticket=60.0,
        venue_id=test_event.venue_id
    )
    event = crud.update_event(db=db, event_id=test_event.id, event=update_data)
    assert event.name == "Updated Concert"
    assert event.available_tickets == 150

def test_delete_event(db, test_event):
    crud.delete_event(db=db, event_id=test_event.id)
    event_in_db = crud.get_event(db=db, event_id=test_event.id)
    assert event_in_db is None


def test_get_upcoming_events(db, test_event):
    events = crud.get_upcoming_events(db=db)
    assert any(e.id == test_event.id for e in events)

def test_get_past_events(db, db_event_past):
    events = crud.get_past_events(db=db)
    assert any(e.id == db_event_past.id for e in events)

def test_get_event_by_location_date(db, test_event, test_venue):
    date = test_event.date_time
    event = crud.get_event_by_location_date(db=db, date=date, venue_id=test_venue.id)
    assert event.id == test_event.id

def test_get_organizer(db, test_event, test_admin):
    organizer_id = crud.get_organizer(db=db, event_id=test_event.id)
    assert organizer_id == test_admin.id

def test_get_upcoming_events_by_venue(db, test_event, test_venue):
    events = crud.get_upcoming_events_by_venue(db=db, venue_id=test_venue.id)
    assert any(e.id == test_event.id for e in events)
