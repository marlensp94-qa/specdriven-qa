"""
Locator Store — Demo_QA
==========================
Centralized element locators for all Swag Labs Mobile screens.
Organized by screen/page with accessibility IDs as the primary strategy (≥80%).
Fallback to resource-id or XPath only when accessibility IDs are unavailable.

Target App: Sauce Labs "My Demo App" for Android
Repository: https://github.com/saucelabs/my-demo-app-android

Usage:
    from framework.pages.locators import LoginLocators, ProductsLocators

    class LoginPage(BasePage):
        key_element = LoginLocators.LOGIN_BUTTON

        def login(self, username, password):
            self.type_text(LoginLocators.USERNAME_FIELD, username)
            ...

Locator Format:
    Each locator is a tuple: (strategy, value)
    - strategy: AppiumBy constant (ACCESSIBILITY_ID, XPATH, ID)
    - value: The locator string

Notes:
    - Locators are based on Sauce Labs "My Demo App" v2.2.0 for Android
    - Accessibility IDs are preferred for cross-platform compatibility
    - XPath is used only as last resort (fragile, slower)
    - If locators break after an APK update, use Appium Inspector to discover
      the new accessibility IDs and update this file only
"""

from appium.webdriver.common.appiumby import AppiumBy


# =============================================================================
# LOGIN SCREEN
# =============================================================================

class LoginLocators:
    """Locators for the Login screen (authentication)."""

    # Key element — used for page load validation
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Login button")

    # Input fields
    USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "Username input field")
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "Password input field")

    # Error messages
    ERROR_MESSAGE = (AppiumBy.XPATH,
                     '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/txtTitle"]')

    # Biometric prompt (if available)
    BIOMETRIC_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Biometrics button")


# =============================================================================
# PRODUCTS SCREEN (Catalog)
# =============================================================================

class ProductsLocators:
    """Locators for the Products/Catalog screen (main product listing)."""

    # Key element — page title
    PRODUCTS_TITLE = (AppiumBy.XPATH,
                      '//android.widget.TextView[@text="Products"]')

    # Sort button
    SORT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Sort button")

    # Sort options (in the sort modal)
    SORT_NAME_ASC = (AppiumBy.ACCESSIBILITY_ID, "nameAsc")
    SORT_NAME_DESC = (AppiumBy.ACCESSIBILITY_ID, "nameDes")
    SORT_PRICE_ASC = (AppiumBy.ACCESSIBILITY_ID, "priceAsc")
    SORT_PRICE_DESC = (AppiumBy.ACCESSIBILITY_ID, "priceDes")

    # Cart icon with badge
    CART_BADGE = (AppiumBy.ACCESSIBILITY_ID, "Cart-tab-item")

    # Product items — use dynamic locator with product name
    @staticmethod
    def product_by_name(name: str) -> tuple:
        """Get locator for a product item by its display name.

        Args:
            name: Product name as displayed in the catalog.

        Returns:
            Locator tuple for the product item.
        """
        return (AppiumBy.XPATH,
                f'//android.widget.TextView[@text="{name}"]')

    @staticmethod
    def product_price_by_name(name: str) -> tuple:
        """Get locator for a product's price label by product name."""
        return (AppiumBy.XPATH,
                f'//android.widget.TextView[@text="{name}"]/following-sibling::android.widget.TextView[contains(@text, "$")]')

    # Add to cart buttons on product cards
    @staticmethod
    def add_to_cart_button(product_index: int) -> tuple:
        """Get the Add to Cart button for a product by its position (0-indexed)."""
        return (AppiumBy.XPATH,
                f'(//android.widget.ImageView[@content-desc="Adds product to cart"])[{product_index + 1}]')


# =============================================================================
# PRODUCT DETAIL SCREEN
# =============================================================================

class ProductDetailLocators:
    """Locators for the Product Detail screen (single product view)."""

    # Key element — product title on detail page
    PRODUCT_TITLE = (AppiumBy.XPATH,
                     '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/productTV"]')

    # Product information
    PRODUCT_PRICE = (AppiumBy.XPATH,
                     '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/priceTV"]')
    PRODUCT_DESCRIPTION = (AppiumBy.XPATH,
                           '//android.widget.TextView[@resource-id="com.saucelabs.mydemoapp.android:id/txtDescription"]')

    # Actions
    ADD_TO_CART_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")
    REMOVE_FROM_CART_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Tap to remove product from cart")

    # Color/variant selection
    BLUE_CIRCLE = (AppiumBy.ACCESSIBILITY_ID, "Blue circle")
    RED_CIRCLE = (AppiumBy.ACCESSIBILITY_ID, "Red circle")
    BLACK_CIRCLE = (AppiumBy.ACCESSIBILITY_ID, "Black circle")

    # Quantity
    COUNTER_PLUS = (AppiumBy.ACCESSIBILITY_ID, "Counter Plus Button")
    COUNTER_MINUS = (AppiumBy.ACCESSIBILITY_ID, "Counter Minus Button")
    COUNTER_AMOUNT = (AppiumBy.ACCESSIBILITY_ID, "Counter Amount")

    # Navigation
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Navigate back")


# =============================================================================
# CART SCREEN
# =============================================================================

