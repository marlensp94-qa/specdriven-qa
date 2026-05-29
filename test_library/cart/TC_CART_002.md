# TC_CART_002 — Verify removing a product from the cart

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CART_002 |
| **Title** | Verify removing a product from the cart |
| **Priority** | High |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that tapping "Remove" on a cart item removes it from the cart and updates the cart badge accordingly.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page
- At least one product has been added to the cart

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Add a product to the cart from the Products page | Cart badge shows "1" |
| 2 | Tap the cart icon to navigate to the Cart page | Cart page displays the added product |
| 3 | Tap the "Remove" button next to the product in the cart | Product is removed from the cart list |
| 4 | Verify the cart is now empty and the badge is no longer displayed | Cart shows no items; cart badge disappears from the cart icon |
