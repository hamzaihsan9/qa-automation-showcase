"""UI Test Suite: Inventory Catalog, Sorting, and Cart Badge Interactions."""

import pytest
from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.regression
class TestInventory:
    """Test product browsing, dynamic filtering/sorting, and cart indicators."""

    def test_catalog_displays_all_default_products(self, authenticated_session: InventoryPage):
        """Verify the store catalog displays exactly 6 products."""
        inv = authenticated_session
        assert inv.get_item_count() == 6
        names = inv.get_all_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bike Light" in names

    def test_sort_alphabetical_ascending(self, authenticated_session: InventoryPage):
        """Verify sorting products from A to Z."""
        inv = authenticated_session
        inv.select_sort_option("az")
        names = inv.get_all_item_names()
        assert names == sorted(names), "Product names are not in ascending alphabetical order"

    def test_sort_alphabetical_descending(self, authenticated_session: InventoryPage):
        """Verify sorting products from Z to A."""
        inv = authenticated_session
        inv.select_sort_option("za")
        names = inv.get_all_item_names()
        assert names == sorted(names, reverse=True), "Product names are not in descending alphabetical order"

    def test_sort_price_low_to_high(self, authenticated_session: InventoryPage):
        """Verify price sorting in ascending order."""
        inv = authenticated_session
        inv.select_sort_option("lohi")
        prices = inv.get_all_item_prices()
        assert prices == sorted(prices), "Prices are not sorted from low to high"

    def test_sort_price_high_to_low(self, authenticated_session: InventoryPage):
        """Verify price sorting in descending order."""
        inv = authenticated_session
        inv.select_sort_option("hilo")
        prices = inv.get_all_item_prices()
        assert prices == sorted(prices, reverse=True), "Prices are not sorted from high to low"

    def test_cart_badge_updates_on_add_and_remove(self, authenticated_session: InventoryPage):
        """Verify shopping cart badge dynamically reflects cart modifications."""
        inv = authenticated_session
        assert inv.get_cart_count() == 0

        # Add first item
        inv.add_item_to_cart_by_name("sauce labs backpack")
        assert inv.get_cart_count() == 1

        # Add second item
        inv.add_item_to_cart_by_name("sauce labs bike light")
        assert inv.get_cart_count() == 2

        # Remove an item
        inv.remove_item_from_cart_by_name("sauce labs backpack")
        assert inv.get_cart_count() == 1
