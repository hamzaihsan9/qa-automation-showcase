"""Page Object for SauceDemo Shopping Cart Page."""

from typing import List
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates Cart interactions, item reviews, and checkout progression."""

    # Selectors
    PAGE_TITLE = '[data-test="title"]'
    CART_ITEMS = '[data-test="inventory-item"]'
    CART_ITEM_NAMES = '[data-test="inventory-item-name"]'
    CART_ITEM_PRICES = '[data-test="inventory-item-price"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        """Verify cart page is visible and ready."""
        return self.is_visible(self.PAGE_TITLE) and self.get_text(self.PAGE_TITLE) == "Your Cart"

    def get_cart_items_count(self) -> int:
        """Return number of item rows in cart."""
        return self.find(self.CART_ITEMS).count()

    def get_cart_item_names(self) -> List[str]:
        """Return product names inside the cart."""
        return self.find(self.CART_ITEM_NAMES).all_inner_texts()

    def remove_item(self, product_name: str) -> None:
        """Remove item from cart by product name."""
        slug = product_name.lower().replace(" ", "-")
        self.click(f'[data-test="remove-{slug}"]')

    def proceed_to_checkout(self) -> None:
        """Click checkout to move to shipping info step."""
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Return to inventory catalog."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
