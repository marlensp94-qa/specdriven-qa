"""
Property-Based Tests for Marker System — Demo_QA
==================================================
Validates correctness properties of the marker system
using Hypothesis for property-based testing.

Properties tested:
- Property 7: Marker Validation Rejects Invalid Values
- Property 8: Marker Metadata Extraction

Run with:
    pytest tests/unit/test_markers.py -v
"""

from unittest.mock import MagicMock

import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

from framework.utils.markers import (
    test_type as marker_test_type,
    priority,
    get_test_metadata,
    VALID_TEST_TYPES,
    VALID_PRIORITIES,
    VALID_DOMAINS,
)


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Strings that are NOT valid test_type values
invalid_test_types = st.text(min_size=1, max_size=50).filter(
    lambda s: s not in VALID_TEST_TYPES
)

# Strings that are NOT valid priority values
invalid_priorities = st.text(min_size=1, max_size=50).filter(
    lambda s: s not in VALID_PRIORITIES
)

# Valid marker values for metadata extraction
valid_component_names = st.text(
    min_size=1, max_size=30,
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_- ")
).filter(lambda s: s.strip() != "")

valid_test_type_values = st.sampled_from(sorted(VALID_TEST_TYPES))
valid_priority_values = st.sampled_from(sorted(VALID_PRIORITIES))
valid_domain_values = st.sampled_from(sorted(VALID_DOMAINS))

# Optional marker values (None means marker not applied)
optional_component = st.one_of(st.none(), valid_component_names)
optional_test_type = st.one_of(st.none(), valid_test_type_values)
optional_priority = st.one_of(st.none(), valid_priority_values)
optional_domain = st.one_of(st.none(), valid_domain_values)


# =============================================================================
# Helpers
# =============================================================================

def make_mock_item(component_val=None, test_type_val=None, priority_val=None, domain_val=None):
    """Create a mock pytest item with the specified marker values.

    Simulates the pytest item.get_closest_marker() interface used by
    get_test_metadata().
    """
    item = MagicMock()

    def get_closest_marker(name):
        marker = MagicMock()
        if name == "component" and component_val is not None:
            marker.args = (component_val,)
            return marker
        elif name == "test_type" and test_type_val is not None:
            marker.args = (test_type_val,)
            return marker
        elif name == "priority" and priority_val is not None:
            marker.args = (priority_val,)
            return marker
        elif name == "domain" and domain_val is not None:
            marker.args = (domain_val,)
            return marker
        return None

    item.get_closest_marker = get_closest_marker
    return item


# =============================================================================
# Property 7: Marker Validation Rejects Invalid Values
# =============================================================================
# For any string that is not in the set of valid values for a marker type,
# applying that marker SHALL raise a ValueError indicating the invalid value
# and the list of allowed values.

class TestMarkerValidationRejectsInvalidValues:
    """Property 7: Marker Validation Rejects Invalid Values."""

    # Feature: qa-demo-training, Property 7: Marker Validation Rejects Invalid Values

    @given(invalid_value=invalid_test_types)
    @settings(max_examples=25)
    def test_invalid_test_type_raises_valueerror(self, invalid_value):
        """
        Any string not in the valid test_type set SHALL raise ValueError
        with the invalid value and allowed values in the message.

        **Validates: Requirements 3.6**
        """
        with pytest.raises(ValueError) as exc_info:
            marker_test_type(invalid_value)

        error_message = str(exc_info.value)

        # Error should mention the invalid value
        assert invalid_value in error_message, (
            f"ValueError should contain invalid value '{invalid_value}', "
            f"got: '{error_message}'"
        )

        # Error should mention the allowed values
        for valid_val in sorted(VALID_TEST_TYPES):
            assert valid_val in error_message, (
                f"ValueError should list allowed value '{valid_val}', "
                f"got: '{error_message}'"
            )

    @given(invalid_value=invalid_priorities)
    @settings(max_examples=25)
    def test_invalid_priority_raises_valueerror(self, invalid_value):
        """
        Any string not in the valid priority set SHALL raise ValueError
        with the invalid value and allowed values in the message.

        **Validates: Requirements 3.7**
        """
        with pytest.raises(ValueError) as exc_info:
            priority(invalid_value)

        error_message = str(exc_info.value)

        # Error should mention the invalid value
        assert invalid_value in error_message, (
            f"ValueError should contain invalid value '{invalid_value}', "
            f"got: '{error_message}'"
        )

        # Error should mention the allowed values
        for valid_val in sorted(VALID_PRIORITIES):
            assert valid_val in error_message, (
                f"ValueError should list allowed value '{valid_val}', "
                f"got: '{error_message}'"
            )

    @given(valid_value=valid_test_type_values)
    @settings(max_examples=25)
    def test_valid_test_type_does_not_raise(self, valid_value):
        """
        Any string in the valid test_type set SHALL NOT raise ValueError.

        **Validates: Requirements 3.6**
        """
        # Should not raise — returns a pytest mark decorator
        result = marker_test_type(valid_value)
        assert result is not None

    @given(valid_value=valid_priority_values)
    @settings(max_examples=25)
    def test_valid_priority_does_not_raise(self, valid_value):
        """
        Any string in the valid priority set SHALL NOT raise ValueError.

        **Validates: Requirements 3.7**
        """
        # Should not raise — returns a pytest mark decorator
        result = priority(valid_value)
        assert result is not None


