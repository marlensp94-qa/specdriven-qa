"""
CheckoutInfoPage — Demo_QA
=============================
Page Object for the Swag Labs Checkout Information screen (Step 1).
Handles filling in shipping and payment information.

Usage:
    from framework.pages.checkout_info_page import CheckoutInfoPage

    checkout_page = CheckoutInfoPage(driver)
    overview_page = checkout_page.fill_checkout_info("John", "Doe", "12345")
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import CheckoutInfoLocators


class CheckoutInfoPage(BasePage):
    """Page Object for the Checkout Information screen.

    Provides methods for filling shipping/payment details and
    proceeding to the order review step.
    """

    key_element = CheckoutInfoLocators.CHECKOUT_TITLE

    def fill_checkout_info(
        self,
        full_name: str,
        address: str,
        city: str,
        zip_code: str,
        country: str,
        card_number: str = "3258 1265 7568 789",
        expiration: str = "03/25",
        security_code: str = "123",
    ):
        """Fill all checkout fields and proceed to payment/review.

        Args:
            full_name: Full name for shipping.
            address: Address line 1.
            city: City name.
            zip_code: Postal/ZIP code.
            country: Country name.
            card_number: Payment card number. Default test value provided.
            expiration: Card expiration date. Default test value provided.
            security_code: Card CVV/security code. Default test value provided.

        Returns:
            CheckoutOverviewPage instance.

        Raises:
            PageNotLoadedError: If overview page doesn't load.
        """
        self.type_text(CheckoutInfoLocators.FULL_NAME_FIELD, full_name)
        self.type_text(CheckoutInfoLocators.ADDRESS_LINE_1, address)
        self.type_text(CheckoutInfoLocators.CITY_FIELD, city)
        self.type_text(CheckoutInfoLocators.ZIP_CODE_FIELD, zip_code)
        self.type_text(CheckoutInfoLocators.COUNTRY_FIELD, country)

        # Scroll down to payment fields
        self.scroll(direction="down", distance=0.4)

        self.type_text(CheckoutInfoLocators.CARD_NUMBER, card_number)
        self.type_text(CheckoutInfoLocators.EXPIRATION_DATE, expiration)
        self.type_text(CheckoutInfoLocators.SECURITY_CODE, security_code)

        self.tap(CheckoutInfoLocators.TO_PAYMENT_BUTTON)

        from framework.pages.checkout_overview_page import CheckoutOverviewPage
        return CheckoutOverviewPage(self.driver)

    def fill_and_submit_empty(self):
        """Submit the form without filling any fields (for negative testing).

        Returns:
            Self (stays on same page due to validation error).
        """
        self.tap(CheckoutInfoLocators.TO_PAYMENT_BUTTON)
        return self

    def cancel(self):
        """Cancel checkout and return to cart.

        Returns:
            CartPage instance.

        Raises:
            PageNotLoadedError: If cart page doesn't load.
        """
        from framework.pages.locators import CommonLocators
        self.tap(CommonLocators.BACK_BUTTON)

        from framework.pages.cart_page import CartPage
        return CartPage(self.driver)

    def is_error_displayed(self) -> bool:
        """Check if a validation error message is displayed.

        Returns:
            True if error is visible, False otherwise.
        """
        return self.is_displayed(CheckoutInfoLocators.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        """Get the validation error message text.

        Returns:
            Error message string.
        """
        return self.get_text(CheckoutInfoLocators.ERROR_MESSAGE)
