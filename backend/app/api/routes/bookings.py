from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.api.deps import SessionDep, get_current_user, CurrentUser
from app.schemas import booking as schemas
from app.crud import booking as crud
from app.enums.booking_state import Booking_State
from app.crud.ticket import cancel_booking as cancel_tickets


router = APIRouter(prefix="/booking", tags=["bookings"])

@router.post("/create", response_model=schemas.Booking)
def create_booking(db: SessionDep, user: CurrentUser):
    return crud.create_booking(db=db, user_id=user.id)


@router.get("/get/{booking_id}", response_model=schemas.Booking)
def read_booking(db: SessionDep,booking_id: int, user: CurrentUser):
    booking = crud.get_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return booking

@router.get("/mybookings",response_model=List[schemas.Booking])
def read_my_bookings(db: SessionDep, user: CurrentUser):
    bookings = crud.get_bookings_by_user(db=db,user_id=user.id)
    if not bookings:
        raise HTTPException(status_code=204)
    return bookings 

@router.put("/{booking_id}/complete", response_model=schemas.Booking)
def complete_booking(db: SessionDep, booking_id: int, user: CurrentUser):
    booking = crud.get_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if booking.status == Booking_State.PAYED:
        raise HTTPException(status_code=409, detail="Booking is already payed")
    if booking.status == Booking_State.COMPLETE:
        raise HTTPException(status_code=409, detail="Booking is already complete!")
    return crud.complete_booking(db=db, booking_id=booking_id)


@router.put("/{booking_id}/pay", response_model=schemas.Booking)
def pay_booking(db: SessionDep,booking_id: int,user: CurrentUser):
    booking = crud.get_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == Booking_State.PAYED:
        raise HTTPException(status_code=409, detail="Booking is already payed")
    if booking.status == Booking_State.IN_PROGRESS:
        raise HTTPException(status_code=409, detail="Booking isn't completed yet!")
    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.pay_booking(db=db, booking_id=booking_id)


@router.delete("/{booking_id}/cancel", response_model=schemas.Booking)
def cancel_booking(db: SessionDep,booking_id: int, user: CurrentUser):
    booking = crud.get_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    cancel_tickets(db=db,booking_id=booking_id)
    return crud.delete_booking(db=db,booking_id=booking_id)
