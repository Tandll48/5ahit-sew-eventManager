import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
from app.core.security import create_access_token

def test_missing_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_invalid_token(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer wrongtoken"})
    assert response.status_code == 401

def test_user_not_found_token(client, db):
    token = create_access_token({"sub": "nonexistent@test.com"}, expires_delta=timedelta(minutes=15))
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_create_user(client_with_admin):
    response = client_with_admin.post("/users/create", json={
        "name": "AliceUser",
        "email": "alice@test.com",
        "password": "Password1",
        "phone_number": "1234567890",
        "is_admin": False
    })
    assert response.status_code == 200
    assert response.json()["name"] == "AliceUser"
    assert response.json()["email"] == "alice@test.com"

def test_create_user_email_exists(client_with_admin, test_admin):
    response = client_with_admin.post("/users/create", json={
        "name": "BobUser",
        "email": test_admin.email,
        "password": "Password1",
        "phone_number": "555555",
        "is_admin": False
    })
    assert response.status_code == 409
    assert "email" in response.json()["detail"]

def test_create_user_phone_exists(client_with_admin, test_admin):
    response = client_with_admin.post("/users/create", json={
        "name": "CharlieUser",
        "email": "charlie@test.com",
        "password": "Password1",
        "phone_number": test_admin.phone_number,
        "is_admin": False
    })
    assert response.status_code == 409
    assert "phone number" in response.json()["detail"]

def test_get_user(client_with_admin, test_user):
    response = client_with_admin.get(f"/users/get/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id

def test_get_user_not_found(client_with_admin):
    response = client_with_admin.get("/users/get/0")
    assert response.status_code == 204

def test_get_active_user(client_with_user, test_user):
    response = client_with_user.get("/users/me")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id

def test_get_all_users(client_with_admin, test_admin, test_user):
    response = client_with_admin.get("/users/all")
    assert response.status_code == 200
    ids = [u["id"] for u in response.json()]
    assert test_admin.id in ids
    assert test_user.id in ids

def test_set_organizer(client_with_admin, test_user):
    response = client_with_admin.put(f"/users/add_organizer/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["is_organizer"] is True

def test_set_organizer_not_found(client_with_admin):
    response = client_with_admin.put("/users/add_organizer/0")
    assert response.status_code == 404

def test_update_user(client_with_admin, test_user):
    response = client_with_admin.put(f"/users/update/{test_user.id}", json={
        "name": "UpdatedUser",
        "email": "updated@test.com",
        "password": "NewPass1",
        "phone_number": "111222333"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedUser"

def test_update_user_not_found(client_with_admin):
    response = client_with_admin.put("/users/update/0", json={
        "name": "Namen",
        "email": "name@test.com",
        "password": "Password1",
        "phone_number": "12345"
    })
    assert response.status_code == 404

def test_update_user_email_exists(client_with_admin, test_user, test_admin):
    response = client_with_admin.put(f"/users/update/{test_user.id}", json={
        "name": "User2",
        "email": test_admin.email,
        "password": "Password1",
        "phone_number": "123456"
    })
    assert response.status_code == 409

def test_update_me(client_with_user, test_user):
    response = client_with_user.put("/users/me/update", json={
        "name": "MeUpdate",
        "email": "meupdate@test.com",
        "password": "Password1",
        "phone_number": "987654321"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "MeUpdate"

def test_delete_user(client_with_admin, test_user):
    response = client_with_admin.delete(f"/users/delete/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id

def test_delete_user_not_found(client_with_admin):
    response = client_with_admin.delete("/users/delete/0")
    assert response.status_code == 404

def test_delete_myself(client_with_admin, test_admin):
    response = client_with_admin.delete(f"/users/delete/{test_admin.id}")
    assert response.status_code == 403
    assert "can't delete yourself" in response.json()["detail"]
