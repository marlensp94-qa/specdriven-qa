# Test Case: TC_LOGIN_002

## Test Case ID
TC_LOGIN_002

## Title
Login fails with invalid password for valid username

## Objective
Verify that login is rejected when an incorrect password is provided for a valid username, and an appropriate error message is displayed.

## Preconditions
- Swag Labs application is installed on the Android emulator
- Emulator is running and Appium server is connected
- User is on the Login screen

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Enter "standard_user" in the username field | Username field displays "standard_user" |
| 2 | Enter "wrong_password" in the password field | Password field displays masked characters |
| 3 | Tap the LOGIN button | Application attempts to authenticate |
| 4 | Observe the error message displayed | Error message "Username and password do not match any user in this service" is shown |
| 5 | Verify the user remains on the Login screen | Login screen is still displayed with username and password fields |

## Priority
High

## Test Scope
Mandatory Regression Test

## Automation Status
automated

## Automation Dependency Category
A
