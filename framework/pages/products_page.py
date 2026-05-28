"""
ProductsPage — Demo_QA
========================
Page Object for the Swag Labs Products/Catalog screen.
Handles product browsing, sorting, and navigation to product details or cart.

Usage:
    from framework.pages.products_page import ProductsPage

    products_page = ProductsPage(driver)
    detail_page = products_page.open_product("Sauce Labs Backpack")
    products_page.sort_products("name_asc")
    cart_page = products_page.open_cart()
"""

from framework.pages.base_page import BasePage
from framework.pages.locators import ProductsLocators, CommonLocators


class ProductsPage(BasePage):
    """Page Object for the Swag Labs Products/Catalog screen.

    Provides methods for browsing products, sorting the catalog,
    and navigating to product details or the shopping cart.
    """

    key_element = ProductsLocators.PRODUCTS_TITLE

    def open_product(self, product_name: str):
        """Tap on a product to open its detail page.

        Args:
            product_name: Exact product name as displayed in the catalog.

        Returns:
            ProductDetailPage instance.

        Raises:
            TimeoutException: If product not found in catalog.
            PageNotLoadedError: If detail page doesn't load.
        """
        product_locator = ProductsLocators.product_by_name(product_name)
        self.tap(product_locator)

        from framework.pages.product_detail_page import ProductDetailPage
        return ProductDetailPage(self.driver)

    def sort_products(self, sort_option: str):
        """Sort the product catalog by the specified option.

        Args:
            sort_option: Sort option identifier. One of:
                - "name_asc": Name (A to Z)
                - "name_desc": Name (Z to A)
                - "price_asc": Price (low to high)
                - "price_desc": Price (high to low)
        """
        self.tap(ProductsLocators.SORT_BUTTON)

        sort_map = {
            "name_asc": ProductsLocators.SORT_NAME_ASC,
            "name_desc": ProductsLocators.SORT_NAME_DESC,
            "price_asc": ProductsLocators.SORT_PRICE_ASC,
            "price_desc": ProductsLocators.SORT_PRICE_DESC,
        }

        locator = sort_map.get(sort_option)
        if locator is None:
            raise ValueError(
                f"Invalid sort option '{sort_option}'. "
                f"Must be one of: {list(sort_map.keys())}"
            )

        self.tap(locator)
        self.log.info("Sorted products by: %s", sort_option)

    def open_cart(self):
        """Navigate to the shopping cart.

        Returns:
            CartPage instance.

        Raises:
            PageNotLoadedError: If cart page doesn't load.
        """
        self.tap(CommonLocators.CART_TAB)

        from framework.pages.cart_page import CartPage
        return CartPage(self.driver)

    def add_product_to_cart(self, product_index: int = 0):
        """Add a product to cart directly from the catalog (by position).

        Args:
            product_index: Zero-based index of the product in the list.
        """
        add_button = ProductsLocators.add_to_cart_button(product_index)
        self.tap(add_button)
        self.log.info("Added product at index %d to cart", product_index)

    def is_product_displayed(self, product_name: str) -> bool:
        """Check if a product is visible in the catalog.

        Args:
            product_name: Product name to check.

        Returns:
            True if product is visible, False otherwise.
        """
        product_locator = ProductsLocators.product_by_name(product_name)
        return self.is_displayed(product_locator)

    def get_product_names(self) -> list:
        """Get all visible product names in the catalog.

        Returns:
            List of product name strings currently visible on screen.
        """
        from appium.webdriver.common.appiumby import AppiumBy
        elements = self.driver.find_elements(
            AppiumBy.XPATH,
            '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/titleTV"]'
        )
        return [el.text for el in elements if el.text]
