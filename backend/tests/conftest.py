import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.session import Base
from app.main import app
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.venue import Venue
from app.models.event import Event
from app.models.booking import Booking
from app.models.ticket import Ticket
from app.core.security import get_password_hash


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_user(db):
    user = User(
        name="Test User",
        email="user@example.com",
        phone_number="123456",
        password=get_password_hash("pass"),
        is_admin=False,
        is_organizer=False,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin(db):
    admin = User(
        name="Admin User",
        email="admin@example.com",
        phone_number="654321",
        password=get_password_hash("pass"),
        is_admin=True,
        is_organizer=False,
        created_at=datetime.now(timezone.utc)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def test_organizer(db):
    organizer = User(
        name="Organizer User",
        email="org@example.com",
        phone_number="777777",
        password=get_password_hash("pass"),
        is_admin=False,
        is_organizer=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(organizer)
    db.commit()
    db.refresh(organizer)
    return organizer

@pytest.fixture
def client_with_user(client, test_user, db):
    def override_get_current_user():
        return db.merge(test_user)
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def client_with_admin(client, test_admin, db):
    def override_get_current_user():
        return db.merge(test_admin)
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def client_with_organizer(client, test_organizer, db):
    def override_get_current_user():
        return db.merge(test_organizer)
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def test_venue(db):
    venue = Venue(
        name="Test Venue",
        address="123 Main St",
        capacity=100
    )
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


@pytest.fixture
def test_event(db, test_venue, test_admin):
    event = Event(
        name="Test Event",
        description="This is a test event",
        date_time=datetime.utcnow() + timedelta(days=1),
        available_tickets=test_venue.capacity,
        price_per_ticket=50.0,
        venue_id=test_venue.id,
        organizer_id=test_admin.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def db_event_past(db, test_venue, test_admin):
    event = Event(
        name="Past Event",
        description="This is a past event",
        date_time=datetime.utcnow() - timedelta(days=5),
        available_tickets=test_venue.capacity,
        price_per_ticket=30.0,
        venue_id=test_venue.id,
        organizer_id=test_admin.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def test_booking(db, test_user):
    booking = Booking(
        user_id=test_user.id,
        booking_date=datetime.utcnow(),
        status="IN_PROGRESS",
        total_price=0.0
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@pytest.fixture
def test_ticket(db, test_booking, test_event):
    ticket = Ticket(
        seat_number=1,
        event_id=test_event.id,
        booking_id=test_booking.booking_id
    )
    test_event.available_tickets -= 1
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket