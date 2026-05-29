# TC_CATALOG_005 — Verify sorting products by name Z to A

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CATALOG_005 |
| **Title** | Verify sorting products by name Z to A |
| **Priority** | Normal |
| **Test Scope** | Extended Regression Test |
| **Automation Status** | planned |
| **Automation Dependency** | A |

## Objective

Verify that selecting the "Name (Z to A)" sort option orders products alphabetically in descending order.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the sort dropdown/filter icon on the Products page | Sort options menu is displayed |
| 2 | Select "Name (Z to A)" from the sort options | Products list reorders alphabetically descending |
| 3 | Read the product names from top to bottom | First product starts with the latest letter; last product starts with "A" or earliest letter |
| 4 | Verify all 6 products remain visible after sorting | Product count remains unchanged and no items are duplicated or missing |
