from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from app.crud import event as crud
from app.schemas import event as schemas
from app.api.deps import SessionDep, authorize_admin, authorize_admin_or_organizer, authorize_organizer, get_current_user, CurrentUser
from app.crud.venue import get_venue
from app.crud.user import get_user

router = APIRouter()

router = APIRouter(prefix="/event", tags=["events"])

@router.post("/create", dependencies=[Depends(authorize_organizer)],response_model=schemas.Event)
def create_event(db:SessionDep,event:schemas.EventCreate, user:CurrentUser):
    venue = get_venue(db=db,venue_id=event.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    if venue.inactive_since is not None:
        raise HTTPException(status_code = 409, detail="Venue is inactive, you can't hold a event there.")
    event_conflict = crud.get_event_by_location_date(db=db,date=event.date_time, venue_id=event.venue_id)
    if event_conflict is not None:
        raise HTTPException(status_code=409,detail="There is already an event at this date, at the venue!")
    return crud.create_event(db=db,event=event,organizer_id=user.id)

@router.get("/get/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: SessionDep):
    event = crud.get_event(db=db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/all", response_model=List[schemas.Event])
def get_all_events(db: SessionDep):
    events= crud.get_events(db=db)
    if not events:
        raise HTTPException(status_code=204)
    return events

@router.get("/venue/{venue_id}", response_model=List[schemas.Event])
def get_events_by_venue(venue_id: int, db: SessionDep):
    db_venue = get_venue(db=db,venue_id=venue_id)
    if not db_venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    events = crud.get_events_by_venue(db=db, venue_id=venue_id)
    if not events:
        raise HTTPException(status_code=204)
    return events

@router.get("/organizer/{organizer_id}", response_model=List[schemas.Event])
def get_events_by_organizer(organizer_id: int, db: SessionDep):
    db_user = get_user(db=db,user_id=organizer_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    events = crud.get_events_by_organizer(db=db, organizer_id=organizer_id)
    if not events:
        raise HTTPException(status_code=204)
    return events

@router.get("/upcoming", response_model=List[schemas.Event])
def get_upcoming_events(db: SessionDep):
    events = crud.get_upcoming_events(db=db)
    if not events:
        raise HTTPException(status_code=204)
    return events

@router.get("/past", response_model=List[schemas.Event])
def get_past_events(db: SessionDep):
    events = crud.get_past_events(db=db)
    if not events:
        raise HTTPException(status_code=204)
    return events

@router.put("/update/{event_id}", dependencies=[Depends(authorize_admin_or_organizer)],response_model=schemas.Event)
def update_event(event_id: int,event: schemas.EventUpdate,db: SessionDep,user: CurrentUser):
    venue = get_venue(db=db,venue_id=event.venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    if venue.inactive_since is not None:
        raise HTTPException(status_code = 409, detail="Venue is inactive, you can't hold a event there.")
    organizer_id = crud.get_organizer(db=db,event_id = event_id)
    if user.is_admin is False and user.id != organizer_id:
        raise HTTPException(status_code=403, detail="Permission denied for events, you are not the organizer of!")
    event_conflict = crud.get_event_by_location_date(db=db,date=event.date_time, venue_id=event.venue_id,event_id=event_id)
    if event_conflict is not None:
        raise HTTPException(status_code=409,detail="There is already an event at this date, at the venue!")
    event_db= crud.get_event(db=db,event_id=event_id)
    if not event_db:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.update_event(db=db,event_id=event_id,event=event)

@router.delete("/delete/{event_id}",dependencies=[Depends(authorize_admin_or_organizer)],response_model=schemas.Event)
def delete_event(event_id: int, db: SessionDep, user:CurrentUser):
    event_db= crud.get_event(db=db,event_id=event_id)
    if not event_db:
        raise HTTPException(status_code=404, detail="Event not found")
    #check für tickets nacha einbauen
    organizer_id = crud.get_organizer(db=db,event_id = event_id)
    if user.is_admin is False and user.id != organizer_id:
        raise HTTPException(status_code=403, detail="Permission denied for events, you are not the organizer of!")
    return crud.delete_event(db=db,event_id=event_id)
