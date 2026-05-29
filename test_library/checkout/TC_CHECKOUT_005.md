# Test Case: Order Confirmation and Return to Products

## Test Case ID
TC_CHECKOUT_005

## Title
Order confirmation screen displays success and allows return to products

## Objective
Verify that the order confirmation screen shows a success message and navigates back.

## Preconditions
- User is logged in with valid credentials (standard_user)
- User has completed the full checkout flow (information entered, order finished)
- User is on the Checkout Complete screen

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify the Checkout Complete screen is displayed | "Thank you for your order" header text is visible |
| 2 | Verify a confirmation message or image is shown | A confirmation icon or descriptive text is displayed below the header |
| 3 | Tap the "Back Home" button | User is navigated back to the Products screen |
| 4 | Verify the Products screen is displayed with the product catalog | Products list is visible and the cart badge is reset (no items) |

## Priority
Normal

## Test Scope
Mandatory Regression Test

## Automation Status
planned

## Automation Dependency Category
A
