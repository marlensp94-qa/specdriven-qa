# TC_CATALOG_001 — Verify product listing displays all items

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CATALOG_001 |
| **Title** | Verify product listing displays all items |
| **Priority** | High |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that the products page displays all available Swag Labs inventory items after successful login.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User has valid credentials (standard_user / secret_sauce)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Launch the Swag Labs app and log in with standard_user credentials | User is redirected to the Products page |
| 2 | Observe the products list on the main catalog screen | All 6 inventory items are displayed with name, price, and image |
| 3 | Scroll down to verify all products are accessible | All products are visible and no items are missing from the list |
| 4 | Verify each product has an "Add to Cart" button | Each product card shows an active "Add to Cart" button |
