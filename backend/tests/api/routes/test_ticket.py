def test_add_ticket_success(client_with_user, test_booking, test_event):
    response = client_with_user.post("/ticket/add", params={"booking_id": test_booking.booking_id, "event_id": test_event.id, "seat_number": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["seat_number"] == 2

def test_add_ticket_booking_not_found(client_with_user, test_event):
    response = client_with_user.post("/ticket/add", params={"booking_id": 0, "event_id": test_event.id, "seat_number": 1})
    assert response.status_code == 404

def test_add_ticket_event_not_found(client_with_user, test_booking):
    response = client_with_user.post("/ticket/add", params={"booking_id": test_booking.booking_id, "event_id": 0, "seat_number": 1})
    assert response.status_code == 404

def test_add_ticket_access_denied(client_with_another_user, test_booking, test_event):
    response = client_with_another_user.post("/ticket/add", params={"booking_id": test_booking.booking_id, "event_id": test_event.id, "seat_number": 1})
    assert response.status_code == 403

def test_add_ticket_seat_taken(client_with_user, test_ticket, test_booking, test_event):
    response = client_with_user.post("/ticket/add", params={"booking_id": test_booking.booking_id, "event_id": test_event.id, "seat_number": 1})
    assert response.status_code == 409

def test_add_ticket_seat_out_of_range(client_with_user, test_booking, test_event):
    response = client_with_user.post("/ticket/add", params={"booking_id": test_booking.booking_id, "event_id": test_event.id, "seat_number": 999})
    assert response.status_code == 409

def test_get_ticket_success(client_with_user, test_ticket):
    response = client_with_user.get(f"/ticket/{test_ticket.ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == test_ticket.ticket_id

def test_get_ticket_not_found(client_with_user):
    response = client_with_user.get("/ticket/0")
    assert response.status_code == 404

def test_get_ticket_access_denied(client_with_another_user, test_ticket):
    response = client_with_another_user.get(f"/ticket/{test_ticket.ticket_id}")
    assert response.status_code == 403

def test_delete_ticket_success(client_with_user, test_ticket):
    response = client_with_user.delete(f"/ticket/{test_ticket.ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == test_ticket.ticket_id

def test_delete_ticket_not_found(client_with_user):
    response = client_with_user.delete("/ticket/0")
    assert response.status_code == 404

def test_delete_ticket_access_denied(client_with_another_user, test_ticket):
    response = client_with_another_user.delete(f"/ticket/{test_ticket.ticket_id}")
    assert response.status_code == 403

def test_available_tickets_success(client_with_user, test_event):
    response = client_with_user.get(f"/ticket/event/{test_event.id}/available")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_available_tickets_none(client_with_user):
    response = client_with_user.get("/ticket/event/0/available")
    assert response.status_code == 204

def test_sold_tickets_success(client_with_user, test_event):
    response = client_with_user.get(f"/ticket/event/{test_event.id}/sold")
    assert response.status_code == 200

def test_sold_tickets_none(client_with_user):
    response = client_with_user.get("/ticket/event/0/sold")
    assert response.status_code == 204

def test_my_tickets_success(client_with_user, test_ticket):
    response = client_with_user.get("/ticket/mytickets")
    assert response.status_code == 200
    data = response.json()
    assert any(t["ticket_id"] == test_ticket.ticket_id for t in data)

def test_my_tickets_empty(client_with_another_user):
    response = client_with_another_user.get("/ticket/mytickets")
    assert response.status_code == 204