@startuml
title Klassendiagramm - Event & Ticket Webserver 

enum BookingStatus {
  in_progress
  payed
  complete
}


class User {
  - user_id: int
  - name: string
  - email: string
  - password_hash: string
  - created_at: datetime
  - is_admin: bool
  - is_organizer: bool
  - phone_number: string
  --
  + createUser()
  + getActiveUser()
  + showUser()
  + getAllUsers()
  + set_organizer()
  + updateUser()
  + updateActiveUser()
  + deleteUser()
}

class Venue {
  - venue_id: int
  - name: string
  - address: string
  - capacity: int
  --
  + createVenue()
  + getVenue()
  + getAllVenues()
  + updateVenue()
  + deleteVenue()
}

class Event {
  - event_id: int
  - name: string
  - description: string
  - date_time: datetime
  - venue_id: int   -- FK -> Venue
  - organizer_id: int -- FK -> User (Organisator)
  - available_tickets: int
  - price_per_ticket: decimal
  --
  + createEvent()
  + readEvent()
  + updateEvent()
  + deleteEvent()
  + listEvents()
  + getDetails()
}

class Ticket {
  - ticket_id: int
  - seat_number: string
  - event_id: int    -- FK -> Event
  - booking_id: int  -- FK -> Booking
  --
  + createTicket()
  + readTicket()
  + updateTicket()
  + deleteTicket()
}

class Booking {
  - booking_id: int
  - booking_date: datetime
  - user_id: int     -- FK -> User
  - total_price: decimal
  --
  + createBooking()
  + readBooking()
  + updateBooking()
  + deleteBooking()
  + addTicket(ticket_id: int)
  + removeTicket(ticket_id: int)
  + completeBooking()
  + cancelBooking()
}

' Venue 1 -> * Event
Venue "1" --> "0..*" Event : hosts

' User (Organizer) 1 -> * Event
User "1" --> "0..*" Event : organizes

' Event 1 -> * Ticket
Event "1" --> "0..*" Ticket : has tickets

' User 1 -> * Booking
User "1" --> "0..*" Booking : books

' Booking 1 -> * Ticket
Booking "1" --> "0..*" Ticket : contains
@enduml