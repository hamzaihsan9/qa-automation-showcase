"""Global Pytest Fixtures and Configuration for UI and API Test Suites."""

import os
import pytest
from datetime import datetime
from typing import Dict, Any, Generator
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.api.client import BookingApiClient, ReqResApiClient


# --------------------------------------------------------------------------
# Configuration & Hooks
# --------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Ensure test artifacts and output directories exist prior to runs."""
    os.makedirs("test-results", exist_ok=True)
    os.makedirs("test-results/screenshots", exist_ok=True)


# --------------------------------------------------------------------------
# API Fixtures
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def booking_api() -> BookingApiClient:
    """Session-scoped Restful-Booker API client."""
    return BookingApiClient()


@pytest.fixture(scope="session")
def reqres_api() -> ReqResApiClient:
    """Session-scoped ReqRes API client with graceful public rate limit handling."""
    client = ReqResApiClient()
    original_send = client.session.send

    def safe_send(request, **kwargs):
        res = original_send(request, **kwargs)
        if res.status_code == 429:
            pytest.skip("ReqRes public sandbox returned HTTP 429 (Rate Limited)")
        return res

    client.session.send = safe_send
    return client


@pytest.fixture
def sample_booking_payload() -> Dict[str, Any]:
    """Factory fixture returning a fresh booking data payload."""
    return {
        "firstname": "Alex",
        "lastname": "Mercer",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-11-01",
            "checkout": "2026-11-08",
        },
        "additionalneeds": "Late Checkout & Breakfast",
    }


# --------------------------------------------------------------------------
# UI / POM Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Returns an unauthenticated LoginPage instance."""
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Returns an InventoryPage instance."""
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Returns a CartPage instance."""
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Returns a CheckoutPage instance."""
    return CheckoutPage(page)


@pytest.fixture
def authenticated_session(page: Page) -> InventoryPage:
    """Pre-authenticates as standard_user and yields ready inventory page."""
    login = LoginPage(page)
    login.load()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    try:
        page.wait_for_url("**/inventory.html", timeout=15000)
    except Exception:
        pass
    assert inv.is_loaded(), "Inventory page failed to load after login"
    return inv


# --------------------------------------------------------------------------
# HTML Report Hooks & Failure Screenshot Attachment
# --------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure for UI tests and attach to report."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        # Check if page fixture was active in the test
        page = item.funcargs.get("page")
        if page:
            os.makedirs("test-results/screenshots", exist_ok=True)
            screenshot_path = f"test-results/screenshots/{item.name}_{int(datetime.now().timestamp())}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                # Attach to pytest-html if available
                try:
                    import pytest_html
                    extra.append(pytest_html.extras.image(screenshot_path))
                except Exception:
                    pass
            except Exception:
                pass
    report.extra = extra


def pytest_html_report_title(report):
    """Custom title for Pytest HTML test execution report."""
    report.title = "QA Automation Showcase — Test Execution Report"
