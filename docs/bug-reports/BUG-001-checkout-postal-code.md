# Bug Report: BR-001 — Inconsistent Validation Formatting on Checkout Step One

**Severity:** Low / Cosmetic  
**Priority:** Medium  
**Component:** Checkout Subsystem / UI Form  
**Environment:** Linux (Ubuntu/Debian/Kali), Chrome 124+, Firefox, WebKit  
**Reporter:** Hamza Ihsan (QA Automation Lead)  
**Status:** Open  

---

### Description
When submitting the checkout customer details form without providing a Postal Code, the error message rendered reads:
> `Error: Postal Code is required`

However, the field label placeholder is simply `Zip/Postal Code`. For international shoppers without standard ZIP nomenclature, the inconsistency between input placeholder hints and strict validation error phrasing causes confusion. Furthermore, trailing whitespaces in the postal code field are not automatically trimmed prior to client submission.

---

### Steps to Reproduce
1. Navigate to `https://www.saucedemo.com/` and log in with `standard_user` / `secret_sauce`.
2. Add any catalog item (e.g., `Sauce Labs Backpack`) to the cart.
3. Click the Shopping Cart icon in the upper right.
4. Click the **Checkout** button.
5. In First Name enter `Jane`, in Last Name enter `Doe`.
6. Leave Postal Code empty (or enter spaces only: `"   "`).
7. Click the **Continue** button.

---

### Expected Result
1. Whitespaces should be stripped during sanitation.
2. The error message should clearly indicate: `"Postal Code / Zip Code is required"` matching the form label.

### Actual Result
Error toast banner displays: `"Error: Postal Code is required"` without trimming spaces, and error icon displays misaligned on ultra-narrow viewports (<360px).

---

### Automated Test Coverage
- **Automated Test:** `tests/ui/test_checkout_e2e.py::TestCheckoutE2E::test_checkout_step_one_missing_postal_code_validation`
- **Assertion:** `assert "Postal Code is required" in checkout_page.get_error_message()`
