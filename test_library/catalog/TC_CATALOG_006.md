# TC_CATALOG_006 — Verify sorting products by price high to low

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CATALOG_006 |
| **Title** | Verify sorting products by price high to low |
| **Priority** | Normal |
| **Test Scope** | Extended Regression Test |
| **Automation Status** | planned |
| **Automation Dependency** | A |

## Objective

Verify that selecting the "Price (high to low)" sort option orders products by descending price value.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the sort dropdown/filter icon on the Products page | Sort options menu is displayed |
| 2 | Select "Price (high to low)" from the sort options | Products list reorders by price descending |
| 3 | Read the prices from top to bottom and compare each consecutive pair | Each product price is greater than or equal to the next product's price |
| 4 | Verify the most expensive item appears first and the cheapest appears last | First item shows the highest price ($49.99); last item shows the lowest price ($7.99) |
