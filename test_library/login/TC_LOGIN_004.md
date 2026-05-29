# Test Case: TC_LOGIN_004

## Test Case ID
TC_LOGIN_004

## Title
Login fails when username and password fields are empty

## Objective
Verify that submitting the login form with empty fields displays a validation error requesting credentials.

## Preconditions
- Swag Labs application is installed on the Android emulator
- Emulator is running and Appium server is connected
- User is on the Login screen
- Username and password fields are empty (default state)

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Verify that the username field is empty | Username field contains no text |
| 2 | Verify that the password field is empty | Password field contains no text |
| 3 | Tap the LOGIN button without entering any credentials | Application attempts form validation |
| 4 | Observe the error message displayed | Error message "Username is required" is shown |
| 5 | Verify the user remains on the Login screen | Login screen is still displayed with the error message visible |

## Priority
Normal

## Test Scope
Mandatory Regression Test

## Automation Status
automated

## Automation Dependency Category
A
