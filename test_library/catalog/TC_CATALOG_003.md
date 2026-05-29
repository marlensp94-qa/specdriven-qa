# TC_CATALOG_003 — Verify sorting products by price low to high

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CATALOG_003 |
| **Title** | Verify sorting products by price low to high |
| **Priority** | Normal |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that selecting the "Price (low to high)" sort option orders products by ascending price value.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the sort dropdown/filter icon on the Products page | Sort options menu is displayed |
| 2 | Select "Price (low to high)" from the sort options | Products list reorders by price ascending |
| 3 | Read the prices from top to bottom and compare each consecutive pair | Each product price is less than or equal to the next product's price |
| 4 | Verify the cheapest item appears first and the most expensive appears last | First item shows the lowest price ($7.99); last item shows the highest price ($49.99) |
