# TC_CART_004 — Verify continue shopping returns to products page

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CART_004 |
| **Title** | Verify continue shopping returns to products page |
| **Priority** | Normal |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that tapping "Continue Shopping" from the cart page navigates the user back to the Products page with the catalog intact.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user
- At least one product has been added to the cart

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Add a product to the cart from the Products page | Cart badge shows "1" |
| 2 | Tap the cart icon to navigate to the Cart page | Cart page loads with the added product visible |
| 3 | Tap the "Continue Shopping" button | User is navigated back to the Products page |
| 4 | Verify the Products page displays all items and the cart badge still shows "1" | All 6 products are listed and the cart badge retains the count |
