"""
check_T004_catalog_browsing — Demo_QA
========================================
Regression test: Verify product catalog loads and displays products.

Preconditions:
    - User is logged in and on the Products screen

Steps:
    1. Log in with standard_user credentials
    2. Verify the Products page is displayed
    3. Retrieve the list of product names
    4. Verify at least one product is visible

Expected Results:
    - Products page loads successfully
    - Product list contains at least one item

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
def check_T004_catalog_browsing(driver):
    """Verify that the product catalog loads and displays products after login."""
    # Login and navigate to products page
    products_page = login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Verify product list is populated
    product_names = products_page.get_product_names()

    assert len(product_names) > 0, (
        "Expected at least one product in the catalog, but found none"
    )
