"""
check_T011_checkout_cancel — Demo_QA
=======================================
Regression test: Start checkout then cancel to return to cart.

Preconditions:
    - User is logged in and on the Products screen
    - At least one product is available in the catalog

Steps:
    1. Log in with standard_user credentials
    2. Add a product to cart
    3. Navigate to cart
    4. Proceed to checkout
    5. Cancel checkout
    6. Verify user is returned to the Cart page

Expected Results:
    - After canceling checkout, user is back on the Cart page

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from tests.flows.login_flow import login_flow
from tests.flows.cart_flow import add_product_to_cart_flow
from framework.pages.locators import CartLocators
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, test_type as mark_test_type, priority


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.regression
@component("Checkout")
@mark_test_type("functional")
@priority("medium")
def check_T011_checkout_cancel(driver):
    """Verify that canceling checkout returns the user to the Cart page."""
    # Login
    login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Add product to cart
    cart_page = add_product_to_cart_flow(driver, PRODUCT_NAME)

    # Proceed to checkout
    checkout_info_page = cart_page.proceed_to_checkout()

    # Cancel checkout — should return to cart
    cart_page_after = checkout_info_page.cancel()

    # Verify we are back on the Cart page
    assert cart_page_after.is_displayed(CartLocators.CART_TITLE), (
        "Expected to be on the Cart page after canceling checkout"
    )
