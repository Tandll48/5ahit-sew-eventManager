import pytest
from app.crud import ticket as crud

def test_add_ticket_to_booking(db, test_booking, test_event):
    seat_number = 1
    ticket = crud.add_ticket_to_booking(
        db=db, 
        booking_id=test_booking.booking_id, 
        event_id=test_event.id, 
        seat_number=seat_number
    )
    assert ticket.seat_number == seat_number
    assert ticket.booking_id == test_booking.booking_id
    assert ticket.event_id == test_event.id
    assert test_event.available_tickets == test_event.venue.capacity - 1

def test_get_ticket(db, test_ticket):
    t = crud.get_ticket(db=db, ticket_id=test_ticket.ticket_id)
    assert t.ticket_id == test_ticket.ticket_id

def test_delete_ticket(db, test_ticket, test_event):
    event_before = test_event.available_tickets
    ticket = crud.delete_ticket(db=db, ticket_id=test_ticket.ticket_id)
    assert ticket.ticket_id == test_ticket.ticket_id
    assert test_event.available_tickets == event_before + 1

def test_get_sold_tickets_by_event(db, test_event, test_ticket):
    tickets = crud.get_sold_tickets_by_event(db=db, event_id=test_event.id)
    assert test_ticket in tickets

def test_get_available_seats_by_event(db, test_event, test_ticket):
    seats = crud.get_available_seats_by_event(db=db, event_id=test_event.id)
    assert test_ticket.seat_number not in seats

def test_get_my_tickets(db, test_user, test_booking, test_ticket):
    tickets = crud.get_my_tickets(db=db, user_id=test_user.id)
    assert test_ticket in tickets

def test_cancel_booking(db, test_booking, test_ticket):
    booking = crud.cancel_booking(db=db, booking_id=test_booking.booking_id)
    assert booking.booking_id == test_booking.booking_id
    tickets = crud.get_my_tickets(db=db, user_id=test_booking.user_id)
    assert test_ticket not in tickets
    assert test_booking.booking_id == booking.booking_id
