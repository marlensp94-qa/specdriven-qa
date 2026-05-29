"""
check_T010_complete_checkout — Demo_QA
==========================================
Smoke test: Verify the full checkout flow from adding a product to order confirmation.

Preconditions:
    - Swag Labs app is installed and launched on the emulator
    - User is logged in and on the Products screen
    - Cart is empty (no items previously added)

Steps:
    1. From the Products screen, open "Sauce Labs Backpack" and add to cart
    2. Navigate back to Products, then open the cart
    3. From the cart, proceed to checkout
    4. Fill in shipping information (name, address, city, zip, country)
    5. Fill in payment information (card number, expiration, security code)
    6. Submit checkout info to reach the order overview
    7. Place the order from the overview screen
    8. Verify the Checkout Complete confirmation screen is displayed

Expected Results:
    - Product is successfully added to cart
    - Checkout info form accepts valid data
    - Order overview displays before final confirmation
    - "Checkout Complete" screen is displayed after placing the order
    - Order is confirmed successfully

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from framework.pages.products_page import ProductsPage
from framework.pages.checkout_complete_page import CheckoutCompletePage
from framework.utils.markers import component, priority


PRODUCT_NAME = "Sauce Labs Backpack"
CHECKOUT_FULL_NAME = "John Doe"
CHECKOUT_ADDRESS = "123 Test Street"
CHECKOUT_CITY = "San Francisco"
CHECKOUT_ZIP = "94105"
CHECKOUT_COUNTRY = "United States"


@pytest.mark.smoke
@component("Checkout")
@priority("critical")
def check_T010_complete_checkout(ensure_logged_in):
    """Verify the complete checkout flow from product selection to order confirmation."""
    driver = ensure_logged_in

    # Step 1: Open product and add to cart
    products_page = ProductsPage(driver)
    product_detail_page = products_page.open_product(PRODUCT_NAME)
    product_detail_page.add_to_cart()

    # Step 2: Navigate back and open cart
    products_page = product_detail_page.go_back()
    cart_page = products_page.open_cart()

    # Step 3: Proceed to checkout
    checkout_info_page = cart_page.proceed_to_checkout()

    # Steps 4-6: Fill checkout info and submit
    checkout_overview_page = checkout_info_page.fill_checkout_info(
        full_name=CHECKOUT_FULL_NAME,
        address=CHECKOUT_ADDRESS,
        city=CHECKOUT_CITY,
        zip_code=CHECKOUT_ZIP,
        country=CHECKOUT_COUNTRY,
    )

    # Step 7: Place the order
    checkout_complete_page = checkout_overview_page.finish_checkout()

    # Step 8: Verify order confirmation
    assert isinstance(checkout_complete_page, CheckoutCompletePage), (
        "Checkout did not return a CheckoutCompletePage instance"
    )
    assert checkout_complete_page.is_order_complete(), (
        "Checkout Complete title is not displayed — order may not have been placed"
    )
