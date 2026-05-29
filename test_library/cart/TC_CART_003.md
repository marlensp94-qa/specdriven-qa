# TC_CART_003 — Verify cart badge updates with multiple items

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CART_003 |
| **Title** | Verify cart badge updates with multiple items |
| **Priority** | High |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that the cart badge count increments correctly when multiple products are added to the cart.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page
- Cart is empty (no items previously added)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap "Add to Cart" on the first product | Cart badge shows "1" |
| 2 | Tap "Add to Cart" on the second product | Cart badge updates to show "2" |
| 3 | Tap "Add to Cart" on the third product | Cart badge updates to show "3" |
| 4 | Tap the cart icon to navigate to the Cart page | Cart page displays all 3 added products with correct names and prices |
| 5 | Verify the total number of items in the cart matches the badge count | Three distinct product entries are listed in the cart |
