# Project Plan: playwright-pytest-automation-framework

A portfolio project to show employers real QA skills:
UI automation, API testing, performance testing, CI, and manual QA.

| Part | What you test | Tool | Skill it proves |
|---|---|---|---|
| UI tests | SauceDemo shop (login, cart, checkout) | Playwright + Python | Automation, POM, fixtures |
| Data-driven tests | Login with 4+ users from CSV | pytest `parametrize` | Test data handling |
| API tests | Restful-Booker (practice hotel booking API) | Playwright `request` + Postman | API testing, CRUD, auth tokens |
| Performance | Small load test | JMeter | Performance basics |
| CI | Tests run on every push | GitHub Actions | DevOps awareness |
| Manual QA docs | Test cases + bug reports | Markdown | Manual testing skills |

Practice sites (made for testing, safe to automate):
- UI: https://www.saucedemo.com (user `standard_user`, password `secret_sauce`)
- API: https://restful-booker.herokuapp.com

---

## Progress checklist

### Phase 1 (Days 1–3): UI tests with POM
- [ ] `git init`, `.gitignore`, first commit, push to GitHub
- [ ] `pages/login_page.py`
- [ ] `pages/products_page.py`
- [ ] `pages/cart_page.py`
- [ ] `pages/checkout_page.py`
- [ ] `tests/ui/test_login.py` (success, wrong password, locked user)
- [ ] `tests/ui/test_cart.py` (add, remove, item count)
- [ ] `tests/ui/test_checkout.py` (full checkout, empty form error)
- [ ] `logged_in_page` fixture in `conftest.py`

### Phase 2 (Day 4): Data-driven login from CSV
- [ ] `test_data/login_users.csv`
- [ ] `test_login_data_driven` with `@pytest.mark.parametrize`

### Phase 3 (Days 5–6): API tests
- [ ] Explore Restful-Booker in Postman, save a collection, export to `postman/`
- [ ] `api` fixture in `conftest.py`
- [ ] `tests/api/test_booking_api.py`: create, get
- [ ] Stretch: auth token, update (PUT), delete

### Phase 4 (Day 7): CI with GitHub Actions
- [ ] `requirements.txt`
- [ ] `.github/workflows/tests.yml`
- [ ] Green check mark on GitHub

### Phase 5 (Days 8–10): JMeter + manual QA docs
- [ ] `jmeter/booking_load_test.jmx` (local server, or at most 5 users on public practice APIs)
- [ ] `docs/test_cases.md` (10–15 test cases)
- [ ] `docs/bug_reports.md` (3 bugs found with `problem_user` / `error_user`)

### Phase 6 (Days 11–12): README + polish
- [ ] README with tech stack, coverage, how to run, folder tree, screenshot
- [ ] Pin the repo on your GitHub profile
- [ ] Add the project to your resume and LinkedIn

---

## Daily routine (about 4–5 hours)

| Block | Time | What |
|---|---|---|
| Main learning | 2–2.5 hrs | That day's phase |
| Side track | 45–60 min | JMeter |
| Job hunt | 1 hr | Apply to 3–5 jobs every day |

Daily Git rhythm:

```
write  ->  run tests  ->  pass?  ->  git add + git commit  ->  git push
```

---

## Target folder structure

```
playwright-pytest-automation-framework/
├── pages/
│   ├── __init__.py
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/
│   │   ├── test_login.py
│   │   ├── test_cart.py
│   │   └── test_checkout.py
│   └── api/
│       └── test_booking_api.py
├── test_data/
│   └── login_users.csv
├── postman/
│   └── restful_booker.postman_collection.json
├── jmeter/
│   └── booking_load_test.jmx
├── docs/
│   ├── test_cases.md
│   └── bug_reports.md
├── .github/workflows/
│   └── tests.yml
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
├── PROJECT_PLAN.md
└── README.md
```

---

## Code reference

### `.gitignore`

