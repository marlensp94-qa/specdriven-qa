"""
Property-Based Tests for Naming Validator — Demo_QA
=====================================================
Validates correctness properties of the test naming convention validator
using Hypothesis for property-based testing.

Properties tested:
- Property 6: Test Naming Convention Validation

Run with:
    pytest tests/unit/test_naming_validator.py -v
"""

import re

import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

from framework.utils.markers import validate_test_name


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Valid positive integers (as strings, no leading zeros except for padding)
positive_integers = st.integers(min_value=1, max_value=99999).map(str)

# Valid description: lowercase letters, digits, underscores, 1-60 chars
valid_descriptions = st.from_regex(r"[a-z0-9_]{1,60}", fullmatch=True)

# Valid test names: check_T{n}_{desc}
valid_test_names = st.builds(
    lambda n, desc: f"check_T{n}_{desc}",
    n=positive_integers,
    desc=valid_descriptions,
)

# Arbitrary strings that may or may not match the pattern
arbitrary_strings = st.text(min_size=0, max_size=200)

# Strings that definitely do NOT match the pattern (various violations)
invalid_prefixes = st.sampled_from([
    "test_",
    "check_",
    "check_t",
    "Check_T",
    "CHECK_T",
    "",
    "x",
    "check_T",
    "check_T_",
])

# Descriptions with invalid characters (uppercase, special chars)
invalid_descriptions = st.from_regex(r"[A-Z!@#$%^&*()+=\[\]{}<>?,./;:'\"|\\~` ]{1,60}", fullmatch=True)


# =============================================================================
# Property 6: Test Naming Convention Validation
# =============================================================================
# For any string, the naming validator SHALL accept it if and only if it matches
# the pattern check_T{n}_{desc} where n is a positive integer and desc contains
# only lowercase letters, digits, and underscores with a maximum length of 60 characters.

class TestNamingConventionValidation:
    """Property 6: Test Naming Convention Validation."""

    # Feature: qa-demo-training, Property 6: Test Naming Convention Validation

    @given(name=valid_test_names)
    @settings(max_examples=25)
    def test_valid_names_are_accepted(self, name):
        """
        Any string matching check_T{n}_{desc} with n > 0 and desc being
        lowercase letters, digits, underscores (1-60 chars) SHALL be accepted.

        **Validates: Requirements 3.2**
        """
        assert validate_test_name(name) is True, (
            f"Expected valid name '{name}' to be accepted"
        )

    @given(data=st.data())
    @settings(max_examples=25)
    def test_zero_id_is_rejected(self, data):
        """
        check_T0_{desc} SHALL be rejected because 0 is not a positive integer.

        **Validates: Requirements 3.2**
        """
        desc = data.draw(valid_descriptions)
        name = f"check_T0_{desc}"
        assert validate_test_name(name) is False, (
            f"Expected name with zero ID '{name}' to be rejected"
        )

    @given(desc=invalid_descriptions)
    @settings(max_examples=25)
    def test_invalid_description_chars_rejected(self, desc):
        """
        Descriptions containing uppercase letters or special characters
        SHALL be rejected.

        **Validates: Requirements 3.2**
        """
        name = f"check_T1_{desc}"
        assert validate_test_name(name) is False, (
            f"Expected name with invalid description '{name}' to be rejected"
        )

    @given(data=st.data())
    @settings(max_examples=25)
    def test_description_exceeding_60_chars_rejected(self, data):
        """
        Descriptions longer than 60 characters SHALL be rejected.

        **Validates: Requirements 3.2**
        """
        # Generate a description that is 61-120 chars long
        long_desc = data.draw(
            st.from_regex(r"[a-z0-9_]{61,120}", fullmatch=True)
        )
        name = f"check_T1_{long_desc}"
        assert validate_test_name(name) is False, (
            f"Expected name with description > 60 chars to be rejected (len={len(long_desc)})"
        )

    @given(name=arbitrary_strings)
    @settings(max_examples=25)
    def test_validator_matches_reference_regex(self, name):
        """
        For any string, validate_test_name returns True if and only if the
        string matches the reference pattern: ^check_T(\\d+)_([a-z0-9_]{1,60})$
        where the numeric part is a positive integer.

        **Validates: Requirements 3.2**
        """
        # Reference implementation of the expected behavior
        pattern = re.compile(r"^check_T(\d+)_([a-z0-9_]{1,60})$")
        match = pattern.match(name)
        expected = match is not None and int(match.group(1)) > 0

        result = validate_test_name(name)
        assert result == expected, (
            f"For input '{name}': expected {expected}, got {result}"
        )

    @given(prefix=invalid_prefixes, n=positive_integers, desc=valid_descriptions)
    @settings(max_examples=25)
    def test_wrong_prefix_rejected(self, prefix, n, desc):
        """
        Names not starting with 'check_T' SHALL be rejected.

        **Validates: Requirements 3.2**
        """
        name = f"{prefix}{n}_{desc}"
        # Only accept if it accidentally forms a valid name
        pattern = re.compile(r"^check_T(\d+)_([a-z0-9_]{1,60})$")
        match = pattern.match(name)
        expected = match is not None and int(match.group(1)) > 0

        result = validate_test_name(name)
        assert result == expected, (
            f"For input '{name}': expected {expected}, got {result}"
        )

    def test_empty_string_rejected(self):
        """Empty string SHALL be rejected.

        **Validates: Requirements 3.2**
        """
        assert validate_test_name("") is False

    def test_empty_description_rejected(self):
        """check_T1_ (empty description) SHALL be rejected.

        **Validates: Requirements 3.2**
        """
        assert validate_test_name("check_T1_") is False
