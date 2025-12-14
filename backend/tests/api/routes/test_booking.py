from app.enums.booking_state import Booking_State

def test_create_booking(client_with_user):
    response = client_with_user.post("/booking/create")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] is not None
    assert data["status"] == Booking_State.IN_PROGRESS.value

def test_read_booking_success(client_with_user, test_booking):
    response = client_with_user.get(f"/booking/get/{test_booking.booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["booking_id"] == test_booking.booking_id

def test_read_booking_not_found(client_with_user):
    response = client_with_user.get("/booking/get/0")
    assert response.status_code == 404

def test_read_booking_access_denied(client_with_another_user, test_booking):
    response = client_with_another_user.get(f"/booking/get/{test_booking.booking_id}")
    assert response.status_code == 403

def test_read_my_bookings_success(client_with_user, test_booking):
    response = client_with_user.get("/booking/mybookings")
    assert response.status_code == 200
    data = response.json()
    assert any(b["booking_id"] == test_booking.booking_id for b in data)

def test_read_my_bookings_empty(client_with_another_user):
    response = client_with_another_user.get("/booking/mybookings")
    assert response.status_code == 204

def test_complete_booking_success(client_with_user, test_booking):
    response = client_with_user.put(f"/booking/{test_booking.booking_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == Booking_State.COMPLETE.value

def test_complete_booking_already_complete(client_with_user, test_booking):
    client_with_user.put(f"/booking/{test_booking.booking_id}/complete")
    response = client_with_user.put(f"/booking/{test_booking.booking_id}/complete")
    assert response.status_code == 409

def test_complete_booking_access_denied(client_with_another_user, test_booking):
    response = client_with_another_user.put(f"/booking/{test_booking.booking_id}/complete")
    assert response.status_code == 403

def test_complete_booking_not_found(client_with_user):
    response = client_with_user.put("/booking/0/complete")
    assert response.status_code == 404

def test_pay_booking_success(client_with_user, test_booking):
    client_with_user.put(f"/booking/{test_booking.booking_id}/complete")
    response = client_with_user.put(f"/booking/{test_booking.booking_id}/pay")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == Booking_State.PAYED.value

def test_pay_booking_already_payed(client_with_user, test_booking):
    client_with_user.put(f"/booking/{test_booking.booking_id}/complete")
    client_with_user.put(f"/booking/{test_booking.booking_id}/pay")
    response = client_with_user.put(f"/booking/{test_booking.booking_id}/pay")
    assert response.status_code == 409

def test_pay_booking_in_progress(client_with_user, test_booking):
    response = client_with_user.put(f"/booking/{test_booking.booking_id}/pay")
    assert response.status_code == 409

def test_pay_booking_access_denied(client_with_user,client_with_another_user, test_booking):
    client_with_user.put(f"/booking/{test_booking.booking_id}/complete")
    response = client_with_another_user.put(f"/booking/{test_booking.booking_id}/pay")
    assert response.status_code == 403

def test_pay_booking_not_found(client_with_user):
    response = client_with_user.put("/booking/0/pay")
    assert response.status_code == 404

def test_cancel_booking_success(client_with_user, test_booking):
    response = client_with_user.delete(f"/booking/{test_booking.booking_id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["booking_id"] == test_booking.booking_id

def test_cancel_booking_access_denied(client_with_another_user, test_booking):
    response = client_with_another_user.delete(f"/booking/{test_booking.booking_id}/cancel")
    assert response.status_code == 403

def test_cancel_booking_not_found(client_with_user):
    response = client_with_user.delete("/booking/0/cancel")
    assert response.status_code == 404