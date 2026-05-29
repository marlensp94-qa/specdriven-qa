# Test Case: Verify Checkout Totals

## Test Case ID
TC_CHECKOUT_004

## Title
Checkout overview displays correct item total, tax, and grand total

## Objective
Verify that the Checkout Overview screen calculates and displays correct pricing.

## Preconditions
- User is logged in with valid credentials (standard_user)
- One or more products with known prices have been added to the cart
- User has entered valid checkout information and is on the Checkout Overview screen

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify the item subtotal is displayed on the Checkout Overview screen | Item Total matches the sum of individual product prices in the cart |
| 2 | Verify the tax amount is displayed | Tax is calculated and displayed as a non-negative value |
| 3 | Verify the grand total is displayed | Total equals Item Total plus Tax amount |
| 4 | Compare displayed product names and prices with items added to cart | Each product name and price matches what was added to the cart |

## Priority
Normal

## Test Scope
Mandatory Regression Test

## Automation Status
planned

## Automation Dependency Category
A
