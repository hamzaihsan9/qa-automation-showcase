"""Page Object for SauceDemo Checkout Workflows (Step 1, Step 2, and Confirmation)."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Encapsulates checkout user details, order review, and confirmation."""

    # Step 1 Selectors
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    ERROR_MESSAGE = '[data-test="error"]'

    # Step 2 Selectors
    ITEM_TOTAL_LABEL = '[data-test="subtotal-label"]'
    TAX_LABEL = '[data-test="tax-label"]'
    TOTAL_LABEL = '[data-test="total-label"]'
    FINISH_BUTTON = '[data-test="finish"]'

    # Complete Step Selectors
    COMPLETE_HEADER = '[data-test="complete-header"]'
    COMPLETE_TEXT = '[data-test="complete-text"]'
    BACK_HOME_BUTTON = '[data-test="back-to-products"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill customer details on Step One."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Fetch validation error on Step One."""
        return self.get_text(self.ERROR_MESSAGE)

    def get_summary_totals(self) -> dict:
        """Retrieve computed order price totals on Step Two."""
        subtotal_raw = self.get_text(self.ITEM_TOTAL_LABEL)
        tax_raw = self.get_text(self.TAX_LABEL)
        total_raw = self.get_text(self.TOTAL_LABEL)

        return {
            "subtotal": float(subtotal_raw.split("$")[-1].strip()),
            "tax": float(tax_raw.split("$")[-1].strip()),
            "total": float(total_raw.split("$")[-1].strip()),
        }

    def finish_order(self) -> None:
        """Click finish to finalize order."""
        self.click(self.FINISH_BUTTON)

    def is_order_successful(self) -> bool:
        """Check if order confirmation banner is present."""
        return (
            self.is_visible(self.COMPLETE_HEADER)
            and "thank you for your order" in self.get_text(self.COMPLETE_HEADER).lower()
        )
