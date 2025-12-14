from sqlalchemy.orm import Session
from datetime import datetime
from app.models.booking import Booking
from app.enums.booking_state import Booking_State

def create_booking(*, db: Session, user_id: int):
    booking = Booking(
        user_id=user_id,
        booking_date=datetime.utcnow(),
        status=Booking_State.IN_PROGRESS,
        total_price=0.0
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_booking(*, db: Session, booking_id: int):
    return (db.query(Booking).filter(Booking.booking_id == booking_id).first())

def get_bookings_by_user(*, db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def refresh_price(*, db: Session, booking_id: int, ticket_price: float):
    booking = get_booking(db=db, booking_id=booking_id)
    booking.total_price += ticket_price
    db.commit()
    db.refresh(booking)
    return booking

def complete_booking(*, db: Session, booking_id: int):
    booking = get_booking(db=db, booking_id=booking_id)
    booking.status = Booking_State.COMPLETE
    db.commit()
    db.refresh(booking)
    return booking


def pay_booking(*, db: Session, booking_id: int):
    booking = get_booking(db=db, booking_id=booking_id)
    booking.status = Booking_State.PAYED
    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(*, db: Session, booking_id: int):
    booking = get_booking(db=db, booking_id=booking_id)
    db.commit()
    db.delete(booking)
    return booking

