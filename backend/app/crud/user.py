from os import name
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timezone


def create_user(*, db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        phone_number=user.phone_number,
        email=user.email,
        password=get_password_hash(user.password),
        is_admin=user.is_admin,
        created_at=datetime.now(timezone.utc),
        is_organizer = False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_superuser(*, db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        phone_number=user.phone_number,
        email=user.email,
        password=get_password_hash(user.password),
        is_admin=True,
        created_at=datetime.now(timezone.utc),
        is_organizer = False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(*, db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(*, db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    if not verify_password(password, str(db_user.password)):
        return None
    return db_user


def get_user_by_email(*, db: Session, email: str, id: int = 0):
    return db.query(User).filter(User.email == email, User.id != id).first()

def get_user_by_phone_number(*, db: Session, number: str, id: int = 0):
    return db.query(User).filter(User.phone_number == number, User.id != id).first()


def update_user(*, db:Session, user: UserUpdate, id:int):
    db_user = get_user(db=db,user_id=id)
    db_user.name = user.name
    db_user.email = user.email
    db_user.phone_number = user.phone_number
    db_user.password = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(*, db:Session, id:int):
    db_user =get_user(db=db,user_id=id)
    db.delete(db_user)
    db.commit()
    return db_user

def set_organizer(*, db:Session, id:int):
    db_user = get_user(db=db, user_id=id)
    db_user.is_organizer = True
    db.commit()
    db.refresh(db_user)
    return db_user