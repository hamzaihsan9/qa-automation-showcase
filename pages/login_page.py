"""Page Object for SauceDemo Authentication / Login Page."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates SauceDemo login elements and user workflows."""

    # Selectors
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'
    LOGIN_LOGO = '.login_logo'

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> None:
        """Open the SauceDemo login page directly."""
        self.navigate("")
        expect(self.find(self.LOGIN_BUTTON)).to_be_visible(timeout=15000)

    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit login form."""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Retrieve displayed error text upon invalid login."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Verify error container visibility."""
        return self.is_visible(self.ERROR_MESSAGE)
