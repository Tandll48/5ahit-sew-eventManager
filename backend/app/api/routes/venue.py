from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from app.crud import venue as crud
from app.schemas import venue as schemas
from app.api.deps import SessionDep, authorize_admin, authorize_organizer
from app.crud.event import get_upcoming_events_by_venue

router = APIRouter()

router = APIRouter(prefix="/venue", tags=["venues"])

@router.post("/create",dependencies=[Depends(authorize_organizer)],response_model=schemas.Venue)
def create_venue(db:SessionDep,venue:schemas.VenueBase):
    existing_address = crud.get_venue_by_address(db=db,address=venue.address)
    if existing_address is not None:
        raise HTTPException(status_code=409, detail="There is already a venue located at this address!")
    return crud.create_venue(db=db,venue=venue)

@router.get("/{venue_id:int}",response_model=schemas.Venue)
def get_venue(db:SessionDep,venue_id:int):
    venue = crud.get_venue(db=db,venue_id=venue_id)
    if venue is None:
        raise HTTPException(status_code=204)
    return venue

@router.get("/all",response_model=List[schemas.Venue])
def get_all_venues(db:SessionDep):
    venues = crud.get_venues(db=db)
    if venues is None:
        raise HTTPException(status_code=204)
    return venues

@router.put("/activate/{venue_id}",dependencies=[Depends(authorize_admin)],response_model=schemas.Venue)
def activate_venue(db:SessionDep,venue_id:int):
    venue = crud.get_venue(db=db,venue_id=venue_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found!")
    if venue.inactive_since is not None:
        raise HTTPException(status_code=409, detail="Venue is already active!")
    return crud.activate_venue(db=db,id=venue_id)

@router.put("/update/{venue_id}",dependencies=[Depends(authorize_organizer)],response_model=schemas.Venue)
def update_venue(db:SessionDep, venue_id:int,venue:schemas.VenueBase):
    venue = crud.get_venue(db=db,venue_id=venue_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found!")
    upcoming_events = get_upcoming_events_by_venue(db=db, venue_id=venue_id)
    if upcoming_events is not None:
        raise HTTPException(status_code=404, detail="You can't change a venue, where are upcoming events!")
    existing_address = crud.get_venue_by_address(db=db,address=venue.address, venue_id=venue_id)
    if existing_address is not None:
        raise HTTPException(status_code=409, detail="There is already a venue located at this address!")
    return crud.update_venue(db=db,id=venue_id,venue=venue)

@router.delete("/delete/{venue_id}",dependencies=[Depends(authorize_organizer)],response_model=schemas.Venue)
def delete_venue(db:SessionDep, venue_id:int):
    venue = crud.get_venue(db=db,venue_id=venue_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found!")
    upcoming_events = get_upcoming_events_by_venue(db=db, venue_id=venue_id)
    if upcoming_events is not None:
        raise HTTPException(status_code=404, detail="You can't change a venue, where are upcoming events!")
    return crud.delete_venue(db=db,id=venue_id)

