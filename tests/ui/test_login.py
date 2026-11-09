from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

def test_login_success(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    expect(page.locator("[data-test='title']")).to_have_text("Products")


def test_login_wrong_password(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "wrong123")

    expect(login_page.error_message).to_contain_text("do not match")