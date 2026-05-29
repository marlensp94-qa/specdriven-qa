# TC_CART_005 — Verify removing product from cart via Products page

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CART_005 |
| **Title** | Verify removing product from cart via Products page |
| **Priority** | Normal |
| **Test Scope** | Extended Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that tapping "Remove" on a product from the Products page (after it was added) removes it from the cart and updates the badge.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page
- Cart is empty (no items previously added)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap "Add to Cart" on a product from the Products page | Button changes to "Remove" and cart badge shows "1" |
| 2 | Tap the "Remove" button on the same product from the Products page | Button changes back to "Add to Cart" |
| 3 | Verify the cart badge is no longer displayed | Cart icon shows no badge number |
| 4 | Tap the cart icon to navigate to the Cart page | Cart page loads and shows an empty cart with no items listed |
