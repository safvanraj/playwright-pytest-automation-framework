import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.fixture
def logged_in_page(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user","secret_sauce")
    yield page