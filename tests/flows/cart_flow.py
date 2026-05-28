"""
Cart Flow — Demo_QA
=====================
Reusable flow for adding a product to the cart and navigating to the CartPage.

Usage:
    from tests.flows.cart_flow import add_product_to_cart_flow

    cart_page = add_product_to_cart_flow(driver, "Sauce Labs Backpack")
"""

from framework.pages.base_page import PageNotLoadedError
from framework.pages.products_page import ProductsPage
from framework.pages.cart_page import CartPage


def _validate_string_param(value, param_name: str) -> None:
    """Validate that a string parameter is not None, empty, or whitespace-only.

    Args:
        value: The value to validate.
        param_name: Name of the parameter (for error messages).

    Raises:
        ValueError: If value is None, empty, or whitespace-only.
    """
    if value is None:
        raise ValueError(f"Parameter '{param_name}' must not be None")
    if not isinstance(value, str):
        raise ValueError(f"Parameter '{param_name}' must be a string")
    if value.strip() == "":
        raise ValueError(
            f"Parameter '{param_name}' must not be empty or whitespace-only"
        )


def add_product_to_cart_flow(driver, product_name: str) -> CartPage:
    """Add a product by name and navigate to the cart.

    Assumes the driver is already on the ProductsPage. Opens the product
    detail, adds it to cart, goes back to products, then opens the cart.

    Args:
        driver: Appium WebDriver instance.
        product_name: Exact name of the product to add (as displayed in catalog).

    Returns:
        CartPage instance with the product added.

    Raises:
        ValueError: If product_name is None, empty, or whitespace-only.
        PageNotLoadedError: If expected page transition fails.
    """
    _validate_string_param(product_name, "product_name")

    products_page = ProductsPage(driver)
    product_detail_page = products_page.open_product(product_name)
    product_detail_page.add_to_cart()

    # go_back() returns ProductsPage, then navigate to cart
    products_page_after = product_detail_page.go_back()
    cart_page = products_page_after.open_cart()

    return cart_page
