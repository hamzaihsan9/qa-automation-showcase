"""UI Test Suite: End-to-End Checkout Workflow and Edge Cases."""

import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.smoke
class TestCheckoutE2E:
    """End-to-End purchasing scenarios and checkout validation rules."""

    def test_full_checkout_workflow_success(
        self,
        authenticated_session: InventoryPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        """Complete happy-path purchase from catalog to order confirmation."""
        inv = authenticated_session

        # 1. Add products
        item_1 = "sauce labs backpack"
        item_2 = "sauce labs bike light"
        inv.add_item_to_cart_by_name(item_1)
        inv.add_item_to_cart_by_name(item_2)
        assert inv.get_cart_count() == 2

        # 2. View cart
        inv.open_cart()
        assert cart_page.is_loaded()
        assert cart_page.get_cart_items_count() == 2
        cart_names = [n.lower() for n in cart_page.get_cart_item_names()]
        assert "sauce labs backpack" in cart_names
        assert "sauce labs bike light" in cart_names

        # 3. Proceed to Checkout Step One
        cart_page.proceed_to_checkout()

        # 4. Fill customer information
        checkout_page.fill_information(first_name="Jane", last_name="Doe", postal_code="94107")

        # 5. Review Step Two Totals
        totals = checkout_page.get_summary_totals()
        assert totals["subtotal"] > 0
        assert totals["tax"] > 0
        assert round(totals["subtotal"] + totals["tax"], 2) == round(totals["total"], 2)

        # 6. Finalize order
        checkout_page.finish_order()
        assert checkout_page.is_order_successful(), "Order confirmation message was not displayed"

    def test_checkout_step_one_missing_postal_code_validation(
        self,
        authenticated_session: InventoryPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        """Verify checkout form alerts user when postal code is missing."""
        inv = authenticated_session
        inv.add_item_to_cart_by_name("sauce labs onesie")
        inv.open_cart()
        cart_page.proceed_to_checkout()

        # Submit without postal code
        checkout_page.fill_information(first_name="Jane", last_name="Doe", postal_code="")
        assert "Postal Code is required" in checkout_page.get_error_message()

    def test_continue_shopping_navigation(
        self,
        authenticated_session: InventoryPage,
        cart_page: CartPage,
    ):
        """Verify user can abort cart and return seamlessly to catalog."""
        inv = authenticated_session
        inv.open_cart()
        assert cart_page.is_loaded()

        cart_page.continue_shopping()
        assert inv.is_loaded()
        assert "/inventory.html" in inv.get_current_url()
