"""Base Page Object containing shared browser interactions and assertions."""

from typing import Optional
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Foundational Page Object Model base class."""

    def __init__(self, page: Page, base_url: str = "https://www.saucedemo.com"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "") -> None:
        """Navigate to relative or absolute path with automatic retry on network lag."""
        url = f"{self.base_url}/{path}".rstrip("/") if not path.startswith("http") else path
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=45000)
        except Exception:
            self.page.goto(url, wait_until="domcontentloaded", timeout=45000)

    def get_title(self) -> str:
        """Return the current document title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return current browser page URL."""
        return self.page.url

    def find(self, selector: str) -> Locator:
        """Return locator for given selector."""
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        """Wait for selector and perform click."""
        self.find(selector).click()

    def fill(self, selector: str, text: str) -> None:
        """Wait for selector and fill text."""
        self.find(selector).fill(text)

    def get_text(self, selector: str) -> str:
        """Get trimmed inner text of element."""
        return self.find(selector).inner_text().strip()

    def is_visible(self, selector: str, timeout: float = 3000) -> bool:
        """Check element visibility within timeout."""
        try:
            self.find(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_url_contains(self, fragment: str, timeout: float = 5000) -> None:
        """Wait until browser URL contains string fragment."""
        self.page.wait_for_url(lambda u: fragment in u, timeout=timeout)
