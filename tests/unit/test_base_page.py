"""
Property-Based Tests for BasePage — Demo_QA
=============================================
Validates correctness properties of the BasePage abstract class
using Hypothesis for property-based testing.

Properties tested:
- Property 4: Page Load Validation Error (PageNotLoadedError raised with page name + locator)
- Property 5: Lazy-Loading Deferred Element Location (single lookup, cached thereafter)

Run with:
    pytest tests/unit/test_base_page.py -v
"""

from unittest.mock import MagicMock, PropertyMock, patch, call
from typing import Tuple

import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

from framework.pages.base_page import BasePage, PageNotLoadedError, _LazyElement
from framework.utils.constants import PAGE_LOAD_TIMEOUT


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Locator strategies used in Appium
locator_strategies = st.sampled_from([
    "accessibility id",
    "id",
    "xpath",
    "class name",
    "-android uiautomator",
])

# Locator values — non-empty printable strings
locator_values = st.text(
    min_size=1,
    max_size=80,
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "S"), whitelist_characters=" _-./[]@")
).filter(lambda s: s.strip() != "")

# Locator tuples (strategy, value)
locator_tuples = st.tuples(locator_strategies, locator_values)

# Page class names — valid Python identifiers
page_class_names = st.from_regex(r"[A-Z][A-Za-z0-9]{2,30}Page", fullmatch=True)


# =============================================================================
# Helpers
# =============================================================================

def make_page_class(class_name: str, key_element: tuple):
    """Dynamically create a concrete BasePage subclass with the given name and key_element."""
    page_cls = type(class_name, (BasePage,), {"key_element": key_element})
    return page_cls


def make_failing_driver(key_element: tuple):
    """Create a mock driver that raises TimeoutException for the key_element."""
    from selenium.common.exceptions import TimeoutException

    driver = MagicMock()

    # Make WebDriverWait(...).until(...) raise TimeoutException
    # BasePage.validate_page uses WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(...)
    # We patch at the module level instead
    return driver


def make_successful_driver():
    """Create a mock driver where element lookups succeed."""
    driver = MagicMock()
    return driver


# =============================================================================
# Property 4: Page Load Validation Error
# =============================================================================
# For any page object class name and any locator tuple (strategy, value),
# when the underlying driver cannot find the key_element within the configured
# timeout, BasePage instantiation SHALL raise a PageNotLoadedError whose message
# contains both the page class name and the key_element locator.

class TestPageLoadValidationError:
    """Property 4: Page Load Validation Error."""

    # Feature: qa-demo-training, Property 4: Page Load Validation Error

    @given(class_name=page_class_names, key_element=locator_tuples)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_page_not_loaded_error_contains_class_name_and_locator(self, class_name, key_element):
        """
        When driver cannot find key_element within timeout, PageNotLoadedError
        is raised with both the page class name and the key_element locator in the message.

        **Validates: Requirements 2.3**
        """
        from selenium.common.exceptions import TimeoutException

        # Create a concrete subclass dynamically
        page_cls = make_page_class(class_name, key_element)

        # Create a mock driver
        driver = MagicMock()

        # Patch WebDriverWait to simulate timeout
        with patch("framework.pages.base_page.WebDriverWait") as mock_wait_class:
            mock_wait_instance = MagicMock()
            mock_wait_class.return_value = mock_wait_instance
            mock_wait_instance.until.side_effect = TimeoutException("Timed out")

            with pytest.raises(PageNotLoadedError) as exc_info:
                page_cls(driver)

            error = exc_info.value
            error_message = str(error)

            # Verify the error contains the page class name
            assert class_name in error_message, (
                f"PageNotLoadedError message should contain class name '{class_name}', "
                f"got: '{error_message}'"
            )

            # Verify the error contains the key_element locator
            assert str(key_element) in error_message, (
                f"PageNotLoadedError message should contain key_element '{key_element}', "
                f"got: '{error_message}'"
            )

            # Verify the error attributes
            assert error.page_name == class_name
            assert error.key_element == key_element

    @given(class_name=page_class_names, key_element=locator_tuples)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_page_not_loaded_error_on_no_such_element(self, class_name, key_element):
        """
        PageNotLoadedError is also raised when NoSuchElementException occurs
        during page validation.

        **Validates: Requirements 2.3**
        """
        from selenium.common.exceptions import NoSuchElementException

        page_cls = make_page_class(class_name, key_element)
        driver = MagicMock()

        with patch("framework.pages.base_page.WebDriverWait") as mock_wait_class:
            mock_wait_instance = MagicMock()
            mock_wait_class.return_value = mock_wait_instance
            mock_wait_instance.until.side_effect = NoSuchElementException("Not found")

            with pytest.raises(PageNotLoadedError) as exc_info:
                page_cls(driver)

            error = exc_info.value
            error_message = str(error)

            assert class_name in error_message
            assert str(key_element) in error_message
            assert error.page_name == class_name
            assert error.key_element == key_element


# =============================================================================
# Property 5: Lazy-Loading Deferred Element Location
# =============================================================================
# For any page object with locator properties, accessing a locator property for
# the first time SHALL trigger exactly one element lookup call, and subsequent
# accesses of the same property SHALL not trigger additional lookups (cached).

