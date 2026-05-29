"""
check_T006_product_detail_view — Demo_QA
===========================================
Regression test: Open a product and verify detail information is displayed.

Preconditions:
    - User is logged in and on the Products screen
    - At least one product is available in the catalog

Steps:
    1. Log in with standard_user credentials
    2. Open the first product ("Sauce Labs Backpack")
    3. Verify product title is displayed
    4. Verify product price is displayed
    5. Verify product description is displayed

Expected Results:
    - Product detail page loads with title, price, and description visible

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from tests.flows.login_flow import login_flow
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, test_type as mark_test_type, priority


@pytest.mark.regression
@component("Catalog")
@mark_test_type("functional")
@priority("high")
def check_T006_product_detail_view(driver):
    """Verify that opening a product displays its title, price, and description."""
    # Login and navigate to products page
    products_page = login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Open a specific product
    product_detail_page = products_page.open_product("Sauce Labs Backpack")

    # Verify product details are displayed
    title = product_detail_page.get_product_title()
    price = product_detail_page.get_product_price()
    description = product_detail_page.get_product_description()

    assert title != "", "Product title should not be empty on detail page"
    assert price != "", "Product price should not be empty on detail page"
    assert description != "", "Product description should not be empty on detail page"
