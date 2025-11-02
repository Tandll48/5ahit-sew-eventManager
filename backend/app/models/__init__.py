from sqlalchemy.orm import relationship
from app.models.user import User
from app.models.venue import Venue
from app.models.event import Event
from app.models.booking import Booking
from app.models.ticket import Ticket

User.bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
User.organized_events = relationship("Event", back_populates="organizer", cascade="all, delete-orphan")

Venue.events = relationship("Event", back_populates="venue", cascade="all, delete-orphan")

Event.venue = relationship("Venue", back_populates="events")
Event.organizer = relationship("User", back_populates="organized_events")
Event.tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")

Booking.user = relationship("User", back_populates="bookings")
Booking.tickets = relationship("Ticket", back_populates="booking", cascade="all, delete-orphan")

Ticket.event = relationship("Event", back_populates="tickets")
Ticket.booking = relationship("Booking", back_populates="tickets")

