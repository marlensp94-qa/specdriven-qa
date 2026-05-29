"""
check_T002_login_invalid_credentials — Demo_QA
=================================================
Regression test: Login with locked_out_user credentials.

Preconditions:
    - App is launched and on the Login screen
    - locked_out_user credentials are available in constants

Steps:
    1. Enter locked_out_user username
    2. Enter locked_out_user password
    3. Tap Login button
    4. Verify error message is displayed

Expected Results:
    - Login is rejected
    - An error message is displayed indicating the user is locked out

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from framework.pages.login_page import LoginPage
from framework.utils.constants import TEST_USER_LOCKED, TEST_PASSWORD_LOCKED
from framework.utils.markers import component, test_type as mark_test_type, priority


@pytest.mark.regression
@component("Login")
@mark_test_type("negative")
@priority("high")
def check_T002_login_invalid_credentials(driver):
    """Verify that a locked-out user cannot log in and sees an error message."""
    login_page = LoginPage(driver)

    # Attempt login with locked_out_user credentials
    error_message = login_page.login_expecting_error(
        TEST_USER_LOCKED, TEST_PASSWORD_LOCKED
    )

    # Verify error is displayed
    assert login_page.is_error_displayed(), (
        "Expected an error message after locked_out_user login attempt"
    )
    assert error_message != "", (
        "Error message should not be empty for locked_out_user"
    )
