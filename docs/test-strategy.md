# Quality Assurance & Test Automation Strategy

## 1. Executive Overview
This document defines the test automation framework architecture and quality engineering strategy implemented in `qa-automation-showcase`. The solution demonstrates enterprise-grade testing patterns for full-stack web applications, combining **Playwright (Python)** for browser automation and **Pytest** for REST API validation.

---

## 2. Test Automation Pyramid

```
           / \
          /   \
         / E2E \         UI & Journey Tests (Playwright POM)
        /  UI   \        - Authentication, Shopping Cart, Checkout E2E
       /---------\
      /   API     \      Integration & Contract API Tests (REST / JSON)
     / Integration \     - Restful-Booker CRUD, ReqRes User Operations
    /---------------\
   /   Unit Tests    \   Data models, helper validations, payload sanitizers
  /-------------------\
```

- **API Layer (Integration & Contract):** Tests microservice boundaries, HTTP response codes, JSON schemas, payload mutations, and authentication headers using session-pooled HTTP clients. Fast execution (~15s for full suite).
- **UI Layer (End-to-End):** Tests real user interactions via headless/headed Chromium browsers using the Page Object Model (POM) to ensure separation of UI selectors from business assertions.

---

## 3. Page Object Model (POM) Architecture

All UI tests adhere strictly to the POM design pattern located under `pages/`:

| Page Object | Responsibilities | Key Methods |
|:---|:---|:---|
| [`BasePage`](file:///home/kali/qa-automation-showcase/pages/base_page.py) | Common Playwright primitives, explicit waits, navigation | `navigate()`, `click()`, `fill()`, `get_text()`, `is_visible()` |
| [`LoginPage`](file:///home/kali/qa-automation-showcase/pages/login_page.py) | Form authentication, error handling | `load()`, `login()`, `get_error_message()` |
| [`InventoryPage`](file:///home/kali/qa-automation-showcase/pages/inventory_page.py) | Product catalog, dynamic sorting, cart counters | `get_all_item_names()`, `select_sort_option()`, `add_item_to_cart_by_name()` |
| [`CartPage`](file:///home/kali/qa-automation-showcase/pages/cart_page.py) | Item review, removals, checkout handoff | `get_cart_item_names()`, `remove_item()`, `proceed_to_checkout()` |
| [`CheckoutPage`](file:///home/kali/qa-automation-showcase/pages/checkout_page.py) | Multi-step shipping and tax calculations | `fill_information()`, `get_summary_totals()`, `finish_order()` |

---

## 4. Test Categories & Pytest Markers

Tests are categorized using Pytest markers defined in `pytest.ini`:

- `@pytest.mark.smoke`: Critical path validation (< 1 min execution) intended for pre-merge commit hooks.
- `@pytest.mark.regression`: Comprehensive suite covering edge cases, negative assertions, and validation errors.
- `@pytest.mark.api`: Backend REST API integration tests.
- `@pytest.mark.ui`: Browser automation tests running via Playwright.
- `@pytest.mark.e2e`: Multi-step user journeys traversing end-to-end purchasing flows.

---

## 5. Defect Management & Severity Criteria

All detected issues are filed under `docs/bug-reports/` using the following severity model:

- **Critical / Blocker (P0):** Application crash, financial miscalculation, checkout deadlock.
- **Major (P1):** Core feature non-functional with no workaround (e.g., login failure for specific user tiers).
- **Minor / Low (P2/P3):** Formatting inconsistency, sort order persistence glitch, localization issues.

---

## 6. Continuous Integration (CI/CD) Quality Gate

Every Pull Request and trunk push triggers `.github/workflows/qa-ci.yml`:
1. Environment setup on `ubuntu-latest`.
2. Python dependency caching.
3. Headless Chromium installation via `playwright install --with-deps`.
4. Stage 1: Smoke test verification (`pytest -m smoke`).
5. Stage 2: Full regression test execution with `--html=report.html`.
6. Artifact archiving with a 14-day retention window.
