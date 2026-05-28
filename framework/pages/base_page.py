"""
BasePage — Demo_QA
====================
Abstract base class for all Page Objects in the framework.
Provides common interaction methods (tap, type, wait, scroll) and
implements the Page Object Model pattern with lazy-loading locators.

Usage:
    from framework.pages.base_page import BasePage, PageNotLoadedError

    class LoginPage(BasePage):
        key_element = (AppiumBy.ACCESSIBILITY_ID, "Login Screen")

        def login(self, username, password):
            self.type_text(self.LOCATORS["username"], username)
            self.type_text(self.LOCATORS["password"], password)
            self.tap(self.LOCATORS["login_button"])
            return ProductsPage(self.driver)
"""

import time
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from framework.utils.constants import (
    DEFAULT_TIMEOUT,
    SHORT_TIMEOUT,
    PAGE_LOAD_TIMEOUT,
    UI_ANIMATION_DELAY,
    SCROLL_PAUSE,
    MAX_SCROLL_ATTEMPTS,
)
from framework.utils.logger_factory import get_logger


class PageNotLoadedError(Exception):
    """Raised when a page fails to load within the expected timeout.

    Attributes:
        page_name: Name of the page class that failed to load.
        key_element: The locator tuple that was not found.
    """

    def __init__(self, page_name: str, key_element: tuple):
        self.page_name = page_name
        self.key_element = key_element
        super().__init__(
            f"Page '{page_name}' failed to load: "
            f"key_element {key_element} not found within timeout"
        )


class _LazyElement:
    """Descriptor that locates an element only on first access (lazy-loading).

    Once located, the element reference is cached on the page instance.
    Subsequent accesses return the cached reference without re-querying.

    Usage in page objects:
        class MyPage(BasePage):
            username_field = _LazyElement((AppiumBy.ACCESSIBILITY_ID, "Username"))
    """

    def __init__(self, locator: tuple):
        self._locator = locator
        self._attr_name = None

    def __set_name__(self, owner, name):
        self._attr_name = f"_lazy_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Check cache first
        cached = getattr(obj, self._attr_name, None)
        if cached is not None:
            try:
                # Verify element is still valid (not stale)
                cached.is_displayed()
                return cached
            except (WebDriverException, AttributeError):
                # Element is stale, re-locate
                pass

        # Locate element and cache it
        element = obj.wait_for_element(self._locator)
        setattr(obj, self._attr_name, element)
        return element

    def __set__(self, obj, value):
        setattr(obj, self._attr_name, value)


