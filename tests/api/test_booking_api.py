from playwright.sync_api import APIRequestContext

NEW_BOOKING = {
    "firstname": "Test",
    "lastname": "User",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-12-01",
        "checkout": "2026-12-05",
    },
    "additionalneeds": "Breakfast",
}


def test_get_all_bookings(api: APIRequestContext):
    response = api.get("/booking")

    assert response.status == 200
    bookings = response.json()
    assert len(bookings) > 0


def test_create_booking(api: APIRequestContext):
    response = api.post("/booking", data=NEW_BOOKING)

    assert response.status == 200
    body = response.json()
    assert body["bookingid"] > 0
    assert body["booking"]["firstname"] == "Test"


def test_get_created_booking(api: APIRequestContext):
    create_response = api.post("/booking", data= NEW_BOOKING)
    booking_id = create_response.json()["bookingid"]

    response = api.get(f"/booking/{booking_id}")
    assert response.status == 200
    booking = response.json()
    assert booking["firstname"] == "Test"
    assert booking["lastname"] == "User"
    assert booking["totalprice"] == 150 

def test_update_booking(api: APIRequestContext, token:str):
    create_response = api.post("/booking", data =NEW_BOOKING)
    booking_id = create_response.json()["bookingid"]

    updated_booking = NEW_BOOKING.copy()
    updated_booking["firstname"] = "Updated"

    response = api.put(
        f"/booking/{booking_id}",
        data=updated_booking,
        headers={"Cookie": f"token={token}"},
    )
    assert response.status == 200
    assert response.json()["firstname"] == "Updated"

def test_deleted_booking(api: APIRequestContext, token:str):
    create_response = api.post("/booking", data= NEW_BOOKING)
    booking_id = create_response.json()["bookingid"]

    response = api.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={token}"},
        )
    assert response.status == 201

    get_response = api.get(f"/booking/{booking_id}")
    assert get_response.status == 404
