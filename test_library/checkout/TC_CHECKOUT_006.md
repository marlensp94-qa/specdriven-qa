# Test Case: Continue Shopping from Cart During Checkout

## Test Case ID
TC_CHECKOUT_006

## Title
Continue shopping from cart navigates back to products catalog

## Objective
Verify that tapping Continue Shopping from the cart returns the user to the catalog.

## Preconditions
- User is logged in with valid credentials (standard_user)
- At least one product has been added to the cart
- User is on the Cart screen (pre-checkout)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify the Cart screen is displayed with items | Cart items are listed with product names and prices |
| 2 | Tap the "Continue Shopping" button | User is navigated back to the Products screen |
| 3 | Verify the Products screen is displayed | Product catalog is visible with all available items |
| 4 | Tap the cart icon to return to cart | Cart still contains the previously added items |

## Priority
Normal

## Test Scope
Extended Regression Test

## Automation Status
automated

## Automation Dependency Category
A
