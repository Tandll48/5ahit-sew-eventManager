from datetime import datetime
from app.schemas.user import UserCreate, UserUpdate
import app.crud.user as crud

def test_create_user(db):
    data = UserCreate(name="John Doe", email="john@example.com", phone_number="123456", password="secret", is_admin=False)
    user = crud.create_user(db=db, user=data)
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.is_admin == False
    assert user.created_at is not None

def test_create_superuser(db):
    data = UserCreate(name="Admin", email="admin@example.com", phone_number="654321", password="secret", is_admin=True)
    user = crud.create_superuser(db=db, user=data)
    assert user.is_admin is True
    assert user.created_at is not None

def test_get_user(db, test_user):
    user = crud.get_user(db=db, user_id=test_user.id)
    assert user.id == test_user.id
    assert user.email == test_user.email

def test_get_users(db, test_user):
    users = crud.get_users(db=db)
    assert len(users) > 0

def test_update_user(db, test_user):
    data = UserUpdate(name="Updated Name", email="upd@example.com", phone_number="999999", password="newpass")
    updated = crud.update_user(db=db, id=test_user.id, user=data)
    assert updated.name == "Updated Name"
    assert updated.email == "upd@example.com"
    assert updated.phone_number == "999999"

def test_delete_user(db, test_user):
    deleted = crud.delete_user(db=db, id=test_user.id)
    # deleted object should still exist, but removed from DB
    assert deleted.id == test_user.id
    # verify user is gone
    assert crud.get_user(db=db, user_id=test_user.id) is None

def test_authenticate_user(db, test_user):
    auth = crud.authenticate_user(db=db, email=test_user.email, password="pass")
    assert auth is not None
    assert auth.id == test_user.id

def test_authenticate_wrong_password(db, test_user):
    auth = crud.authenticate_user(db=db, email=test_user.email, password="wrong")
    assert auth is None

def test_authenticate_wrong_email(db):
    auth = crud.authenticate_user(db=db, email="wrong@example.com", password="pass")
    assert auth is None

def test_get_user_by_email(db, test_user):
    user = crud.get_user_by_email(db=db, email=test_user.email)
    assert user.id == test_user.id

def test_get_user_by_phone_number(db, test_user):
    user = crud.get_user_by_phone_number(db=db, number=test_user.phone_number)
    assert user.id == test_user.id

def test_set_organizer(db, test_user):
    user = crud.set_organizer(db=db, id=test_user.id)
    assert user.is_organizer is True
