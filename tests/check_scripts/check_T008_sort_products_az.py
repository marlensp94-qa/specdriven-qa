"""
check_T008_sort_products_az — Demo_QA
========================================
Regression test: Sort products A-Z and verify alphabetical order.

Preconditions:
    - User is logged in and on the Products screen
    - Multiple products are available in the catalog

Steps:
    1. Log in with standard_user credentials
    2. Sort products by Name (A to Z)
    3. Retrieve the list of product names
    4. Verify the list is in ascending alphabetical order

Expected Results:
    - Products are displayed in A-Z alphabetical order after sorting

Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7
"""

import pytest

from tests.flows.login_flow import login_flow
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD_STANDARD
from framework.utils.markers import component, test_type as mark_test_type, priority


@pytest.mark.regression
@component("Catalog")
@mark_test_type("functional")
@priority("medium")
def check_T008_sort_products_az(driver):
    """Verify that sorting products A-Z results in alphabetical order."""
    # Login and navigate to products page
    products_page = login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)

    # Sort by name ascending (A to Z)
    products_page.sort_products("name_asc")

    # Get product names after sorting
    product_names = products_page.get_product_names()

    assert len(product_names) > 1, (
        "Need at least 2 products to verify sort order"
    )

    # Verify alphabetical order (case-insensitive)
    sorted_names = sorted(product_names, key=str.lower)
    assert product_names == sorted_names, (
        f"Products not in A-Z order. Got: {product_names}, "
        f"Expected: {sorted_names}"
    )
