# Test Case: TC_LOGIN_005

## Test Case ID
TC_LOGIN_005

## Title
User can log out and return to the Login screen

## Objective
Verify that a logged-in user can successfully log out via the side menu and is returned to the Login screen.

## Preconditions
- Swag Labs application is installed on the Android emulator
- Emulator is running and Appium server is connected
- User is logged in with valid credentials (standard_user / secret_sauce)
- Products page is displayed

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the hamburger menu icon in the top-left corner | Side navigation menu slides open |
| 2 | Tap the "LOGOUT" option in the side menu | Application processes the logout request |
| 3 | Observe the resulting screen | Login screen is displayed with empty username and password fields |
| 4 | Verify the LOGIN button is visible and enabled | LOGIN button is present and tappable |

## Priority
High

## Test Scope
Mandatory Regression Test

## Automation Status
planned

## Automation Dependency Category
D
