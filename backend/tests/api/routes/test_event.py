from datetime import datetime, timedelta
def test_create_event(client_with_organizer, test_venue):
    response = client_with_organizer.post("/event/create", json={
        "name": "New Event",
        "description": "A fun event",
        "date_time": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "price_per_ticket": 20.0,
        "venue_id": test_venue.id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Event"
    assert data["venue"]["id"] == test_venue.id

def test_create_event_conflict(client_with_organizer, test_event):
    response = client_with_organizer.post("/event/create", json={
        "name": "Conflict Event",
        "description": "Conflict",
        "date_time": test_event.date_time.isoformat(),
        "price_per_ticket": 30.0,
        "venue_id": test_event.venue_id
    })
    assert response.status_code == 409

def test_get_event(client_with_organizer, test_event):
    response = client_with_organizer.get(f"/event/get/{test_event.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_event.id

def test_get_event_not_found(client_with_organizer):
    response = client_with_organizer.get("/event/get/999")
    assert response.status_code == 404

def test_get_all_events(client_with_organizer, test_event):
    response = client_with_organizer.get("/event/all")
    assert response.status_code == 200
    assert any(e["id"] == test_event.id for e in response.json())

def test_get_all_events_empty(client_with_organizer):
    response = client_with_organizer.get("/event/all")
    assert response.status_code == 204

def test_get_events_by_venue(client_with_organizer, test_event, test_venue):
    response = client_with_organizer.get(f"/event/venue/{test_venue.id}")
    assert response.status_code == 200
    assert any(e["id"] == test_event.id for e in response.json())

def test_get_events_by_venue_not_found(client_with_organizer):
    response = client_with_organizer.get("/event/venue/999")
    assert response.status_code == 404

def test_get_events_by_organizer(client_with_organizer, test_event, test_organizer):
    response = client_with_organizer.get(f"/event/organizer/{test_organizer.id}")
    assert response.status_code == 200
    assert any(e["id"] == test_event.id for e in response.json())

def test_get_events_by_organizer_not_found(client_with_organizer):
    response = client_with_organizer.get("/event/organizer/999")
    assert response.status_code == 404

def test_get_upcoming_events(client_with_organizer, test_event):
    response = client_with_organizer.get("/event/upcoming")
    assert response.status_code == 200
    assert any(e["id"] == test_event.id for e in response.json())

def test_get_past_events(client_with_organizer,test_past_event, test_venue, test_organizer):
    response = client_with_organizer.get("/event/past")
    assert response.status_code == 200
    assert any(e["id"] == test_past_event.id for e in response.json())

def test_update_event(client_with_organizer, test_event, test_venue):
    response = client_with_organizer.put(f"/event/update/{test_event.id}", json={
        "name": "Updated Event",
        "description": "Updated description",
        "date_time": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "price_per_ticket": 60.0,
        "venue_id": test_venue.id,
        "available_tickets": test_event.available_tickets
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Event"

def test_update_event_not_found(client_with_organizer):
    response = client_with_organizer.put("/event/update/999", json={
        "name": "Nonexistent",
        "description": "None",
        "date_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "price_per_ticket": 20.0,
        "venue_id": 1,
        "available_tickets": 10
    })
    assert response.status_code == 404

def test_delete_event(client_with_organizer, test_event):
    response = client_with_organizer.delete(f"/event/delete/{test_event.id}")
    assert response.status_code == 200

def test_delete_event_not_found(client_with_organizer):
    response = client_with_organizer.delete("/event/delete/999")
    assert response.status_code == 404