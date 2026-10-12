"""Page Object for SauceDemo Inventory / Products Catalog Page."""

from typing import List
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Encapsulates SauceDemo catalog navigation, sorting, and cart actions."""

    # Selectors
    PAGE_TITLE = '[data-test="title"]'
    INVENTORY_ITEMS = '[data-test="inventory-item"]'
    ITEM_NAMES = '[data-test="inventory-item-name"]'
    ITEM_PRICES = '[data-test="inventory-item-price"]'
    SORT_DROPDOWN = '[data-test="product-sort-container"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    CART_LINK = '[data-test="shopping-cart-link"]'
    BURGER_MENU = '#react-burger-menu-btn'
    LOGOUT_LINK = '#logout_sidebar_link'

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        """Verify inventory page has fully loaded."""
        return self.is_visible(self.PAGE_TITLE) and self.get_text(self.PAGE_TITLE) == "Products"

    def get_item_count(self) -> int:
        """Count currently rendered catalog items."""
        return self.find(self.INVENTORY_ITEMS).count()

    def get_all_item_names(self) -> List[str]:
        """Fetch all product names listed in the inventory."""
        return self.find(self.ITEM_NAMES).all_inner_texts()

    def get_all_item_prices(self) -> List[float]:
        """Fetch all product prices as float numbers."""
        raw_prices = self.find(self.ITEM_PRICES).all_inner_texts()
        return [float(p.replace("$", "").strip()) for p in raw_prices]

    def add_item_to_cart_by_index(self, index: int = 0) -> None:
        """Add specific item to cart by index."""
        button = self.find(self.INVENTORY_ITEMS).nth(index).locator('button[data-test^="add-to-cart"]')
        button.click()

    def add_item_to_cart_by_name(self, product_name: str) -> None:
        """Add item matching product name to cart."""
        slug = product_name.lower().replace(" ", "-")
        self.click(f'[data-test="add-to-cart-{slug}"]')

    def remove_item_from_cart_by_name(self, product_name: str) -> None:
        """Remove item matching product name from cart."""
        slug = product_name.lower().replace(" ", "-")
        self.click(f'[data-test="remove-{slug}"]')

    def get_cart_count(self) -> int:
        """Return the count displayed on the shopping cart badge."""
        if self.is_visible(self.CART_BADGE, timeout=1000):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def open_cart(self) -> None:
        """Navigate to cart view."""
        self.click(self.CART_LINK)

    def select_sort_option(self, option_value: str) -> None:
        """Select sorting order: 'az', 'za', 'lohi', 'hilo' with dynamic DOM wait."""
        self.find(self.SORT_DROPDOWN).select_option(option_value)
        # Wait dynamically for DOM re-order to settle
        for _ in range(10):
            self.page.wait_for_timeout(200)
            items = self.find(self.ITEM_NAMES).all_inner_texts()
            if items:
                if option_value == "az" and items[0].startswith("Sauce Labs B"):
                    break
                elif option_value == "za" and items[0].startswith("Test"):
                    break
                elif option_value == "lohi" and self.get_all_item_prices()[0] < 10.0:
                    break
                elif option_value == "hilo" and self.get_all_item_prices()[0] > 40.0:
                    break

    def logout(self) -> None:
        """Perform user logout through burger navigation drawer."""
        self.click(self.BURGER_MENU)
        self.find(self.LOGOUT_LINK).wait_for(state="visible", timeout=5000)
        self.click(self.LOGOUT_LINK)
