# 🚀 Enterprise QA Automation Showcase

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-8.0+-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)](.github/workflows/qa-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade test automation engineering showcase demonstrating production-grade testing practices for full-stack systems. Built with **Python**, **Playwright**, and **Pytest**, this repository models realistic multi-layer test strategies spanning UI End-to-End flows, REST API contract validation, CI/CD automation, and systematic defect tracking.

---

## 🎯 Architecture & Coverage Overview

The framework adopts the **Test Pyramid** strategy with two core validation layers:

```
           / \
          /   \
         / E2E \         Browser UI Workflows (Playwright + POM)
        /  UI   \        SauceDemo E-Commerce Catalog & Checkout
       /---------\
      /   API     \      REST API Integration & Contract Tests
     / Integration \     Restful-Booker (CRUD/Auth) & ReqRes (User Mgmt)
    /---------------\
```

### 1. Web UI Automation (Playwright POM)
- **Target Application:** SauceDemo e-commerce portal ([saucedemo.com](https://www.saucedemo.com/)).
- **Pattern:** Page Object Model (POM) decoupling locators from test logic.
- **Scenarios:**
  - Standard user login, invalid credentials, empty field validations, and account lockout handling.
  - Dynamic catalog sorting (alphabetical ascending/descending, price low-to-high, price high-to-low).
  - Dynamic cart badge updates upon item addition and deletion.
  - Multi-step end-to-end checkout flow with subtotal, tax calculation, and order confirmation verification.

### 2. REST API Automation (Pytest + Requests)
- **Target Services:**
  - [Restful-Booker](https://restful-booker.herokuapp.com): Ping health checks, admin token generation, booking creation, retrieval, full updates (`PUT`), partial updates (`PATCH`), deletion (`DELETE`), and negative 404 validation.
  - [ReqRes](https://reqres.in): Paginated user listing, schema contract assertions, user registration, authentication, and user mutations.

---

## 📁 Repository Structure

```
qa-automation-showcase/
├── .github/
│   └── workflows/
│       └── qa-ci.yml                # Automated GitHub Actions test pipeline
├── docs/
│   ├── bug-reports/
│   │   ├── BUG-001-checkout-postal-code.md
│   │   └── BUG-002-inventory-sorting-persistence.md
│   └── test-strategy.md            # Enterprise QA test methodology & pyramid
├── pages/
│   ├── __init__.py                 # POM exports
│   ├── base_page.py                # Reusable Playwright wrappers & explicit waits
│   ├── login_page.py               # Authentication elements & methods
│   ├── inventory_page.py           # Product catalog, sorting, and cart actions
│   ├── cart_page.py                # Reviewing & removing items in the cart
│   └── checkout_page.py            # Customer info, summary calculation, finish
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures, API clients & HTML hooks
│   ├── api/
│   │   ├── __init__.py
│   │   ├── client.py               # REST API clients (Booking & ReqRes)
│   │   ├── test_auth_api.py        # Token generation & login/register tests
│   │   ├── test_booking_api.py     # Booking CRUD & lifecycle tests
│   │   └── test_users_api.py       # User management & pagination tests
│   └── ui/
│       ├── __init__.py
│       ├── test_login.py           # UI login positive & negative scenarios
│       ├── test_inventory.py       # Catalog sorting & cart badge checks
│       └── test_checkout_e2e.py    # Complete end-to-end purchasing workflow
├── pytest.ini                      # Test discovery, custom markers & options
├── requirements.txt                # Pinned framework dependencies
└── README.md                       # Documentation & execution guide
```

---

## ⚡ Quickstart & Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12 and 3.14)
- Git

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone git@github.com:hamzaihsan9/qa-automation-showcase.git
cd qa-automation-showcase

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

---

## 🧪 Running the Test Suite

All tests can be executed via `pytest` with granular control using markers or directory paths:

### Run Everything
```bash
pytest
```
*Automatically generates a self-contained HTML execution report at `report.html`.*

### Run by Domain / Layer
```bash
# Run only REST API test suites
pytest tests/api/

# Run only UI browser test suites
pytest tests/ui/
```

### Run by Pytest Marker
```bash
# Run smoke tests (fast critical path verification)
pytest -m smoke

# Run full regression suite
pytest -m regression

# Run end-to-end checkout journeys
pytest -m e2e
```

### Headed Execution (Watch Browser in Action)
```bash
pytest tests/ui/ --headed --slowmo 500
```

---

## 📊 Test Reporting

The framework generates rich, self-contained HTML execution reports via `pytest-html`:
- Open `report.html` in your browser:
  ```bash
  # Linux
  xdg-open report.html
  ```
- **Automated Failure Screenshots:** If any UI test encounters an assertion error, a full-page screenshot is automatically captured and embedded directly into the test result row under `test-results/screenshots/`.

---

## 🔄 CI/CD Automation

Every code push and pull request triggers [`.github/workflows/qa-ci.yml`](.github/workflows/qa-ci.yml):
1. Provisions Ubuntu runner with Python environment caching.
2. Installs dependencies and headless Chromium with OS-level libraries.
3. Executes `@pytest.mark.smoke` checks.
4. Executes the full regression suite.
5. Archives `report.html` and failure screenshots as build artifacts with 14-day retention.

---

## 🐞 Bug Reporting

Formal industry-standard defect reports are documented under [`docs/bug-reports/`](docs/bug-reports/):
- **BR-001:** [Inconsistent Validation Formatting on Checkout Step One](docs/bug-reports/BUG-001-checkout-postal-code.md)
- **BR-002:** [Catalog Sort State Resets on Back Navigation](docs/bug-reports/BUG-002-inventory-sorting-persistence.md)

---

## 👤 Author

**Hamza Ihsan**  
Full-Stack & QA Automation Engineer  
- GitHub: [@hamzaihsan9](https://github.com/hamzaihsan9)
- Email: hamza.ihsan.f@gmail.com
