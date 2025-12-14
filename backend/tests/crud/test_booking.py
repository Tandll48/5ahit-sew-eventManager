import pytest
from app.crud import booking as crud
from app.enums.booking_state import Booking_State

def test_create_booking(db, test_user):
    booking = crud.create_booking(db=db, user_id=test_user.id)
    assert booking.user_id == test_user.id
    assert booking.status == Booking_State.IN_PROGRESS
    assert booking.total_price == 0.0

def test_get_booking(db, test_booking):
    booking = crud.get_booking(db=db, booking_id=test_booking.booking_id)
    assert booking.booking_id == test_booking.booking_id

def test_get_bookings_by_user(db, test_user, test_booking):
    bookings = crud.get_bookings_by_user(db=db, user_id=test_user.id)
    assert test_booking in bookings

def test_refresh_price(db, test_booking):
    new_total = test_booking.total_price + 50.0
    booking = crud.refresh_price(db=db, booking_id=test_booking.booking_id, ticket_price=50.0)
    assert booking.total_price == new_total

def test_complete_booking(db, test_booking):
    booking = crud.complete_booking(db=db, booking_id=test_booking.booking_id)
    assert booking.status == Booking_State.COMPLETE

def test_pay_booking(db, test_booking):
    # set status to COMPLETE first to allow payment
    crud.complete_booking(db=db, booking_id=test_booking.booking_id)
    booking = crud.pay_booking(db=db, booking_id=test_booking.booking_id)
    assert booking.status == Booking_State.PAYED

def test_delete_booking(db, test_booking):
    booking_id = test_booking.booking_id
    booking = crud.delete_booking(db=db, booking_id=booking_id)
    assert booking.booking_id == booking_id
    assert crud.get_booking(db=db, booking_id=booking_id) is None