# =============================================================================
# Property 8: Marker Metadata Extraction
# =============================================================================
# For any combination of valid markers (component, test_type, priority, domain)
# applied to a pytest test item, get_test_metadata(item) SHALL return a dictionary
# containing all applied marker values with correct keys and no data loss.

class TestMarkerMetadataExtraction:
    """Property 8: Marker Metadata Extraction."""

    # Feature: qa-demo-training, Property 8: Marker Metadata Extraction

    @given(
        component_val=optional_component,
        test_type_val=optional_test_type,
        priority_val=optional_priority,
        domain_val=optional_domain,
    )
    @settings(max_examples=25)
    def test_metadata_contains_all_applied_markers(
        self, component_val, test_type_val, priority_val, domain_val
    ):
        """
        For any combination of valid markers applied to a test item,
        get_test_metadata returns a dict with all applied values and correct keys.

        **Validates: Requirements 3.4**
        """
        item = make_mock_item(
            component_val=component_val,
            test_type_val=test_type_val,
            priority_val=priority_val,
            domain_val=domain_val,
        )

        metadata = get_test_metadata(item)

        # Verify the result is a dictionary with expected keys
        assert isinstance(metadata, dict)
        assert "component" in metadata
        assert "test_type" in metadata
        assert "priority" in metadata
        assert "domain" in metadata

        # Verify each applied marker value is correctly extracted
        assert metadata["component"] == component_val, (
            f"Expected component='{component_val}', got '{metadata['component']}'"
        )
        assert metadata["test_type"] == test_type_val, (
            f"Expected test_type='{test_type_val}', got '{metadata['test_type']}'"
        )
        assert metadata["priority"] == priority_val, (
            f"Expected priority='{priority_val}', got '{metadata['priority']}'"
        )
        assert metadata["domain"] == domain_val, (
            f"Expected domain='{domain_val}', got '{metadata['domain']}'"
        )

    @given(
        component_val=valid_component_names,
        test_type_val=valid_test_type_values,
        priority_val=valid_priority_values,
        domain_val=valid_domain_values,
    )
    @settings(max_examples=25)
    def test_all_markers_applied_no_data_loss(
        self, component_val, test_type_val, priority_val, domain_val
    ):
        """
        When ALL markers are applied, get_test_metadata returns all values
        with no data loss — every value is present and matches the input.

        **Validates: Requirements 3.4**
        """
        item = make_mock_item(
            component_val=component_val,
            test_type_val=test_type_val,
            priority_val=priority_val,
            domain_val=domain_val,
        )

        metadata = get_test_metadata(item)

        # No None values when all markers are applied
        assert metadata["component"] is not None
        assert metadata["test_type"] is not None
        assert metadata["priority"] is not None
        assert metadata["domain"] is not None

        # Exact value match
        assert metadata["component"] == component_val
        assert metadata["test_type"] == test_type_val
        assert metadata["priority"] == priority_val
        assert metadata["domain"] == domain_val

    def test_no_markers_returns_all_none(self):
        """
        When no markers are applied, get_test_metadata returns all None values.

        **Validates: Requirements 3.4**
        """
        item = make_mock_item()  # No markers applied

        metadata = get_test_metadata(item)

        assert metadata == {
            "component": None,
            "test_type": None,
            "priority": None,
            "domain": None,
        }

    @given(component_val=valid_component_names)
    @settings(max_examples=25)
    def test_partial_markers_preserves_applied_values(self, component_val):
        """
        When only some markers are applied, get_test_metadata returns the
        applied values and None for unapplied markers.

        **Validates: Requirements 3.4**
        """
        item = make_mock_item(component_val=component_val)

        metadata = get_test_metadata(item)

        assert metadata["component"] == component_val
        assert metadata["test_type"] is None
        assert metadata["priority"] is None
        assert metadata["domain"] is None
