import csv
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage



DATA_FILE = Path(__file__).parents[2]/"test_data"/ "login_users.csv"

def  load_login_data():
    with open(DATA_FILE, newline="") as file:
        return [
            (raw["username"], raw["password"], raw["expected"])
            for raw in csv.DictReader(file)

        ]

@pytest.mark.parametrize("username, password, expected", load_login_data())
def test_login_data_driven(page: Page, username, password, expected):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username,password)

    if expected == "success":
        expect(page.locator("[data-test = 'title']")).to_have_text("Products")
    else:
        expect(login_page.error_message).to_contain_text(expected)


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