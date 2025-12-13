from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.crud import user as crud
from app.schemas import user as schemas
from app.api.deps import SessionDep, authorize_admin, get_current_user, CurrentUser


router = APIRouter()

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", dependencies=[Depends(authorize_admin)],response_model=schemas.User)
def create_user(db: SessionDep, user: schemas.UserCreate):
    existing_user = crud.get_user_by_email(db=db,email = user.email) 
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="There is already a account with this email!")
    if user.phone_number is not None:
        existing_phone = crud.get_user_by_phone_number(db=db, number=user.phone_number)
        if existing_phone is not None:
           raise HTTPException(status_code=409, detail="There is already a account with this phone number!")
    return crud.create_user(db=db, user=user)


@router.get("/get/{user_id}",response_model=schemas.User)
def get_user(db: SessionDep, user_id: int):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=204, detail="No user with ID:{user_id}")
    return user

@router.get("/me",dependencies=[Depends(get_current_user)],response_model=schemas.User)
def get_active_user(db: SessionDep, current_user:CurrentUser):
    return crud.get_user(db=db, user_id=current_user.id)

@router.get("/all",dependencies=[Depends(authorize_admin)],response_model=List[schemas.User])
def get_all_users(db: SessionDep):
    return crud.get_users(db=db)

@router.put("/add_organizer/{user_id}",dependencies=[Depends(authorize_admin)], response_model=schemas.User)
def set_organizer(db: SessionDep, user_id: int):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="No user with ID:{user_id}")
    return crud.set_organizer(db=db, id=user_id)


@router.put("/update/{user_id}",dependencies=[Depends(authorize_admin)],response_model=schemas.User)
def update_user(db:SessionDep, user:schemas.UserUpdate, user_id: int):
    existing_user = crud.get_user(db=db,user_id=user_id)
    if existing_user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    existing_email = crud.get_user_by_email(db=db,email = user.email,id = user_id) 
    if existing_email is not None:
        raise HTTPException(status_code=409, detail="There is already a account with this email!")
    if user.phone_number is not None:
        existing_phone = crud.get_user_by_phone_number(db=db, number=user.phone_number,id = user_id)
        if existing_phone is not None:
           raise HTTPException(status_code=409, detail="There is already a account with this phone number!")
    return crud.update_user(db=db,user=user,id=user_id)


@router.put("/me/update",dependencies=[Depends(get_current_user)],response_model=schemas.User)
def update_me(db: SessionDep, user:schemas.UserUpdate, current_user:CurrentUser):
    existing_user = crud.get_user_by_email(db=db,email = user.email,id = current_user.id) 
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="There is already a account with this email!")
    if user.phone_number is not None:
        existing_phone = crud.get_user_by_phone_number(db=db, number=user.phone_number,id = current_user.id)
        if existing_phone is not None:
           raise HTTPException(status_code=409, detail="There is already a account with this phone number!")
    return crud.update_user(db=db,user=user,id=current_user.id)

@router.delete("/delete/{user_id}",dependencies=[Depends(authorize_admin)],response_model=schemas.User)
def delete_user(db:SessionDep, user_id: int, current_user:CurrentUser):
    user_exists = crud.get_user(db=db,user_id=user_id)
    if user_exists is None:
        raise HTTPException(status_code=404,detail="User not found")
    if current_user.id == user_id:
        raise HTTPException(status_code=403,detail="You can't delete yourself")
    return crud.delete_user(db=db,id=user_id)

