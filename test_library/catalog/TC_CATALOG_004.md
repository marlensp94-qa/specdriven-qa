# TC_CATALOG_004 — Verify product detail page displays correct information

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CATALOG_004 |
| **Title** | Verify product detail page displays correct information |
| **Priority** | High |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that tapping a product from the catalog opens the product detail page with the correct name, description, price, and image.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Identify a product on the Products page and note its name and price | Product name and price are visible on the catalog card |
| 2 | Tap on the product name or image to open the detail view | Product detail page loads with the product title displayed |
| 3 | Verify the product name, description, and price on the detail page | Name and price match the catalog listing; description text is present and non-empty |
| 4 | Verify the "Add to Cart" button is displayed on the detail page | An active "Add to Cart" button is visible |
| 5 | Tap the back button to return to the Products page | User is returned to the Products page with all items still listed |
