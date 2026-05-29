# TC_CART_006 — Verify cart persists items after navigating away

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CART_006 |
| **Title** | Verify cart persists items after navigating away |
| **Priority** | Normal |
| **Test Scope** | Extended Regression Test |
| **Automation Status** | planned |
| **Automation Dependency** | D |

## Objective

Verify that items added to the cart remain in the cart after navigating to product details and back to the Products page.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page
- Cart is empty (no items previously added)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap "Add to Cart" on a product from the Products page | Cart badge shows "1" |
| 2 | Tap on a different product to open its detail page | Product detail page loads |
| 3 | Tap the back button to return to the Products page | Products page loads with the first product still showing "Remove" |
| 4 | Tap the cart icon to navigate to the Cart page | Cart page displays the originally added product with correct name and price |
