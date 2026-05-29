# TC_CART_001 — Verify adding a single product to the cart

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CART_001 |
| **Title** | Verify adding a single product to the cart |
| **Priority** | High |
| **Test Scope** | Smoke Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that tapping "Add to Cart" on a product adds it to the shopping cart and updates the cart badge count.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page
- Cart is empty (no items previously added)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify the cart badge is not displayed (cart is empty) | No badge number is shown on the cart icon |
| 2 | Tap the "Add to Cart" button on the first product | Button text changes to "Remove" |
| 3 | Verify the cart badge updates to show "1" | Cart icon displays a badge with the number 1 |
| 4 | Tap the cart icon to navigate to the Cart page | Cart page loads and displays the added product with correct name and price |
