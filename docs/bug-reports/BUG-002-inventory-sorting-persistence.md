# Bug Report: BR-002 — Catalog Sort State Resets on Back Navigation

**Severity:** Low / UX Glitch  
**Priority:** Medium  
**Component:** Catalog / Inventory UI  
**Environment:** All Browsers (Chromium, Firefox, WebKit)  
**Reporter:** Hamza Ihsan (QA Automation Lead)  
**Status:** Open  

---

### Description
When a user sorts products (e.g., Price low to high `lohi` or Price high to low `hilo`), clicks into the shopping cart, and clicks the **Continue Shopping** button, the catalog view resets to the default sorting order (`az` - Name A to Z). The sort dropdown indicator and internal sorting order should persist across intra-session navigation.

---

### Steps to Reproduce
1. Log in to `https://www.saucedemo.com/`.
2. Select **Price (low to high)** from the filter dropdown (`[data-test="product-sort-container"]`).
3. Confirm catalog is sorted with `$7.99` item (Sauce Labs Onesie) first.
4. Click the Cart button (`[data-test="shopping-cart-link"]`).
5. In the cart page, click the **Continue Shopping** button (`[data-test="continue-shopping"]`).
6. Observe catalog ordering upon return.

---

### Expected Result
The catalog should retain the user's previously selected filter preference (`Price (low to high)`), or the query param `?sort=lohi` should be preserved in the browser history.

### Actual Result
Catalog resets to default `az` (A to Z) ordering without maintaining the user's selection context.

---

### Automated Test Coverage
- **Automated Test:** `tests/ui/test_inventory.py::TestInventory::test_sort_price_low_to_high`
- **Navigation Verification:** `tests/ui/test_checkout_e2e.py::TestCheckoutE2E::test_continue_shopping_navigation`
