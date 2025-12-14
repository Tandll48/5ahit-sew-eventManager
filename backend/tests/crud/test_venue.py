import pytest
from app.schemas.venue import VenueBase
import app.crud.venue as crud


def test_create_venue(db):
    venue_data = VenueBase(name="Test Venue", address="123 Main St", capacity=100)
    venue = crud.create_venue(db=db, venue=venue_data)
    assert venue.name == "Test Venue"
    assert venue.address == "123 Main St"
    assert venue.capacity == 100

def test_get_venue(db, test_venue):
    venue = crud.get_venue(db=db, venue_id=test_venue.id)
    assert venue.id == test_venue.id

def test_get_venues(db, test_venue):
    venues = crud.get_venues(db=db)
    assert any(v.id == test_venue.id for v in venues)

def test_get_venue_by_address(db, test_venue):
    venue = crud.get_venue_by_address(db=db, address=test_venue.address)
    assert venue.id == test_venue.id

def test_update_venue(db, test_venue):
    updated_data = VenueBase(name="Updated Venue", address="456 Street", capacity=200)
    venue = crud.update_venue(db=db, id=test_venue.id, venue=updated_data)
    assert venue.name == "Updated Venue"
    assert venue.address == "456 Street"
    assert venue.capacity == 200

def test_delete_venue(db, test_venue):
    venue = crud.delete_venue(db=db, id=test_venue.id)
    assert venue.inactive_since is not None

def test_activate_venue(db, test_venue):
    crud.delete_venue(db=db, id=test_venue.id)
    venue = crud.activate_venue(db=db, id=test_venue.id)
    assert venue.inactive_since is None
