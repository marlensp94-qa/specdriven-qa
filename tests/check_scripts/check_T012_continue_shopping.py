"""
check_T012_continue_shopping — Demo_QA
=========================================
Regression test: From cart, tap Continue Shopping to return to products.

Preconditions:
    - User is logged in and on the Products screen
    - At least one product is available in the catalog

Steps:
    1. Log in with standard_user credentials
    2. Add a product to cart
    3. Navigate to cart
    4. Tap "Continue Shopping"
    5. Verify user is returned to the Products page

Expected Results:
    - After tapping Continue Shopping, user is back on the Products page

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from tests.flows.login_flow import login_flow
from tests.flows.cart_flow import add_product_to_cart_flow
from framework.pages.locators import ProductsLocators
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, test_type as mark_test_type, priority


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.regression
@component("Cart")
@mark_test_type("functional")
@priority("medium")
def check_T012_continue_shopping(driver):
    """Verify that Continue Shopping from cart returns to the Products page."""
    # Login
    login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Add product to cart and go to cart
    cart_page = add_product_to_cart_flow(driver, PRODUCT_NAME)

    # Tap Continue Shopping
    products_page = cart_page.continue_shopping()

    # Verify we are back on the Products page
    assert products_page.is_displayed(ProductsLocators.PRODUCTS_TITLE), (
        "Expected to be on the Products page after tapping Continue Shopping"
    )
