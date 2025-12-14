from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.event import Event
from app.models.booking import Booking
from app.crud.booking import refresh_price

def add_ticket_to_booking(*, db: Session, booking_id: int, event_id: int, seat_number: int):
    event = db.query(Event).filter(Event.id == event_id).first()

    ticket = Ticket(
        seat_number=seat_number,
        event_id=event_id,
        booking_id=booking_id
    )

    event.available_tickets -= 1
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    refresh_price(
        db=db,
        booking_id=booking_id,
        ticket_price=event.price_per_ticket
    )

    return ticket

def get_ticket(*, db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

def delete_ticket(*, db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    event = ticket.event
    booking = ticket.booking

    event.available_tickets += 1

    refresh_price(
        db=db,
        booking_id=booking.booking_id,
        ticket_price=-event.price_per_ticket
    )

    db.delete(ticket)
    db.commit()
    return ticket

def get_sold_tickets_by_event(*, db: Session, event_id: int):
    return db.query(Ticket).filter(Ticket.event_id == event_id).all()

def get_available_seats_by_event(*, db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    sold_seats = {t.seat_number for t in db.query(Ticket).filter(Ticket.event_id == event_id).all()}
    return [s for s in range(1, event.venue.capacity + 1) if s not in sold_seats]

def get_my_tickets(*, db: Session, user_id: int):
    return db.query(Ticket).join(Ticket.booking).filter(Booking.user_id == user_id).all()


def cancel_booking(*, db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()

    tickets = db.query(Ticket).filter(Ticket.booking_id == booking_id).all()
    for t in tickets:
        t.event.available_tickets += 1
        refresh_price(db=db, booking_id=booking_id, ticket_price=-t.event.price_per_ticket)
        db.delete(t)
        db.commit()
    return booking