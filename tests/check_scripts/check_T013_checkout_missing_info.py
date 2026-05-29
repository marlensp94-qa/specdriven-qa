"""
check_T013_checkout_missing_info — Demo_QA
=============================================
Regression test: Submit checkout form with empty fields and verify error.

Preconditions:
    - User is logged in and on the Products screen
    - At least one product is in the cart

Steps:
    1. Log in with standard_user credentials
    2. Add a product to cart
    3. Navigate to cart
    4. Proceed to checkout
    5. Submit the form without filling any fields
    6. Verify a validation error message is displayed

Expected Results:
    - Checkout form rejects submission with empty fields
    - A validation error message is displayed

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from tests.flows.login_flow import login_flow
from tests.flows.cart_flow import add_product_to_cart_flow
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, test_type as mark_test_type, priority


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.regression
@component("Checkout")
@mark_test_type("negative")
@priority("high")
def check_T013_checkout_missing_info(driver):
    """Verify that submitting checkout with empty fields shows a validation error."""
    # Login
    login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Add product to cart
    cart_page = add_product_to_cart_flow(driver, PRODUCT_NAME)

    # Proceed to checkout
    checkout_info_page = cart_page.proceed_to_checkout()

    # Submit form without filling any fields
    checkout_info_page.fill_and_submit_empty()

    # Verify error message is displayed
    assert checkout_info_page.is_error_displayed(), (
        "Expected a validation error when submitting checkout with empty fields"
    )
