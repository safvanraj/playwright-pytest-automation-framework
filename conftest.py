import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.fixture
def logged_in_page(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user","secret_sauce")
    yield page


@pytest.fixture
def api(playwright):
    context = playwright.request.new_context(
        base_url="https://restful-booker.herokuapp.com",
        extra_http_headers ={"Accept": "application/json"},
    )
    yield context
    context.dispose()

@pytest.fixture
def token(api):
    response = api.post(
        "/auth",
        data = {"username": "admin", "password": "password123"},
    )
    assert response.status == 200
    return response.json()["token"]