class TestLazyLoadingDeferredElementLocation:
    """Property 5: Lazy-Loading Deferred Element Location."""

    # Feature: qa-demo-training, Property 5: Lazy-Loading Deferred Element Location

    @given(locator=locator_tuples)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_first_access_triggers_exactly_one_lookup(self, locator):
        """
        Accessing a lazy-loaded locator property for the first time triggers
        exactly one element lookup call.

        **Validates: Requirements 2.4**
        """
        # Create a page class with a LazyElement descriptor
        page_cls = type("TestPage", (BasePage,), {
            "key_element": ("accessibility id", "test_key"),
            "my_element": _LazyElement(locator),
        })

        driver = MagicMock()
        mock_element = MagicMock()
        mock_element.is_displayed.return_value = True

        # Patch WebDriverWait for both validate_page and element lookup
        with patch("framework.pages.base_page.WebDriverWait") as mock_wait_class:
            mock_wait_instance = MagicMock()
            mock_wait_class.return_value = mock_wait_instance
            mock_wait_instance.until.return_value = mock_element

            # Instantiate page (validate_page will succeed)
            page = page_cls(driver)

            # Reset mock to track only the lazy element access
            mock_wait_class.reset_mock()
            mock_wait_instance.until.reset_mock()
            mock_wait_instance.until.return_value = mock_element

            # First access — should trigger one lookup
            result = page.my_element

            assert result == mock_element
            # wait_for_element is called which uses WebDriverWait
            assert mock_wait_class.call_count == 1, (
                f"Expected exactly 1 WebDriverWait call on first access, "
                f"got {mock_wait_class.call_count}"
            )

    @given(locator=locator_tuples, access_count=st.integers(min_value=2, max_value=10))
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_subsequent_accesses_use_cache(self, locator, access_count):
        """
        After the first access, subsequent accesses of the same property
        return the cached element without additional lookups.

        **Validates: Requirements 2.4**
        """
        page_cls = type("CachedPage", (BasePage,), {
            "key_element": ("accessibility id", "cached_key"),
            "cached_element": _LazyElement(locator),
        })

        driver = MagicMock()
        mock_element = MagicMock()
        mock_element.is_displayed.return_value = True

        with patch("framework.pages.base_page.WebDriverWait") as mock_wait_class:
            mock_wait_instance = MagicMock()
            mock_wait_class.return_value = mock_wait_instance
            mock_wait_instance.until.return_value = mock_element

            page = page_cls(driver)

            # Reset to track only lazy element accesses
            mock_wait_class.reset_mock()
            mock_wait_instance.until.reset_mock()
            mock_wait_instance.until.return_value = mock_element

            # First access
            first_result = page.cached_element
            first_call_count = mock_wait_class.call_count

            # Subsequent accesses — should NOT trigger additional lookups
            for i in range(access_count - 1):
                result = page.cached_element
                assert result == mock_element, (
                    f"Access #{i + 2} should return same cached element"
                )

            # Total WebDriverWait calls should still be 1 (only from first access)
            assert mock_wait_class.call_count == first_call_count, (
                f"Expected no additional lookups after first access. "
                f"First access calls: {first_call_count}, "
                f"Total after {access_count} accesses: {mock_wait_class.call_count}"
            )

    @given(
        locator_a=locator_tuples,
        locator_b=locator_tuples,
    )
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_different_properties_cached_independently(self, locator_a, locator_b):
        """
        Multiple lazy-loaded properties are cached independently — accessing
        one does not affect the cache of another.

        **Validates: Requirements 2.4**
        """
        page_cls = type("MultiPropPage", (BasePage,), {
            "key_element": ("accessibility id", "multi_key"),
            "element_a": _LazyElement(locator_a),
            "element_b": _LazyElement(locator_b),
        })

        driver = MagicMock()
        mock_element_a = MagicMock(name="element_a")
        mock_element_a.is_displayed.return_value = True
        mock_element_b = MagicMock(name="element_b")
        mock_element_b.is_displayed.return_value = True

        with patch("framework.pages.base_page.WebDriverWait") as mock_wait_class:
            mock_wait_instance = MagicMock()
            mock_wait_class.return_value = mock_wait_instance
            # Return different elements for validate_page and each lazy access
            mock_wait_instance.until.return_value = mock_element_a

            page = page_cls(driver)

            # Reset tracking
            mock_wait_class.reset_mock()
            mock_wait_instance.until.reset_mock()

            # Set up side_effect to return different elements for each call
            mock_wait_instance.until.side_effect = [mock_element_a, mock_element_b]

            # Access element_a
            result_a = page.element_a
            assert result_a == mock_element_a

            # Access element_b
            result_b = page.element_b
            assert result_b == mock_element_b

            # Total lookups should be exactly 2 (one per property)
            assert mock_wait_class.call_count == 2, (
                f"Expected 2 lookups (one per property), got {mock_wait_class.call_count}"
            )

            # Now access both again — should use cache
            mock_wait_class.reset_mock()
            mock_wait_instance.until.reset_mock()

            cached_a = page.element_a
            cached_b = page.element_b

            assert cached_a == mock_element_a
            assert cached_b == mock_element_b
            assert mock_wait_class.call_count == 0, (
                "Subsequent accesses should use cache, no new lookups"
            )
