def test_create_venue(client_with_organizer):
    response = client_with_organizer.post("/venue/create", json={
        "name": "Test Venue",
        "address": "123 Main St",
        "capacity": 100
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Venue"

def test_create_venue_address_exists(client_with_organizer, test_venue):
    response = client_with_organizer.post("/venue/create", json={
        "name": "Another Venue",
        "address": test_venue.address,
        "capacity": 50
    })
    assert response.status_code == 409

def test_get_venue(client_with_organizer, test_venue):
    response = client_with_organizer.get(f"/venue/{test_venue.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_venue.id

def test_get_venue_not_found(client_with_organizer):
    response = client_with_organizer.get("/venue/0")
    assert response.status_code == 204

def test_get_all_venues(client_with_organizer, test_venue):
    response = client_with_organizer.get("/venue/all")
    assert response.status_code == 200
    ids = [v["id"] for v in response.json()]
    assert test_venue.id in ids

def test_activate_venue(client_with_organizer, inactive_venue):
    inactive_venue.inactive_since = "2025-01-01T00:00:00"
    response = client_with_organizer.put(f"/venue/activate/{inactive_venue.id}")
    assert response.status_code == 200
    assert response.json()["inactive_since"] is None

def test_activate_venue_not_found(client_with_organizer):
    response = client_with_organizer.put("/venue/activate/0")
    assert response.status_code == 404

def test_activate_venue_already_active(client_with_organizer, test_venue):
    test_venue.inactive_since = None
    response = client_with_organizer.put(f"/venue/activate/{test_venue.id}")
    assert response.status_code == 409

def test_update_venue(client_with_organizer, test_venue):
    response = client_with_organizer.put(f"/venue/update/{test_venue.id}", json={
        "name": "Updated Venue",
        "address": "456 Another St",
        "capacity": 150
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Venue"

def test_update_venue_not_found(client_with_organizer):
    response = client_with_organizer.put("/venue/update/0", json={
        "name": "Name",
        "address": "Address",
        "capacity": 100
    })
    assert response.status_code == 404

def test_update_venue_address_exists(client_with_organizer, test_venue):
    new_venue = test_venue
    response = client_with_organizer.put(f"/venue/update/{test_venue.id}", json={
        "name": "Venue New",
        "address": new_venue.address,
        "capacity": 100
    })
    assert response.status_code == 409

def test_delete_venue(client_with_organizer, test_venue):
    response = client_with_organizer.delete(f"/venue/delete/{test_venue.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_venue.id

def test_delete_venue_not_found(client_with_organizer):
    response = client_with_organizer.delete("/venue/delete/0")
    assert response.status_code == 404
