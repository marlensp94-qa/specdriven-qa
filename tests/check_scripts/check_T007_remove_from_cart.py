"""
check_T007_remove_from_cart — Demo_QA
========================================
Regression test: Add a product to cart, then remove it.

Preconditions:
    - User is logged in and on the Products screen
    - At least one product is available in the catalog

Steps:
    1. Log in with standard_user credentials
    2. Add "Sauce Labs Backpack" to cart via product detail
    3. Navigate to the cart
    4. Verify the product is in the cart
    5. Remove the product from the cart
    6. Verify the cart is empty or product is no longer listed

Expected Results:
    - Product is successfully added to cart
    - After removal, the product is no longer in the cart

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from tests.flows.login_flow import login_flow
from tests.flows.cart_flow import add_product_to_cart_flow
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, test_type as mark_test_type, priority


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.regression
@component("Cart")
@mark_test_type("functional")
@priority("high")
def check_T007_remove_from_cart(driver):
    """Verify that a product can be added to cart and then removed."""
    # Login
    login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Add product to cart and navigate to cart page
    cart_page = add_product_to_cart_flow(driver, PRODUCT_NAME)

    # Verify product is in cart
    assert cart_page.is_item_in_cart(PRODUCT_NAME), (
        f"Expected '{PRODUCT_NAME}' to be in cart after adding"
    )

    # Remove the product
    cart_page.remove_item(PRODUCT_NAME)

    # Verify product is no longer in cart
    assert not cart_page.is_item_in_cart(PRODUCT_NAME), (
        f"Expected '{PRODUCT_NAME}' to be removed from cart"
    )
