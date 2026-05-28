"""
LoginPage — Demo_QA
=====================
Page Object for the Swag Labs Login screen.
Handles user authentication (login with credentials, clear fields).

Usage:
    from framework.pages.login_page import LoginPage

    login_page = LoginPage(driver)
    products_page = login_page.login("bob@example.com", "10203040")
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import LoginLocators


class LoginPage(BasePage):
    """Page Object for the Swag Labs Login screen.

    Provides methods for user authentication and credential management.
    Validates page load by checking the Login button is visible.
    """

    key_element = LoginLocators.LOGIN_BUTTON

    def login(self, username: str, password: str):
        """Enter credentials and tap Login.

        Args:
            username: User email/username.
            password: User password.

        Returns:
            ProductsPage instance after successful login.

        Raises:
            PageNotLoadedError: If ProductsPage doesn't load after login.
        """
        self.type_text(LoginLocators.USERNAME_FIELD, username)
        self.type_text(LoginLocators.PASSWORD_FIELD, password)
        self.tap(LoginLocators.LOGIN_BUTTON)

        # Import here to avoid circular imports
        from framework.pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def login_expecting_error(self, username: str, password: str) -> str:
        """Enter credentials expecting login to fail. Returns error message.

        Args:
            username: User email/username.
            password: User password.

        Returns:
            Error message text displayed on screen.
        """
        self.type_text(LoginLocators.USERNAME_FIELD, username)
        self.type_text(LoginLocators.PASSWORD_FIELD, password)
        self.tap(LoginLocators.LOGIN_BUTTON)

        return self.get_text(LoginLocators.ERROR_MESSAGE)

    def clear_credentials(self):
        """Clear both username and password fields.

        Useful for testing multiple login attempts in sequence.
        """
        username_el = self.wait_for_element(LoginLocators.USERNAME_FIELD)
        username_el.clear()

        password_el = self.wait_for_element(LoginLocators.PASSWORD_FIELD)
        password_el.clear()

        self.log.info("Credentials cleared")

    def is_error_displayed(self) -> bool:
        """Check if a login error message is currently visible.

        Returns:
            True if error message is displayed, False otherwise.
        """
        return self.is_displayed(LoginLocators.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        """Get the current error message text.

        Returns:
            Error message string, or empty string if not displayed.
        """
        if self.is_error_displayed():
            return self.get_text(LoginLocators.ERROR_MESSAGE)
        return ""
