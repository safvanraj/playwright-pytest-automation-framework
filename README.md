# Playwright + Pytest Automation Framework

![Tests](https://github.com/safvanraj/playwright-pytest-automation-framework/actions/workflows/tests.yml/badge.svg)

A test automation framework built with **Playwright (Python)** and **pytest**, covering both **UI** and **API** testing, with **CI on GitHub Actions**.

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Playwright | Browser automation and API requests |
| pytest | Test runner, fixtures, parametrize |
| pytest-html | HTML test reports |
| pytest-xdist | Parallel test runs |
| GitHub Actions | CI: runs all tests on every push |

## Test Coverage

| Area | Application | Tests |
|---|---|---|
| UI: Login (valid, invalid, data-driven from CSV) | [SauceDemo](https://www.saucedemo.com) | 7 |
| UI: Add to cart | SauceDemo | 1 |
| UI: Full end-to-end checkout | SauceDemo | 1 |
| API: Full CRUD (GET, POST, PUT, DELETE) with token auth | [Restful-Booker](https://restful-booker.herokuapp.com) | 5 |
| **Total** | | **14** |

## Framework Design

- **Page Object Model (POM):** each page has its own class in `pages/`, so locators live in one place
- **Fixtures (`conftest.py`):** `logged_in_page` (UI login), `api` (API request context), `token` (auth)
- **Data-driven testing:** login cases read from `test_data/login_users.csv` with `@pytest.mark.parametrize`
- **API tests verify real data:** read-back after create, 404 check after delete
- **CI pipeline:** GitHub Actions runs the full suite headless and uploads an HTML report

## Project Structure

```
.github/workflows/tests.yml   # CI pipeline
pages/                        # Page Objects (login, products, cart, checkout)
tests/
  ui/                         # Browser tests
  api/                        # API tests
test_data/login_users.csv     # Test data for data-driven login
conftest.py                   # Shared fixtures
requirements.txt              # Dependencies
```

## How to Run

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies and browsers
pip install -r requirements.txt
python -m playwright install

# 3. Run all tests
python -m pytest -v

# Run only UI or only API tests
python -m pytest tests/ui -v
python -m pytest tests/api -v

# Watch the browser
python -m pytest tests/ui --headed --slowmo 500

# HTML report
python -m pytest --html=report.html --self-contained-html
```

## Findings

- Restful-Booker returns **201** for `DELETE /booking/{id}`, where **200** or **204** is expected.
- Restful-Booker returns **418 (I'm a teapot)** when the `Accept` header is not JSON or XML.

## Roadmap

- [x] UI tests with Page Object Model
- [x] Data-driven tests (CSV)
- [x] API tests (full CRUD + auth)
- [x] CI with GitHub Actions
- [ ] Performance testing with JMeter
- [ ] Manual test cases and bug reports

## Author

**Mohmedsafvan Raj**: QA Automation
GitHub: [safvanraj](https://github.com/safvanraj)