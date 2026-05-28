"""
ProductDetailPage — Demo_QA
==============================
Page Object for the Swag Labs Product Detail screen.
Handles viewing product info, adding/removing from cart, and navigation back.

Usage:
    from framework.pages.product_detail_page import ProductDetailPage

    detail_page = ProductDetailPage(driver)
    detail_page.add_to_cart()
    products_page = detail_page.go_back()
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import ProductDetailLocators


class ProductDetailPage(BasePage):
    """Page Object for the Swag Labs Product Detail screen.

    Provides methods for viewing product information, managing cart state,
    and navigating back to the catalog.
    """

    key_element = ProductDetailLocators.PRODUCT_TITLE

    def add_to_cart(self):
        """Add the current product to the shopping cart.

        Taps the "Add to Cart" button on the product detail screen.
        """
        self.tap(ProductDetailLocators.ADD_TO_CART_BUTTON)
        self.log.info("Product added to cart from detail page")

    def remove_from_cart(self):
        """Remove the current product from the shopping cart.

        Taps the "Remove" button (visible when product is already in cart).
        """
        self.tap(ProductDetailLocators.REMOVE_FROM_CART_BUTTON)
        self.log.info("Product removed from cart from detail page")

    def go_back(self):
        """Navigate back to the Products catalog.

        Returns:
            ProductsPage instance.

        Raises:
            PageNotLoadedError: If products page doesn't load.
        """
        self.tap(ProductDetailLocators.BACK_BUTTON)

        from framework.pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def get_product_title(self) -> str:
        """Get the product title text.

        Returns:
            Product title string.
        """
        return self.get_text(ProductDetailLocators.PRODUCT_TITLE)

    def get_product_price(self) -> str:
        """Get the product price text.

        Returns:
            Price string (e.g., "$29.99").
        """
        return self.get_text(ProductDetailLocators.PRODUCT_PRICE)

    def get_product_description(self) -> str:
        """Get the product description text.

        Returns:
            Description string.
        """
        return self.get_text(ProductDetailLocators.PRODUCT_DESCRIPTION)

    def set_quantity(self, quantity: int):
        """Set the product quantity using +/- buttons.

        Args:
            quantity: Desired quantity (minimum 1).
        """
        # Get current quantity
        current = int(self.get_text(ProductDetailLocators.COUNTER_AMOUNT))

        while current < quantity:
            self.tap(ProductDetailLocators.COUNTER_PLUS)
            current += 1

        while current > quantity and current > 1:
            self.tap(ProductDetailLocators.COUNTER_MINUS)
            current -= 1

        self.log.info("Quantity set to %d", quantity)

    def is_add_to_cart_visible(self) -> bool:
        """Check if Add to Cart button is visible (product not in cart).

        Returns:
            True if Add to Cart is visible, False if Remove is shown instead.
        """
        return self.is_displayed(ProductDetailLocators.ADD_TO_CART_BUTTON)
