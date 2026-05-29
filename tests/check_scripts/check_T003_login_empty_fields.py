"""
check_T003_login_empty_fields — Demo_QA
==========================================
Regression test: Login with empty username and password fields.

Preconditions:
    - App is launched and on the Login screen

Steps:
    1. Leave username field empty
    2. Leave password field empty
    3. Tap Login button
    4. Verify error message is displayed

Expected Results:
    - Login is rejected
    - An error message is displayed indicating credentials are required

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from framework.pages.login_page import LoginPage
from framework.utils.markers import component, test_type as mark_test_type, priority


@pytest.mark.regression
@component("Login")
@mark_test_type("negative")
@priority("medium")
def check_T003_login_empty_fields(driver):
    """Verify that submitting empty username and password shows an error."""
    login_page = LoginPage(driver)

    # Attempt login with empty credentials
    error_message = login_page.login_expecting_error("", "")

    # Verify error is displayed
    assert login_page.is_error_displayed(), (
        "Expected an error message when submitting empty credentials"
    )
    assert error_message != "", (
        "Error message should not be empty for blank credentials"
    )
