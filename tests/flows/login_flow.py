"""
Login Flow — Demo_QA
======================
Reusable flow for authenticating a user and returning the ProductsPage.

Usage:
    from tests.flows.login_flow import login_flow

    products_page = login_flow(driver, "standard_user", "secret_sauce")
"""

from framework.pages.base_page import PageNotLoadedError
from framework.pages.login_page import LoginPage
from framework.pages.products_page import ProductsPage


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


def login_flow(driver, username: str, password: str) -> ProductsPage:
    """Execute login and return ProductsPage.

    Navigates through the login screen using the provided credentials
    and returns the resulting ProductsPage instance.

    Args:
        driver: Appium WebDriver instance.
        username: User email/username for login.
        password: User password for login.

    Returns:
        ProductsPage instance after successful login.

    Raises:
        ValueError: If username or password is None, empty, or whitespace-only.
        PageNotLoadedError: If ProductsPage doesn't load after login.
    """
    _validate_string_param(username, "username")
    _validate_string_param(password, "password")

    login_page = LoginPage(driver)
    products_page = login_page.login(username, password)

    return products_page
