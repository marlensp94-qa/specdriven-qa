# Test Case: Cancel Checkout

## Test Case ID
TC_CHECKOUT_003

## Title
Cancel checkout returns user to the Cart screen

## Objective
Verify that canceling the checkout process navigates the user back to the Cart screen.

## Preconditions
- User is logged in with valid credentials (standard_user)
- At least one product has been added to the cart
- User is on the Checkout Information screen

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify the Checkout Information screen is displayed | First Name, Last Name, and Zip Code fields are visible |
| 2 | Optionally enter partial information in the fields | Fields accept input (this step verifies data is not persisted) |
| 3 | Tap the "Cancel" button | User is navigated back to the Cart screen |
| 4 | Verify the cart still contains the previously added items | Cart items are unchanged and displayed correctly |

## Priority
High

## Test Scope
Mandatory Regression Test

## Automation Status
automated

## Automation Dependency Category
A
