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