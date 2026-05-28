"""
CheckoutOverviewPage — Demo_QA
=================================
Page Object for the Swag Labs Checkout Overview/Review screen (Step 2).
Handles reviewing the order and completing the purchase.

Usage:
    from framework.pages.checkout_overview_page import CheckoutOverviewPage

    overview_page = CheckoutOverviewPage(driver)
    complete_page = overview_page.finish_checkout()
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import CheckoutOverviewLocators


class CheckoutOverviewPage(BasePage):
    """Page Object for the Checkout Overview/Review screen.

    Provides methods for reviewing order details and completing
    or canceling the purchase.
    """

    key_element = CheckoutOverviewLocators.PLACE_ORDER_BUTTON

    def finish_checkout(self):
        """Complete the purchase by tapping 'Place Order'.

        Returns:
            CheckoutCompletePage instance.

        Raises:
            PageNotLoadedError: If confirmation page doesn't load.
        """
        self.tap(CheckoutOverviewLocators.PLACE_ORDER_BUTTON)

        from framework.pages.checkout_complete_page import CheckoutCompletePage
        return CheckoutCompletePage(self.driver)

    def cancel(self):
        """Cancel the order and return to the products catalog.

        Returns:
            ProductsPage instance.

        Raises:
            PageNotLoadedError: If products page doesn't load.
        """
        from framework.pages.locators import CommonLocators
        self.tap(CommonLocators.BACK_BUTTON)

        from framework.pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def get_total(self) -> str:
        """Get the order total amount.

        Returns:
            Total price string (e.g., "$29.99").
        """
        return self.get_text(CheckoutOverviewLocators.TOTAL)

    def get_item_total(self) -> str:
        """Get the item subtotal (before tax).

        Returns:
            Item total string.
        """
        return self.get_text(CheckoutOverviewLocators.ITEM_TOTAL)

    def get_delivery_address(self) -> str:
        """Get the delivery address shown in the review.

        Returns:
            Delivery address text.
        """
        return self.get_text(CheckoutOverviewLocators.DELIVERY_ADDRESS)
