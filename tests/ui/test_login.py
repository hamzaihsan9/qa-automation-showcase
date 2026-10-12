"""UI Test Suite: User Authentication & Session Scenarios (SauceDemo)."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    """Test login functionality across valid, invalid, and edge-case inputs."""

    def test_successful_login(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Verify standard user can log in and view product catalog."""
        login_page.load()
        login_page.login("standard_user", "secret_sauce")
        for _ in range(5):
            if inventory_page.is_loaded():
                break
            login_page.page.wait_for_timeout(500)

        assert inventory_page.is_loaded(), "Inventory page did not display after standard login"
        assert "/inventory.html" in inventory_page.get_current_url()

    def test_locked_out_user(self, login_page: LoginPage):
        """Verify locked-out user receives prominent lockout notification."""
        login_page.load()
        login_page.login("locked_out_user", "secret_sauce")

        assert login_page.is_error_displayed()
        error_text = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_text

    def test_invalid_password(self, login_page: LoginPage):
        """Verify authentication failure with incorrect password."""
        login_page.load()
        login_page.login("standard_user", "wrong_sauce_123")

        assert login_page.is_error_displayed()
        assert "Username and password do not match" in login_page.get_error_message()

    def test_empty_username_validation(self, login_page: LoginPage):
        """Verify client-side validation requires username."""
        login_page.load()
        login_page.login("", "secret_sauce")

        assert login_page.is_error_displayed()
        assert "Username is required" in login_page.get_error_message()

    def test_empty_password_validation(self, login_page: LoginPage):
        """Verify client-side validation requires password."""
        login_page.load()
        login_page.login("standard_user", "")

        assert login_page.is_error_displayed()
        assert "Password is required" in login_page.get_error_message()

    def test_user_logout(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Verify user can log out securely via navigation drawer."""
        login_page.load()
        login_page.login("standard_user", "secret_sauce")
        assert inventory_page.is_loaded()

        inventory_page.logout()
        for _ in range(5):
            if login_page.is_visible(login_page.LOGIN_BUTTON):
                break
            login_page.page.wait_for_timeout(500)
        assert login_page.is_visible(login_page.LOGIN_BUTTON)