class CartLocators:
    """Locators for the Cart/Shopping Cart screen."""

    # Key element — cart title
    CART_TITLE = (AppiumBy.XPATH,
                  '//android.widget.TextView[@text="My Cart"]')

    # Cart items
    @staticmethod
    def cart_item_by_name(name: str) -> tuple:
        """Get locator for a cart item by product name."""
        return (AppiumBy.XPATH,
                f'//android.widget.TextView[@text="{name}"]')

    @staticmethod
    def remove_item_button(product_name: str) -> tuple:
        """Get the Remove button for a specific cart item."""
        return (AppiumBy.XPATH,
                f'//android.widget.TextView[@text="{product_name}"]/ancestor::android.view.ViewGroup//android.widget.ImageView[@content-desc="Removes product from cart"]')

    # Cart totals
    TOTAL_ITEMS = (AppiumBy.XPATH,
                   '//android.widget.TextView[contains(@text, "Total:")]')
    TOTAL_PRICE = (AppiumBy.XPATH,
                   '//android.widget.TextView[contains(@text, "$")]')

    # Actions
    PROCEED_TO_CHECKOUT = (AppiumBy.ACCESSIBILITY_ID, "Proceed To Checkout button")
    CONTINUE_SHOPPING = (AppiumBy.ACCESSIBILITY_ID, "Continue Shopping button")

    # Empty cart state
    NO_ITEMS_TEXT = (AppiumBy.XPATH,
                    '//android.widget.TextView[@text="No Items"]')


# =============================================================================
# CHECKOUT INFO SCREEN (Step 1: Shipping Information)
# =============================================================================

class CheckoutInfoLocators:
    """Locators for the Checkout Information screen (name, address)."""

    # Key element — checkout title
    CHECKOUT_TITLE = (AppiumBy.XPATH,
                      '//android.widget.TextView[@text="Checkout"]')

    # Input fields
    FULL_NAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "Full Name* input field")
    ADDRESS_LINE_1 = (AppiumBy.ACCESSIBILITY_ID, "Address Line 1* input field")
    ADDRESS_LINE_2 = (AppiumBy.ACCESSIBILITY_ID, "Address Line 2 input field")
    CITY_FIELD = (AppiumBy.ACCESSIBILITY_ID, "City* input field")
    STATE_FIELD = (AppiumBy.ACCESSIBILITY_ID, "State/Region input field")
    ZIP_CODE_FIELD = (AppiumBy.ACCESSIBILITY_ID, "Zip Code* input field")
    COUNTRY_FIELD = (AppiumBy.ACCESSIBILITY_ID, "Country* input field")

    # Payment fields
    CARD_NUMBER = (AppiumBy.ACCESSIBILITY_ID, "Card Number* input field")
    EXPIRATION_DATE = (AppiumBy.ACCESSIBILITY_ID, "Expiration Date* input field")
    SECURITY_CODE = (AppiumBy.ACCESSIBILITY_ID, "Security Code* input field")

    # Actions
    TO_PAYMENT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "To Payment button")

    # Error messages
    ERROR_MESSAGE = (AppiumBy.XPATH,
                     '//android.widget.TextView[contains(@text, "required")]')


# =============================================================================
# CHECKOUT OVERVIEW SCREEN (Step 2: Review Order)
# =============================================================================

class CheckoutOverviewLocators:
    """Locators for the Checkout Overview/Review screen."""

    # Key element — review order title
    OVERVIEW_TITLE = (AppiumBy.XPATH,
                      '//android.widget.TextView[@text="Checkout"]')

    # Order summary
    ITEM_TOTAL = (AppiumBy.XPATH,
                  '//android.widget.TextView[contains(@text, "Item total")]')
    TAX = (AppiumBy.XPATH,
           '//android.widget.TextView[contains(@text, "Tax")]')
    TOTAL = (AppiumBy.XPATH,
             '//android.widget.TextView[contains(@text, "Total:")]')

    # Delivery address
    DELIVERY_ADDRESS = (AppiumBy.XPATH,
                        '//android.widget.TextView[contains(@text, "Delivery Address")]')

    # Payment info
    PAYMENT_INFO = (AppiumBy.XPATH,
                    '//android.widget.TextView[contains(@text, "Payment Method")]')

    # Actions
    PLACE_ORDER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Place Order button")


# =============================================================================
# CHECKOUT COMPLETE SCREEN (Order Confirmation)
# =============================================================================

class CheckoutCompleteLocators:
    """Locators for the Checkout Complete/Confirmation screen."""

    # Key element — success message
    COMPLETE_TITLE = (AppiumBy.XPATH,
                      '//android.widget.TextView[@text="Checkout Complete"]')

    # Confirmation content
    SUCCESS_IMAGE = (AppiumBy.ACCESSIBILITY_ID, "Checkout complete screen")
    CONTINUE_SHOPPING_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue Shopping button")


# =============================================================================
# COMMON / NAVIGATION
# =============================================================================

class CommonLocators:
    """Locators shared across multiple screens (navigation, menus)."""

    # Bottom navigation
    CATALOG_TAB = (AppiumBy.ACCESSIBILITY_ID, "Catalog-tab-item")
    CART_TAB = (AppiumBy.ACCESSIBILITY_ID, "Cart-tab-item")
    MORE_TAB = (AppiumBy.ACCESSIBILITY_ID, "More-tab-item")

    # Hamburger menu
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Open Menu")
    MENU_CLOSE = (AppiumBy.ACCESSIBILITY_ID, "Close Menu")

    # Menu items
    MENU_CATALOG = (AppiumBy.ACCESSIBILITY_ID, "menu item catalog")
    MENU_CART = (AppiumBy.ACCESSIBILITY_ID, "menu item cart")
    MENU_LOGIN = (AppiumBy.ACCESSIBILITY_ID, "menu item log in")
    MENU_LOGOUT = (AppiumBy.ACCESSIBILITY_ID, "menu item log out")
    MENU_ABOUT = (AppiumBy.ACCESSIBILITY_ID, "menu item about")

    # Back navigation
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Navigate back")

    # Loading indicator
    LOADING_SPINNER = (AppiumBy.XPATH,
                       '//android.widget.ProgressBar')
