# TC_CATALOG_002 — Verify sorting products by name A to Z

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | TC_CATALOG_002 |
| **Title** | Verify sorting products by name A to Z |
| **Priority** | High |
| **Test Scope** | Mandatory Regression Test |
| **Automation Status** | automated |
| **Automation Dependency** | A |

## Objective

Verify that selecting the "Name (A to Z)" sort option orders products alphabetically in ascending order.

## Preconditions

- Swag Labs APK is installed on the Android emulator
- Appium server is running and connected
- User is logged in as standard_user and on the Products page

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the sort dropdown/filter icon on the Products page | Sort options menu is displayed |
| 2 | Select "Name (A to Z)" from the sort options | Products list reorders alphabetically ascending |
| 3 | Read the product names from top to bottom | First product starts with "A" or earliest letter; last product starts with latest letter |
| 4 | Verify all 6 products remain visible after sorting | Product count remains unchanged and no items are duplicated or missing |