class BasePage(ABC):
    """Abstract base class for all page objects.

    Provides common interaction methods and page validation.
    Subclasses must define `key_element` as a locator tuple used to
    verify the page has loaded successfully.

    Attributes:
        key_element: Tuple of (locator_strategy, locator_value) used to
                     validate the page is loaded. Must be defined by subclasses.
        driver: Appium WebDriver instance.
        timeout: Default wait timeout in seconds.

    Args:
        driver: Appium WebDriver instance.
        timeout: Default explicit wait timeout. Defaults to DEFAULT_TIMEOUT.

    Raises:
        PageNotLoadedError: If key_element is not found within timeout.
    """

    key_element: Tuple[str, str] = None  # Must be overridden by subclasses

    # Expose _LazyElement for use in subclasses
    LazyElement = _LazyElement

    def __init__(self, driver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.log = get_logger(self.__class__.__name__)

        # Validate page loaded
        self.validate_page()
        self.log.info("Page loaded: %s", self.__class__.__name__)

    def validate_page(self):
        """Validate that the page has loaded by checking key_element presence.

        Raises:
            PageNotLoadedError: If key_element not found within PAGE_LOAD_TIMEOUT.
        """
        if self.key_element is None:
            self.log.warning(
                "No key_element defined for %s. Skipping validation.",
                self.__class__.__name__,
            )
            return

        try:
            WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
                EC.visibility_of_element_located(self.key_element)
            )
        except (TimeoutException, NoSuchElementException):
            raise PageNotLoadedError(
                page_name=self.__class__.__name__,
                key_element=self.key_element,
            )

    def tap(self, locator: tuple, timeout: int = None):
        """Tap an element identified by locator.

        Args:
            locator: Tuple of (strategy, value) — e.g., (AppiumBy.ACCESSIBILITY_ID, "Login").
            timeout: Wait timeout. Defaults to self.timeout.
        """
        element = self.wait_for_element(locator, timeout)
        element.click()
        self.log.info("Tapped: %s", locator[1])

    def type_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None):
        """Clear and type text into an element.

        Args:
            locator: Tuple of (strategy, value).
            text: Text to type.
            clear_first: Whether to clear existing text before typing. Default True.
            timeout: Wait timeout. Defaults to self.timeout.
        """
        element = self.wait_for_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.log.info("Typed '%s' into: %s", text[:20] + "..." if len(text) > 20 else text, locator[1])

    def wait_for_element(self, locator: tuple, timeout: int = None):
        """Wait for an element to be visible and return it.

        Args:
            locator: Tuple of (strategy, value).
            timeout: Maximum wait time in seconds. Defaults to self.timeout.

        Returns:
            WebElement once visible.

        Raises:
            TimeoutException: If element not visible within timeout.
        """
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )

    def is_displayed(self, locator: tuple, timeout: int = None) -> bool:
        """Check if an element is displayed within timeout.

        Args:
            locator: Tuple of (strategy, value).
            timeout: Maximum wait time. Defaults to SHORT_TIMEOUT.

        Returns:
            True if element is visible, False otherwise.
        """
        wait_time = timeout or SHORT_TIMEOUT
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll(self, direction: str = "down", distance: float = 0.5):
        """Scroll the screen in the specified direction.

        Uses W3C Actions for reliable cross-platform scrolling.

        Args:
            direction: Scroll direction — "up" or "down". Default "down".
            distance: Scroll distance as fraction of screen height (0.0–1.0). Default 0.5.
        """
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]

        center_x = width // 2

        if direction == "down":
            start_y = int(height * 0.7)
            end_y = int(height * (0.7 - distance * 0.5))
        else:  # up
            start_y = int(height * 0.3)
            end_y = int(height * (0.3 + distance * 0.5))

        self.driver.swipe(center_x, start_y, center_x, end_y, duration=300)
        time.sleep(SCROLL_PAUSE)
        self.log.info("Scrolled %s (distance: %.1f)", direction, distance)

    def scroll_to_element(self, locator: tuple, direction: str = "down", max_attempts: int = None) -> bool:
        """Scroll until an element becomes visible.

        Args:
            locator: Tuple of (strategy, value) for the target element.
            direction: Scroll direction. Default "down".
            max_attempts: Maximum scroll attempts. Defaults to MAX_SCROLL_ATTEMPTS.

        Returns:
            True if element found, False if max attempts reached.
        """
        attempts = max_attempts or MAX_SCROLL_ATTEMPTS
        for i in range(attempts):
            if self.is_displayed(locator, timeout=2):
                self.log.info("Element found after %d scroll(s): %s", i, locator[1])
                return True
            self.scroll(direction=direction, distance=0.3)
        self.log.warning("Element not found after %d scrolls: %s", attempts, locator[1])
        return False

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """Get text content of an element.

        Args:
            locator: Tuple of (strategy, value).
            timeout: Wait timeout. Defaults to self.timeout.

        Returns:
            Text content of the element.
        """
        element = self.wait_for_element(locator, timeout)
        text = element.text
        self.log.info("Got text '%s' from: %s", text[:30] if text else "", locator[1])
        return text

    def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> Optional[str]:
        """Get an attribute value from an element.

        Args:
            locator: Tuple of (strategy, value).
            attribute: Attribute name to retrieve.
            timeout: Wait timeout. Defaults to self.timeout.

        Returns:
            Attribute value as string, or None if not found.
        """
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute)

    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = None) -> bool:
        """Wait for an element to become invisible or removed from DOM.

        Useful for waiting for loading spinners, splash screens, etc.

        Args:
            locator: Tuple of (strategy, value).
            timeout: Maximum wait time. Defaults to self.timeout.

        Returns:
            True if element disappeared, False if still visible after timeout.
        """
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def take_screenshot(self, filename: str) -> Optional[str]:
        """Capture a screenshot and save to the reports directory.

        Args:
            filename: Filename for the screenshot (e.g., "login_failure.png").

        Returns:
            Full path to saved screenshot, or None on failure.
        """
        try:
            import os
            from framework.utils.constants import REPORTS_DIR

            reports_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                REPORTS_DIR,
            )
            os.makedirs(reports_path, exist_ok=True)
            filepath = os.path.join(reports_path, filename)
            self.driver.save_screenshot(filepath)
            self.log.info("Screenshot saved: %s", filepath)
            return filepath
        except (WebDriverException, OSError) as e:
            self.log.error("Failed to save screenshot: %s", e.__class__.__name__)
            return None
