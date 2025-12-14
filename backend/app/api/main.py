from fastapi import APIRouter

from app.api.routes import cmd, users, login, venue, event, bookings, ticket

api_router = APIRouter()
api_router.include_router(cmd.router)
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(venue.router)
api_router.include_router(event.router)
api_router.include_router(bookings.router)
api_router.include_router(ticket.router)