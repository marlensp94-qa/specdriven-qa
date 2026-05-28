"""
Marker System — Demo_QA
=========================
Custom pytest markers for test classification and traceability.
Provides decorator functions that validate marker values at collection time
and make metadata accessible to reporting hooks.

Markers:
- @component("Login") — Jira component for traceability
- @test_type("functional") — Test classification
- @priority("high") — Test priority level
- @domain("security") — Organizational domain grouping

Usage:
    from framework.utils.markers import component, test_type, priority, domain

    @component("Login")
    @test_type("functional")
    @priority("critical")
    @domain("security")
    @pytest.mark.smoke
    def check_T001_login_valid_credentials(driver):
        ...
"""

import pytest
from typing import List, Optional


# =============================================================================
# Valid Values
# =============================================================================

VALID_TEST_TYPES = frozenset({"functional", "smoke", "negative", "boundary", "integration"})
VALID_PRIORITIES = frozenset({"critical", "high", "medium", "low"})
VALID_DOMAINS = frozenset({"security", "user_experience", "integration", "performance", "offline"})


# =============================================================================
# Marker Decorators
# =============================================================================

def component(name: str):
    """Mark test with a Jira component name for traceability.

    Components link automated tests to Jira components, enabling filtering
    and reporting by functional area.

    Args:
        name: Component name (e.g., "Login", "Cart", "Checkout").

    Returns:
        pytest.mark decorator.

    Example:
        @component("Login")
        def check_T001_login_valid_credentials(driver):
            ...
    """
    return pytest.mark.component(name)


def test_type(type_name: str):
    """Classify test by type.

    Valid values:
    - 'functional': Standard functional verification
    - 'smoke': Critical path / smoke test
    - 'negative': Negative/error scenario
    - 'boundary': Boundary/edge case
    - 'integration': Integration with external systems

    Args:
        type_name: Test type identifier.

    Returns:
        pytest.mark decorator.

    Raises:
        ValueError: If type_name is not in the valid set.

    Example:
        @test_type("functional")
        def check_T001_login_valid_credentials(driver):
            ...
    """
    if type_name not in VALID_TEST_TYPES:
        raise ValueError(
            f"Invalid test_type '{type_name}'. "
            f"Must be one of: {sorted(VALID_TEST_TYPES)}"
        )
    return pytest.mark.test_type(type_name)


def priority(level: str):
    """Mark test priority level.

    Valid values:
    - 'critical': Blocks release if failing
    - 'high': Core flow, must pass for release
    - 'medium': Standard validation
    - 'low': Edge case, nice-to-have

    Args:
        level: Priority level string.

    Returns:
        pytest.mark decorator.

    Raises:
        ValueError: If level is not in the valid set.

    Example:
        @priority("critical")
        def check_T001_login_valid_credentials(driver):
            ...
    """
    if level not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{level}'. "
            f"Must be one of: {sorted(VALID_PRIORITIES)}"
        )
    return pytest.mark.priority(level)


def domain(domain_name: str):
    """Mark test domain for organizational grouping.

    Valid values:
    - 'security': Authentication, permissions, encryption
    - 'user_experience': UI, navigation, accessibility
    - 'integration': APIs, external systems, hardware
    - 'performance': Launch time, memory, responsiveness
    - 'offline': Offline mode, sync, data persistence

    Args:
        domain_name: Domain identifier.

    Returns:
        pytest.mark decorator.

    Raises:
        ValueError: If domain_name is not in the valid set.

    Example:
        @domain("security")
        def check_T001_login_valid_credentials(driver):
            ...
    """
    if domain_name not in VALID_DOMAINS:
        raise ValueError(
            f"Invalid domain '{domain_name}'. "
            f"Must be one of: {sorted(VALID_DOMAINS)}"
        )
    return pytest.mark.domain(domain_name)


# =============================================================================
# Metadata Extraction
# =============================================================================

def get_test_metadata(item) -> dict:
    """Extract all custom marker metadata from a pytest test item.

    Used by conftest.py hooks and the report generator to access
    marker data for each test.

    Args:
        item: pytest test item (from pytest hooks or fixtures).

    Returns:
        Dictionary with keys:
        - component: str or None
        - test_type: str or None
        - priority: str or None
        - domain: str or None

    Example:
        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(item, call):
            metadata = get_test_metadata(item)
            # metadata = {"component": "Login", "test_type": "functional", ...}
    """
    metadata = {
        "component": None,
        "test_type": None,
        "priority": None,
        "domain": None,
    }

    # Extract component marker
    component_marker = item.get_closest_marker("component")
    if component_marker and component_marker.args:
        metadata["component"] = component_marker.args[0]

    # Extract test_type marker
    test_type_marker = item.get_closest_marker("test_type")
    if test_type_marker and test_type_marker.args:
        metadata["test_type"] = test_type_marker.args[0]

    # Extract priority marker
    priority_marker = item.get_closest_marker("priority")
    if priority_marker and priority_marker.args:
        metadata["priority"] = priority_marker.args[0]

    # Extract domain marker
    domain_marker = item.get_closest_marker("domain")
    if domain_marker and domain_marker.args:
        metadata["domain"] = domain_marker.args[0]

    return metadata


# =============================================================================
# Naming Convention Validator
# =============================================================================

import re

# Pattern: check_T{positive_integer}_{description}
# Description: lowercase letters, digits, underscores, max 60 chars
_NAMING_PATTERN = re.compile(
    r"^check_T(\d+)_([a-z0-9_]{1,60})$"
)


def validate_test_name(name: str) -> bool:
    """Validate that a test function name follows the naming convention.

    Convention: check_T{number}_{description}
    - {number}: positive integer (test case ID from Test_Library)
    - {description}: lowercase letters, digits, underscores (max 60 chars)

    Args:
        name: Test function name to validate.

    Returns:
        True if name matches the convention, False otherwise.

    Example:
        validate_test_name("check_T001_login_valid_credentials")  # True
        validate_test_name("check_T12_add_to_cart")               # True
        validate_test_name("test_login")                          # False
        validate_test_name("check_T0_x")                          # False (0 not positive)
    """
    match = _NAMING_PATTERN.match(name)
    if match is None:
        return False

    # Verify the number is a positive integer (not 0)
    number = int(match.group(1))
    return number > 0


def get_test_case_id(name: str) -> Optional[int]:
    """Extract the test case ID number from a test function name.

    Args:
        name: Test function name following check_T{number}_{description} convention.

    Returns:
        Integer test case ID, or None if name doesn't match convention.

    Example:
        get_test_case_id("check_T001_login_valid")  # 1
        get_test_case_id("check_T42_checkout")      # 42
        get_test_case_id("test_something")          # None
    """
    match = _NAMING_PATTERN.match(name)
    if match is None:
        return None
    number = int(match.group(1))
    return number if number > 0 else None


# =============================================================================
# Convenience aliases
# =============================================================================

components = component  # Allow plural usage