```
.venv/
venv*/
__pycache__/
.pytest_cache/
test-results/
report/
report.html
.env
```

### `requirements.txt`

```
pytest
pytest-playwright
pytest-html
pytest-xdist
```

### `pytest.ini`

```ini
[pytest]
testpaths = tests
addopts = -v
```

### `pages/login_page.py`

```python
from playwright.sync_api import Page


class LoginPage:
    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator("[data-test='error']")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

### `pages/products_page.py`

```python
from playwright.sync_api import Page


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def add_to_cart(self, product_name: str):
        product = self.page.locator(".inventory_item").filter(has_text=product_name)
        product.get_by_role("button", name="Add to cart").click()

    def open_cart(self):
        self.cart_link.click()
```

### `conftest.py`

```python
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_page(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    yield page


@pytest.fixture
def api(playwright):
    context = playwright.request.new_context(
        base_url="https://restful-booker.herokuapp.com",
        extra_http_headers={"Accept": "application/json"},
    )
    yield context
    context.dispose()
```

### `test_data/login_users.csv`

```
username,password,expected
standard_user,secret_sauce,success
locked_out_user,secret_sauce,locked out
standard_user,wrong123,do not match
,secret_sauce,Username is required
```

### Data-driven login test (in `tests/ui/test_login.py`)

```python
import csv
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

DATA_FILE = Path(__file__).parents[2] / "test_data" / "login_users.csv"


def load_login_data():
    with open(DATA_FILE, newline="") as file:
        return [(row["username"], row["password"], row["expected"])
                for row in csv.DictReader(file)]


@pytest.mark.parametrize("username, password, expected", load_login_data())
def test_login_data_driven(page: Page, username, password, expected):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)

    if expected == "success":
        expect(page.locator("[data-test='title']")).to_have_text("Products")
    else:
        expect(login_page.error_message).to_contain_text(expected)
```

### `tests/api/test_booking_api.py`

```python
BOOKING = {
    "firstname": "Test",
    "lastname": "User",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
    "additionalneeds": "Breakfast",
}


def test_create_booking(api):
    response = api.post("/booking", data=BOOKING)

    assert response.status == 200
    body = response.json()
    assert body["bookingid"] > 0
    assert body["booking"]["firstname"] == "Test"


def test_get_created_booking(api):
    booking_id = api.post("/booking", data=BOOKING).json()["bookingid"]

    response = api.get(f"/booking/{booking_id}")

    assert response.status == 200
    assert response.json()["lastname"] == "User"
```

### `.github/workflows/tests.yml`

```yaml
name: QA Automation Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install browsers
        run: python -m playwright install --with-deps chromium

      - name: Run tests
        run: python -m pytest --html=report.html --self-contained-html

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: report.html
```

---

## Useful commands

```
python -m pytest                                  # run all tests
python -m pytest tests/ui --headed --slowmo 500   # watch UI tests
python -m pytest --browser chromium --browser firefox -n 2   # cross-browser, parallel
python -m playwright codegen https://www.saucedemo.com      # find locators
git status / git add . / git commit -m "..." / git push
```

---

## Resume entry (fill in once built)

**playwright-pytest-automation-framework** | Python, Playwright, pytest, Postman, JMeter, GitHub Actions
- Built a UI automation framework with Page Object Model, pytest fixtures and data-driven tests from CSV
- Automated REST API CRUD tests with token-based authentication and response validation
- Set up a CI pipeline with GitHub Actions that runs all tests on every push and publishes HTML reports
- Designed a JMeter load test and documented manual test cases and bug reports
- github.com/YOUR-USERNAME/playwright-pytest-automation-framework

---

## Rules to remember

1. Run tests before you commit. Commit small and often, with clear messages.
2. Keep CI green.
3. No passwords or secrets in code. Use `.gitignore`.
4. Be able to explain every line in an interview.
5. Never load-test sites you don't own. Keep loads tiny on practice APIs.
6. Apply to jobs every day while you build.
