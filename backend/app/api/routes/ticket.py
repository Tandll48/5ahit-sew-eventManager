from typing import List
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.schemas.ticket import Ticket
from app.crud import ticket as crud

router = APIRouter(prefix="/ticket", tags=["tickets"])

@router.post("/add", response_model=Ticket)
def add_ticket(booking_id: int, event_id: int, seat_number: int, db: SessionDep, user: CurrentUser):
    booking = db.query(crud.Booking).filter(crud.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    event = db.query(crud.Event).filter(crud.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.available_tickets <= 0:
        raise HTTPException(status_code=409, detail="No tickets available")
    if seat_number < 1 or seat_number > event.venue.capacity:
        raise HTTPException(status_code=409, detail="Seat number out of range")
    seat_taken = db.query(crud.Ticket).filter(crud.Ticket.event_id==event_id, crud.Ticket.seat_number==seat_number).first()
    if seat_taken:
        raise HTTPException(status_code=409, detail="Seat already taken")
    return crud.add_ticket_to_booking(db=db, booking_id=booking_id, event_id=event_id, seat_number=seat_number)

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int, db: SessionDep, user: CurrentUser):
    ticket = crud.get_ticket(db=db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return ticket

@router.delete("/{ticket_id}", response_model=Ticket)
def delete_ticket(ticket_id: int, db: SessionDep, user: CurrentUser):
    ticket = crud.get_ticket(db=db, ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.delete_ticket(db=db, ticket_id=ticket_id)

@router.get("/event/{event_id}/available", response_model=List[int])
def available_tickets(event_id: int, db: SessionDep):
    seats = crud.get_available_seats_by_event(db=db, event_id=event_id)
    if not seats:
        raise HTTPException(status_code=204)
    return seats

@router.get("/event/{event_id}/sold", response_model=List[Ticket])
def sold_tickets(event_id: int, db: SessionDep):
    tickets = crud.get_sold_tickets_by_event(db=db, event_id=event_id)
    if not tickets:
        raise HTTPException(status_code=204)
    return tickets

@router.get("/mytickets", response_model=List[Ticket])
def my_tickets(db: SessionDep, user: CurrentUser):
    tickets = crud.get_my_tickets(db=db, user_id=user.id)
    if not tickets:
        raise HTTPException(status_code=204)
    return tickets

