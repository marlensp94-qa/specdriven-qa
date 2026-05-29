# Test Case: TC_LOGIN_001

## Test Case ID
TC_LOGIN_001

## Title
Valid login with standard user credentials

## Objective
Verify that a user can successfully log in with valid credentials and is redirected to the Products page.

## Preconditions
- Swag Labs application is installed on the Android emulator
- Emulator is running and Appium server is connected
- User is on the Login screen
- Valid credentials are available (standard_user / secret_sauce)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Launch the Swag Labs application | Login screen is displayed with username and password fields visible |
| 2 | Enter "standard_user" in the username field | Username field displays "standard_user" |
| 3 | Enter "secret_sauce" in the password field | Password field displays masked characters |
| 4 | Tap the LOGIN button | Application processes the login request |
| 5 | Observe the resulting screen | Products page is displayed with the "PRODUCTS" title visible |

## Priority
High

## Test Scope
Smoke Test

## Automation Status
automated

## Automation Dependency Category
A
