from enum import Enum

class Booking_State(Enum):
    IN_PROGRESS = "in_progress"
    PAYED = "payed"
    COMPLETE = "complete"