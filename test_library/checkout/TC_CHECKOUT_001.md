# Test Case: Complete Checkout Flow

## Test Case ID
TC_CHECKOUT_001

## Title
Complete checkout with valid shipping information

## Objective
Verify that a user can complete the full checkout process with valid information.

## Preconditions
- User is logged in with valid credentials (standard_user)
- At least one product has been added to the cart
- User is on the Cart screen

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the "Checkout" button on the Cart screen | Checkout Information screen is displayed with First Name, Last Name, and Zip Code fields |
| 2 | Enter valid first name, last name, and zip code | All fields accept input and display entered text correctly |
| 3 | Tap the "Continue" button | Checkout Overview screen is displayed showing order summary |
| 4 | Verify the item name, price, and total are displayed correctly | Item details match the product added to cart, total includes tax |
| 5 | Tap the "Finish" button | Checkout Complete screen is displayed with "Thank you for your order" confirmation message |

## Priority
High

## Test Scope
Smoke Test

## Automation Status
automated

## Automation Dependency Category
A
