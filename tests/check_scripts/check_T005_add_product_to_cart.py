"""
check_T005_add_product_to_cart — Demo_QA
============================================
Smoke test: Verify that a user can add a product to the cart and see the cart badge update.

Preconditions:
    - Swag Labs app is installed and launched on the emulator
    - User is logged in and on the Products screen
    - Cart is empty (no items previously added)

Steps:
    1. From the Products screen, tap on "Sauce Labs Backpack" to open detail
    2. Tap "Add to Cart" on the product detail page
    3. Navigate back to the Products screen
    4. Open the cart
    5. Verify the product appears in the cart

Expected Results:
    - Product detail page loads successfully
    - "Add to Cart" action completes without error
    - Cart contains "Sauce Labs Backpack" after adding
    - Cart page displays the added item

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from framework.pages.products_page import ProductsPage
from framework.pages.product_detail_page import ProductDetailPage
from framework.pages.cart_page import CartPage
from framework.utils.markers import component, priority


PRODUCT_NAME = "Sauce Labs Backpack"


@pytest.mark.smoke
@component("Cart")
@priority("critical")
def check_T005_add_product_to_cart(ensure_logged_in):
    """Verify adding a product to cart and confirming it appears in the cart."""
    driver = ensure_logged_in

    # Step 1: Open product detail
    products_page = ProductsPage(driver)
    product_detail_page = products_page.open_product(PRODUCT_NAME)

    # Step 2: Add to cart
    product_detail_page.add_to_cart()

    # Step 3: Navigate back to Products
    products_page = product_detail_page.go_back()

    # Step 4: Open the cart
    cart_page = products_page.open_cart()

    # Step 5: Verify product is in the cart
    assert isinstance(cart_page, CartPage), (
        "Navigation to CartPage failed"
    )
    assert cart_page.is_item_in_cart(PRODUCT_NAME), (
        f"'{PRODUCT_NAME}' was not found in the cart after adding it"
    )
