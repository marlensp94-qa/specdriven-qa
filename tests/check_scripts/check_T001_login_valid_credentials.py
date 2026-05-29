"""
check_T001_login_valid_credentials — Demo_QA
===============================================
Smoke test: Verify that a standard user can log in with valid credentials.

Preconditions:
    - Swag Labs app is installed and launched on the emulator
    - App is on the Login screen
    - standard_user credentials are valid (bod@example.com / 10203040)

Steps:
    1. Enter valid username (standard_user) in the username field
    2. Enter valid password in the password field
    3. Tap the Login button
    4. Verify the Products screen is displayed

Expected Results:
    - Login succeeds without error
    - Products screen loads with the "Products" title visible
    - User has access to the product catalog

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from framework.pages.login_page import LoginPage
from framework.pages.products_page import ProductsPage
from framework.pages.locators import ProductsLocators
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, priority


@pytest.mark.smoke
@component("Login")
@priority("critical")
def check_T001_login_valid_credentials(driver):
    """Verify standard_user can log in and reach the Products screen."""
    # Step 1-2: Enter credentials
    login_page = LoginPage(driver)

    # Step 3: Tap Login
    products_page = login_page.login(TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Step 4: Verify Products screen is displayed
    assert isinstance(products_page, ProductsPage), (
        "Login did not return a ProductsPage instance"
    )
    assert products_page.is_displayed(ProductsLocators.PRODUCTS_TITLE), (
        "Products title is not visible after login — login may have failed"
    )
