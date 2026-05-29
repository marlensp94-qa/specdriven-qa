# Test Case: Checkout with Missing Information

## Test Case ID
TC_CHECKOUT_002

## Title
Checkout fails when required shipping fields are empty

## Objective
Verify that the checkout process displays an error when required fields are left empty.

## Preconditions
- User is logged in with valid credentials (standard_user)
- At least one product has been added to the cart
- User is on the Checkout Information screen

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Leave all fields (First Name, Last Name, Zip Code) empty | Fields remain empty with no pre-filled values |
| 2 | Tap the "Continue" button | An error message is displayed indicating "First Name is required" |
| 3 | Enter first name only and tap "Continue" | An error message is displayed indicating "Last Name is required" |
| 4 | Enter first name and last name, leave zip code empty, tap "Continue" | An error message is displayed indicating "Postal Code is required" |

## Priority
High

## Test Scope
Mandatory Regression Test

## Automation Status
automated

## Automation Dependency Category
A
