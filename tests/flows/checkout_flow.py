"""
Checkout Flow — Demo_QA
=========================
Reusable flow for completing the checkout process.

Usage:
    from tests.flows.checkout_flow import complete_checkout_flow

    complete_page = complete_checkout_flow(driver, "John", "Doe", "12345")
"""

from framework.pages.base_page import PageNotLoadedError
from framework.pages.cart_page import CartPage
from framework.pages.checkout_info_page import CheckoutInfoPage
from framework.pages.checkout_overview_page import CheckoutOverviewPage
from framework.pages.checkout_complete_page import CheckoutCompletePage


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


def complete_checkout_flow(
    driver, first_name: str, last_name: str, zip_code: str
) -> CheckoutCompletePage:
    """Complete checkout with provided shipping information.

    Assumes the driver is already on the CartPage with items in the cart.
    Proceeds through checkout info, overview, and finishes the order.

    Args:
        driver: Appium WebDriver instance.
        first_name: First name for shipping information.
        last_name: Last name for shipping information.
        zip_code: ZIP/postal code for shipping information.

    Returns:
        CheckoutCompletePage instance after successful order placement.

    Raises:
        ValueError: If any parameter is None, empty, or whitespace-only.
        PageNotLoadedError: If expected page transition fails.
    """
    _validate_string_param(first_name, "first_name")
    _validate_string_param(last_name, "last_name")
    _validate_string_param(zip_code, "zip_code")

    cart_page = CartPage(driver)
    checkout_info_page = cart_page.proceed_to_checkout()

    # Fill checkout info — the page expects full_name, address, city, zip, country
    # For the flow, we use first_name + last_name as full name, with defaults for other fields
    full_name = f"{first_name} {last_name}"
    checkout_overview_page = checkout_info_page.fill_checkout_info(
        full_name=full_name,
        address="123 Test Street",
        city="Test City",
        zip_code=zip_code,
        country="United States",
    )

    complete_page = checkout_overview_page.finish_checkout()

    return complete_page
