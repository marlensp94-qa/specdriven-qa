"""
Reusable Test Flows — Demo_QA
================================
Composable multi-step operations using page objects.

These flows encapsulate common multi-step user journeys and can be
chained together in test scenarios to reduce code duplication.

Usage:
    from tests.flows import login_flow, add_product_to_cart_flow, complete_checkout_flow

    products_page = login_flow(driver, "standard_user", "secret_sauce")
    cart_page = add_product_to_cart_flow(driver, "Sauce Labs Backpack")
    complete_page = complete_checkout_flow(driver, "John", "Doe", "12345")
"""

from tests.flows.login_flow import login_flow
from tests.flows.cart_flow import add_product_to_cart_flow
from tests.flows.checkout_flow import complete_checkout_flow

__all__ = [
    "login_flow",
    "add_product_to_cart_flow",
    "complete_checkout_flow",
]
