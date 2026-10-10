# QA Automation Showcase

Test automation framework for web UI and REST APIs built with Python, Playwright, and Pytest.

The project demonstrates test architecture using the Page Object Model (POM) pattern for frontend testing against SauceDemo, and integration/contract tests against the Restful-Booker and ReqRes REST APIs.

---

## Test Coverage

### UI Automation (Playwright)
Target: https://www.saucedemo.com/

- Page Object Model implementation separating selectors from test assertions.
- Authentication tests covering successful login, locked-out users, invalid credentials, empty field validations, and user logout.
- Inventory catalog tests covering item count, dynamic sorting (A-Z, Z-A, price low-to-high, price high-to-low), and shopping cart badge counter updates.
- Shopping cart tests covering item review, removal, and navigation back to the catalog.
- End-to-end checkout flow verifying customer info form validation, subtotal and tax calculation, and order completion.

### API Testing (Pytest + Requests)
Targets: Restful-Booker and ReqRes

- Restful-Booker: Ping health check, admin token authentication, booking creation, retrieval, full update (PUT), partial update (PATCH), deletion (DELETE), and 404 validation.
- ReqRes: Paginated user lists, schema contract assertions, user creation, updates, and deletion with handling for third-party rate limits.

---

## Project Structure

```
qa-automation-showcase/
├── .github/
│   └── workflows/
│       └── qa-ci.yml           # GitHub Actions CI workflow
├── docs/
│   ├── bug-reports/
│   │   ├── BUG-001-checkout-postal-code.md
│   │   └── BUG-002-inventory-sorting-persistence.md
│   └── test-strategy.md        # Test strategy and pyramid documentation
├── pages/
│   ├── __init__.py             # Page object exports
│   ├── base_page.py            # Base page with Playwright wrappers and waits
│   ├── login_page.py           # Login page actions and locators
│   ├── inventory_page.py       # Catalog, sorting, and cart actions
│   ├── cart_page.py            # Cart item verification and removal
│   └── checkout_page.py        # Checkout form, summary, and confirmation
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and reporting hooks
│   ├── api/
│   │   ├── client.py           # API clients for Restful-Booker and ReqRes
│   │   ├── test_auth_api.py    # Auth and token generation tests
│   │   ├── test_booking_api.py # Booking CRUD lifecycle tests
│   │   └── test_users_api.py   # User management and pagination tests
│   └── ui/
│       ├── test_login.py       # UI authentication tests
│       ├── test_inventory.py   # Catalog sorting and badge tests
│       └── test_checkout_e2e.py # End-to-end purchasing workflow tests
├── pytest.ini                  # Pytest configuration and markers
├── requirements.txt            # Python dependencies
└── README.md
```

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- Git

### Installation

1. Clone the repository:
```bash
git clone git@github.com:hamzaihsan9/qa-automation-showcase.git
cd qa-automation-showcase
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the Playwright Chromium browser:
```bash
playwright install chromium
```

---

## Running Tests

### Run all tests
```bash
pytest
```
Generates a self-contained HTML report at `report.html`.

### Run by category
```bash
# Run only API tests
pytest tests/api/

# Run only UI tests
pytest tests/ui/
```

### Run by pytest marker
```bash
# Smoke tests
pytest -m smoke

# Full regression suite
pytest -m regression

# End-to-end checkout flow
pytest -m e2e
```

### Run UI tests in headed mode
```bash
pytest tests/ui/ --headed --slowmo 500
```

---

## Reporting

- An HTML test report is generated automatically at `report.html` after every test run.
- On test failure, full-page screenshots are saved automatically to `test-results/screenshots/` and embedded in the HTML report.

To view the report:
```bash
xdg-open report.html
```

---

## CI/CD Pipeline

The repository includes a GitHub Actions workflow in `.github/workflows/qa-ci.yml` that runs on every push and pull request to `main`. It:
- Sets up Python 3.12 with pip caching.
- Installs dependencies and Playwright browser binaries.
- Executes the test suite with Chromium.
- Uploads `report.html` and failure screenshots as workflow artifacts.

---

## Defect Reports

Documented bug reports following standard industry formats are located in `docs/bug-reports/`:
- `BUG-001-checkout-postal-code.md`: Form validation wording discrepancy and whitespace handling.
- `BUG-002-inventory-sorting-persistence.md`: Catalog sort filter resets on navigation back from cart.

---

## Author

Hamza Ihsan
- GitHub: https://github.com/hamzaihsan9
- Email: hamza.ihsan.f@gmail.com
