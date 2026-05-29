"""
Property-Based Tests for Flow Parameter Validation — Demo_QA
==============================================================
Validates correctness properties of reusable flow functions'
parameter validation using Hypothesis for property-based testing.

Properties tested:
- Property 10: Flow Parameter Validation

Run with:
    pytest tests/unit/test_flows_validation.py -v
"""

from unittest.mock import MagicMock

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from tests.flows.login_flow import login_flow
from tests.flows.cart_flow import add_product_to_cart_flow
from tests.flows.checkout_flow import complete_checkout_flow


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Invalid string values: None, empty string, or whitespace-only strings
whitespace_only = st.text(
    alphabet=" \t\n\r\x0b\x0c",
    min_size=1,
    max_size=20,
)

invalid_string_params = st.one_of(
    st.none(),
    st.just(""),
    whitespace_only,
)


# =============================================================================
# Helpers
# =============================================================================

def make_mock_driver():
    """Create a mock Appium driver for testing validation logic.

    The flow functions validate parameters BEFORE using the driver,
    so the mock doesn't need real Appium behavior.
    """
    return MagicMock()


# =============================================================================
# Property 10: Flow Parameter Validation
# =============================================================================
# For any reusable flow function (login_flow, add_product_to_cart_flow,
# complete_checkout_flow) and any of its required string parameters,
# passing None, an empty string, or a string composed entirely of whitespace
# SHALL raise a ValueError whose message identifies which parameter failed
# validation.

# Feature: qa-demo-training, Property 10: Flow Parameter Validation


class TestLoginFlowParameterValidation:
    """Property 10: Flow Parameter Validation — login_flow."""

    # Feature: qa-demo-training, Property 10: Flow Parameter Validation

    @given(invalid_username=invalid_string_params)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_login_flow_rejects_invalid_username(self, invalid_username):
        """
        For login_flow, passing None, empty, or whitespace-only username
        SHALL raise a ValueError whose message identifies 'username'.

        **Validates: Requirements 14.3**
        """
        driver = make_mock_driver()

        with pytest.raises(ValueError) as exc_info:
            login_flow(driver, invalid_username, "valid_password")

        error_message = str(exc_info.value)
        assert "username" in error_message.lower(), (
            f"ValueError should identify 'username' parameter, "
            f"got: '{error_message}'"
        )

    @given(invalid_password=invalid_string_params)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_login_flow_rejects_invalid_password(self, invalid_password):
        """
        For login_flow, passing None, empty, or whitespace-only password
        SHALL raise a ValueError whose message identifies 'password'.

        **Validates: Requirements 14.3**
        """
        driver = make_mock_driver()

        with pytest.raises(ValueError) as exc_info:
            login_flow(driver, "valid_user", invalid_password)

        error_message = str(exc_info.value)
        assert "password" in error_message.lower(), (
            f"ValueError should identify 'password' parameter, "
            f"got: '{error_message}'"
        )


class TestAddProductToCartFlowParameterValidation:
    """Property 10: Flow Parameter Validation — add_product_to_cart_flow."""

    # Feature: qa-demo-training, Property 10: Flow Parameter Validation

    @given(invalid_product_name=invalid_string_params)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_add_product_to_cart_flow_rejects_invalid_product_name(self, invalid_product_name):
        """
        For add_product_to_cart_flow, passing None, empty, or whitespace-only
        product_name SHALL raise a ValueError whose message identifies
        'product_name'.

        **Validates: Requirements 14.3**
        """
        driver = make_mock_driver()

        with pytest.raises(ValueError) as exc_info:
            add_product_to_cart_flow(driver, invalid_product_name)

        error_message = str(exc_info.value)
        assert "product_name" in error_message.lower(), (
            f"ValueError should identify 'product_name' parameter, "
            f"got: '{error_message}'"
        )


class TestCompleteCheckoutFlowParameterValidation:
    """Property 10: Flow Parameter Validation — complete_checkout_flow."""

    # Feature: qa-demo-training, Property 10: Flow Parameter Validation

    @given(invalid_first_name=invalid_string_params)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_complete_checkout_flow_rejects_invalid_first_name(self, invalid_first_name):
        """
        For complete_checkout_flow, passing None, empty, or whitespace-only
        first_name SHALL raise a ValueError whose message identifies
        'first_name'.

        **Validates: Requirements 14.3**
        """
        driver = make_mock_driver()

        with pytest.raises(ValueError) as exc_info:
            complete_checkout_flow(driver, invalid_first_name, "Doe", "12345")

        error_message = str(exc_info.value)
        assert "first_name" in error_message.lower(), (
            f"ValueError should identify 'first_name' parameter, "
            f"got: '{error_message}'"
        )

    @given(invalid_last_name=invalid_string_params)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_complete_checkout_flow_rejects_invalid_last_name(self, invalid_last_name):
        """
        For complete_checkout_flow, passing None, empty, or whitespace-only
        last_name SHALL raise a ValueError whose message identifies
        'last_name'.

        **Validates: Requirements 14.3**
        """
        driver = make_mock_driver()

        with pytest.raises(ValueError) as exc_info:
            complete_checkout_flow(driver, "John", invalid_last_name, "12345")

        error_message = str(exc_info.value)
        assert "last_name" in error_message.lower(), (
            f"ValueError should identify 'last_name' parameter, "
            f"got: '{error_message}'"
        )

    @given(invalid_zip_code=invalid_string_params)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_complete_checkout_flow_rejects_invalid_zip_code(self, invalid_zip_code):
        """
        For complete_checkout_flow, passing None, empty, or whitespace-only
        zip_code SHALL raise a ValueError whose message identifies
        'zip_code'.

        **Validates: Requirements 14.3**
        """
        driver = make_mock_driver()

        with pytest.raises(ValueError) as exc_info:
            complete_checkout_flow(driver, "John", "Doe", invalid_zip_code)

        error_message = str(exc_info.value)
        assert "zip_code" in error_message.lower(), (
            f"ValueError should identify 'zip_code' parameter, "
            f"got: '{error_message}'"
        )
