"""
CheckoutCompletePage — Demo_QA
=================================
Page Object for the Swag Labs Checkout Complete/Confirmation screen.
Handles the order confirmation state and navigation back to shopping.

Usage:
    from framework.pages.checkout_complete_page import CheckoutCompletePage

    complete_page = CheckoutCompletePage(driver)
    products_page = complete_page.back_to_products()
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import CheckoutCompleteLocators


class CheckoutCompletePage(BasePage):
    """Page Object for the Checkout Complete/Confirmation screen.

    Provides methods for verifying order completion and navigating
    back to the product catalog.
    """

    key_element = CheckoutCompleteLocators.COMPLETE_TITLE

    def back_to_products(self):
        """Navigate back to the products catalog after order completion.

        Returns:
            ProductsPage instance.

        Raises:
            PageNotLoadedError: If products page doesn't load.
        """
        self.tap(CheckoutCompleteLocators.CONTINUE_SHOPPING_BUTTON)

        from framework.pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def is_order_complete(self) -> bool:
        """Verify the order completion title is displayed.

        Returns:
            True if "Checkout Complete" title is visible.
        """
        return self.is_displayed(CheckoutCompleteLocators.COMPLETE_TITLE)
