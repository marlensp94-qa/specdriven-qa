# Test Case: TC_LOGIN_003

## Test Case ID
TC_LOGIN_003

## Title
Login fails for locked out user account

## Objective
Verify that a locked out user cannot log in and receives an appropriate locked account error message.

## Preconditions
- Swag Labs application is installed on the Android emulator
- Emulator is running and Appium server is connected
- User is on the Login screen
- Locked out user credentials are available (locked_out_user / secret_sauce)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Enter "locked_out_user" in the username field | Username field displays "locked_out_user" |
| 2 | Enter "secret_sauce" in the password field | Password field displays masked characters |
| 3 | Tap the LOGIN button | Application attempts to authenticate |
| 4 | Observe the error message displayed | Error message "Sorry, this user has been locked out" is shown |
| 5 | Verify the user remains on the Login screen | Login screen is still displayed with the error message visible |

## Priority
High

## Test Scope
Mandatory Regression Test

## Automation Status
automated

## Automation Dependency Category
A
