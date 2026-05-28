"""
CartPage — Demo_QA
====================
Page Object for the Swag Labs Shopping Cart screen.
Handles viewing cart items, removing products, and proceeding to checkout.

Usage:
    from framework.pages.cart_page import CartPage

    cart_page = CartPage(driver)
    cart_page.remove_item("Sauce Labs Backpack")
    checkout_page = cart_page.proceed_to_checkout()
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import CartLocators


class CartPage(BasePage):
    """Page Object for the Swag Labs Shopping Cart screen.

    Provides methods for managing cart contents and navigating
    to checkout or back to shopping.
    """

    key_element = CartLocators.CART_TITLE

    def remove_item(self, product_name: str):
        """Remove a specific product from the cart.

        Args:
            product_name: Exact name of the product to remove.
        """
        remove_locator = CartLocators.remove_item_button(product_name)
        self.tap(remove_locator)
        self.log.info("Removed '%s' from cart", product_name)

    def proceed_to_checkout(self):
        """Tap 'Proceed to Checkout' to start the checkout flow.

        Returns:
            CheckoutInfoPage instance.

        Raises:
            PageNotLoadedError: If checkout page doesn't load.
        """
        self.tap(CartLocators.PROCEED_TO_CHECKOUT)

        from framework.pages.checkout_info_page import CheckoutInfoPage
        return CheckoutInfoPage(self.driver)

    def continue_shopping(self):
        """Tap 'Continue Shopping' to return to the product catalog.

        Returns:
            ProductsPage instance.

        Raises:
            PageNotLoadedError: If products page doesn't load.
        """
        self.tap(CartLocators.CONTINUE_SHOPPING)

        from framework.pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def is_item_in_cart(self, product_name: str) -> bool:
        """Check if a specific product is in the cart.

        Args:
            product_name: Product name to check.

        Returns:
            True if product is visible in cart, False otherwise.
        """
        item_locator = CartLocators.cart_item_by_name(product_name)
        return self.is_displayed(item_locator)

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty (shows 'No Items' message).

        Returns:
            True if cart is empty, False if items are present.
        """
        return self.is_displayed(CartLocators.NO_ITEMS_TEXT)

    def get_total_price(self) -> str:
        """Get the total price displayed in the cart.

        Returns:
            Total price string (e.g., "$29.99").
        """
        return self.get_text(CartLocators.TOTAL_PRICE)
