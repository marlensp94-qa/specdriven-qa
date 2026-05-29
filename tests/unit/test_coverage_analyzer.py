"""
Property-Based Tests for CoverageAnalyzer — Demo_QA
=====================================================
Validates correctness properties of the coverage analysis system
using Hypothesis for property-based testing.

Properties tested:
- Property 12: Coverage Mapping Correctness (matching, gaps, no duplicates/phantoms)

Run with:
    pytest tests/unit/test_coverage_analyzer.py -v
"""

import os
import ast
import tempfile
import shutil
from pathlib import Path

import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

from framework.utils.coverage_analyzer import (
    CoverageAnalyzer,
    CoverageMapping,
    CoverageReport,
    ParsedTestCase,
)


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Generate positive integer IDs (1-999) for test cases
test_case_ids = st.integers(min_value=1, max_value=999)

# Generate feature names for test case IDs (e.g., LOGIN, CART, CATALOG, CHECKOUT)
feature_names = st.sampled_from(["LOGIN", "CART", "CATALOG", "CHECKOUT", "PRODUCT"])

# Generate valid check script description suffixes (lowercase, digits, underscores)
script_descriptions = st.from_regex(r"[a-z][a-z0-9_]{2,20}", fullmatch=True)

# Generate test case titles
test_case_titles = st.text(
    min_size=5, max_size=60,
    alphabet=st.characters(whitelist_categories=("L", "N", "Z"))
).filter(lambda s: s.strip() != "")

# Automation dependency categories
dependency_categories = st.sampled_from(["A", "B", "C", "D"])

# Automation statuses for manual test cases
automation_statuses = st.sampled_from(["automated", "planned", "manual-only"])


def make_test_case_id(feature: str, numeric_id: int) -> str:
    """Build a test case ID like TC_LOGIN_001."""
    return f"TC_{feature}_{numeric_id:03d}"


def make_check_script_name(numeric_id: int, description: str) -> str:
    """Build a check script function name like check_T1_login_valid."""
    return f"check_T{numeric_id}_{description}"


# Strategy for generating a set of unique numeric IDs
unique_id_lists = st.lists(
    test_case_ids,
    min_size=1,
    max_size=20,
    unique=True,
)


# =============================================================================
# Helpers
# =============================================================================


def create_temp_project():
    """Create a fresh temporary project directory with test_library and tests dirs."""
    temp_dir = tempfile.mkdtemp()
    test_library = os.path.join(temp_dir, "test_library")
    tests_path = os.path.join(temp_dir, "tests", "check_scripts")
    os.makedirs(test_library)
    os.makedirs(tests_path)
    return temp_dir, test_library, tests_path


def write_test_case_md(test_library_path: str, feature: str, numeric_id: int, title: str, status: str, dependency: str):
    """Write a markdown test case file to the test library."""
    feature_dir = os.path.join(test_library_path, feature.lower())
    os.makedirs(feature_dir, exist_ok=True)

    tc_id = make_test_case_id(feature, numeric_id)
    file_path = os.path.join(feature_dir, f"{tc_id}.md")

    content = f"""# Test Case: {tc_id} — {title}

## Test Case Information

| Field | Value |
|-------|-------|
| **ID** | {tc_id} |
| **Title** | {title} |
| **Priority** | High |
| **Automation Status** | {status} |
| **Automation Dependency** | {dependency} |

## Objective

Verify that the feature works correctly.

## Preconditions

- App is installed
- User is on the home screen

## Steps

1. Open the app
2. Navigate to the feature
3. Perform the action

## Expected Results

1. App opens successfully
2. Feature screen is displayed
3. Action completes as expected
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def write_check_script(tests_path: str, numeric_id: int, description: str):
    """Write a Python check script file with a matching function."""
    func_name = make_check_script_name(numeric_id, description)
    file_name = f"check_T{numeric_id:03d}_{description}.py"
    file_path = os.path.join(tests_path, file_name)

    content = f'''"""Check script for test case T{numeric_id}."""

import pytest


def {func_name}():
    """Automated test for T{numeric_id}."""
    assert True
'''
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


# =============================================================================
# Property 12: Coverage Mapping Correctness
# =============================================================================
# For any set of manual test case IDs and set of check script function names
# following the check_T{id}_{desc} pattern, the CoverageAnalyzer SHALL correctly
# match each test case ID to its corresponding check script (by extracting the
# numeric ID), report unmatched test cases as gaps, and never produce duplicate
# or phantom mappings.
#
# Feature: qa-demo-training, Property 12: Coverage Mapping Correctness


class TestCoverageMappingCorrectness:
    """Property 12: Coverage Mapping Correctness.

    **Validates: Requirements 16.1**
    """

    @given(
        all_ids=unique_id_lists,
        automated_fraction=st.floats(min_value=0.0, max_value=1.0),
        feature=feature_names,
        descriptions=st.lists(script_descriptions, min_size=20, max_size=20),
        dependency=dependency_categories,
    )
    @settings(
        max_examples=100,
        suppress_health_check=[HealthCheck.too_slow],
        deadline=None,
    )
    def test_correct_matching_by_numeric_id(
        self, all_ids, automated_fraction, feature, descriptions, dependency
    ):
        """
        CoverageAnalyzer correctly matches test cases to check scripts by numeric ID.

        **Validates: Requirements 16.1**
        """
        temp_dir, test_library, tests_path = create_temp_project()
        try:
            # Determine which IDs will have corresponding check scripts
            num_automated = max(0, int(len(all_ids) * automated_fraction))
            automated_ids = set(all_ids[:num_automated])

            # Write test case markdown files for ALL IDs
            for i, numeric_id in enumerate(all_ids):
                title = f"Test case for feature {numeric_id}"
                status = "automated" if numeric_id in automated_ids else "planned"
                write_test_case_md(test_library, feature, numeric_id, title, status, dependency)

            # Write check scripts ONLY for automated IDs
            for i, numeric_id in enumerate(sorted(automated_ids)):
                desc = descriptions[i % len(descriptions)]
                write_check_script(tests_path, numeric_id, desc)

            # Run the analyzer
            analyzer = CoverageAnalyzer(
                test_library_path=test_library,
                tests_path=tests_path,
            )
            report = analyzer.analyze()

            # --- PROPERTY ASSERTIONS ---

            # 1. Every test case in the library appears exactly once in mappings
            mapped_ids = [m.test_case_id for m in report.mappings]
            expected_ids = [make_test_case_id(feature, nid) for nid in all_ids]
            assert sorted(mapped_ids) == sorted(expected_ids), (
                f"Mismatch between mapped IDs and expected IDs.\n"
                f"Mapped: {sorted(mapped_ids)}\n"
                f"Expected: {sorted(expected_ids)}"
            )

            # 2. No duplicate mappings (each test case ID appears exactly once)
            assert len(mapped_ids) == len(set(mapped_ids)), (
                f"Duplicate mappings found: {[x for x in mapped_ids if mapped_ids.count(x) > 1]}"
            )

            # 3. Automated test cases are correctly matched to their scripts
            for mapping in report.mappings:
                tc_id = mapping.test_case_id
                id_match = CoverageAnalyzer._TC_ID_PATTERN.search(tc_id)
                if id_match:
                    numeric_id = int(id_match.group(1))
                    if numeric_id in automated_ids:
                        # Should have a matching check script
                        assert mapping.check_script is not None, (
                            f"Test case {tc_id} (ID {numeric_id}) should be matched "
                            f"to a check script but got None"
                        )
                        assert mapping.status == "automated", (
                            f"Test case {tc_id} matched to script but status is "
                            f"'{mapping.status}' instead of 'automated'"
                        )
                        # The matched script should contain the correct numeric ID
                        script_match = CoverageAnalyzer._CHECK_SCRIPT_PATTERN.match(
                            mapping.check_script
                        )
                        assert script_match is not None, (
                            f"Matched script '{mapping.check_script}' doesn't follow "
                            f"check_T{{id}}_{{desc}} pattern"
                        )
                        script_numeric_id = int(script_match.group(1))
                        assert script_numeric_id == numeric_id, (
                            f"Test case {tc_id} (ID {numeric_id}) matched to script "
                            f"with ID {script_numeric_id}"
                        )

            # 4. No phantom mappings (scripts that don't exist shouldn't appear)
            all_script_names = set()
            for py_file in Path(tests_path).glob("check_*.py"):
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if CoverageAnalyzer._CHECK_SCRIPT_PATTERN.match(node.name):
                            all_script_names.add(node.name)

            for mapping in report.mappings:
                if mapping.check_script is not None:
                    assert mapping.check_script in all_script_names, (
                        f"Phantom mapping: '{mapping.check_script}' doesn't exist "
                        f"in check scripts directory"
                    )
        finally:
            shutil.rmtree(temp_dir)

    @given(
        all_ids=unique_id_lists,
        feature=feature_names,
        dependency=dependency_categories,
    )
    @settings(
        max_examples=100,
        suppress_health_check=[HealthCheck.too_slow],
        deadline=None,
    )
    def test_unmatched_cases_reported_as_gaps(
        self, all_ids, feature, dependency
    ):
        """
        Test cases without corresponding check scripts are reported as gaps.

        **Validates: Requirements 16.1**
        """
        temp_dir, test_library, tests_path = create_temp_project()
        try:
            # Write test cases but NO check scripts — all should be gaps
            for numeric_id in all_ids:
                title = f"Unmatched test case {numeric_id}"
                write_test_case_md(test_library, feature, numeric_id, title, "planned", dependency)

            # Run the analyzer
            analyzer = CoverageAnalyzer(
                test_library_path=test_library,
                tests_path=tests_path,
            )
            report = analyzer.analyze()

            # All test cases should appear in gaps
            gap_ids = [g.test_case_id for g in report.gaps]
            expected_ids = [make_test_case_id(feature, nid) for nid in all_ids]
            assert sorted(gap_ids) == sorted(expected_ids), (
                f"Not all unmatched cases reported as gaps.\n"
                f"Gaps: {sorted(gap_ids)}\n"
                f"Expected: {sorted(expected_ids)}"
            )

            # None of the gaps should have a check_script assigned
            for gap in report.gaps:
                assert gap.check_script is None, (
                    f"Gap {gap.test_case_id} has check_script '{gap.check_script}' "
                    f"but should be None"
                )

            # Gap status should never be "automated"
            for gap in report.gaps:
                assert gap.status != "automated", (
                    f"Gap {gap.test_case_id} has status 'automated' but no script exists"
                )
        finally:
            shutil.rmtree(temp_dir)

    @given(
        all_ids=unique_id_lists,
        feature=feature_names,
        descriptions=st.lists(script_descriptions, min_size=20, max_size=20),
        dependency=dependency_categories,
    )
    @settings(
        max_examples=100,
        suppress_health_check=[HealthCheck.too_slow],
        deadline=None,
    )
    def test_no_duplicate_script_assignments(
        self, all_ids, feature, descriptions, dependency
    ):
        """
        Each check script is assigned to at most one test case (no duplicates).

        **Validates: Requirements 16.1**
        """
        temp_dir, test_library, tests_path = create_temp_project()
        try:
            # Write test cases and scripts for all IDs
            for i, numeric_id in enumerate(all_ids):
                title = f"Test case {numeric_id}"
                write_test_case_md(test_library, feature, numeric_id, title, "automated", dependency)
                desc = descriptions[i % len(descriptions)]
                write_check_script(tests_path, numeric_id, desc)

            # Run the analyzer
            analyzer = CoverageAnalyzer(
                test_library_path=test_library,
                tests_path=tests_path,
            )
            report = analyzer.analyze()

            # Collect all assigned scripts (non-None)
            assigned_scripts = [
                m.check_script for m in report.mappings if m.check_script is not None
            ]

            # No script should be assigned to more than one test case
            assert len(assigned_scripts) == len(set(assigned_scripts)), (
                f"Duplicate script assignments found: "
                f"{[s for s in assigned_scripts if assigned_scripts.count(s) > 1]}"
            )
        finally:
            shutil.rmtree(temp_dir)

    @given(
        all_ids=unique_id_lists,
        feature=feature_names,
        descriptions=st.lists(script_descriptions, min_size=20, max_size=20),
        dependency=dependency_categories,
    )
    @settings(
        max_examples=100,
        suppress_health_check=[HealthCheck.too_slow],
        deadline=None,
    )
    def test_statistics_match_mappings(
        self, all_ids, feature, descriptions, dependency
    ):
        """
        Coverage statistics accurately reflect the mapping results.

        **Validates: Requirements 16.1**
        """
        temp_dir, test_library, tests_path = create_temp_project()
        try:
            # Automate roughly half the IDs
            half = len(all_ids) // 2
            automated_ids = all_ids[:half]

            for i, numeric_id in enumerate(all_ids):
                title = f"Test case {numeric_id}"
                status = "automated" if numeric_id in automated_ids else "manual-only"
                write_test_case_md(test_library, feature, numeric_id, title, status, dependency)

            for i, numeric_id in enumerate(automated_ids):
                desc = descriptions[i % len(descriptions)]
                write_check_script(tests_path, numeric_id, desc)

            # Run the analyzer
            analyzer = CoverageAnalyzer(
                test_library_path=test_library,
                tests_path=tests_path,
            )
            report = analyzer.analyze()

            # Verify statistics match actual mappings
            stats = report.statistics
            actual_automated = sum(1 for m in report.mappings if m.status == "automated")
            actual_planned = sum(1 for m in report.mappings if m.status == "planned")
            actual_manual = sum(1 for m in report.mappings if m.status == "manual-only")

            assert stats["total"] == len(report.mappings), (
                f"Stats total {stats['total']} != mappings count {len(report.mappings)}"
            )
            assert stats["automated"] == actual_automated, (
                f"Stats automated {stats['automated']} != actual {actual_automated}"
            )
            assert stats["planned"] == actual_planned, (
                f"Stats planned {stats['planned']} != actual {actual_planned}"
            )
            assert stats["manual_only"] == actual_manual, (
                f"Stats manual_only {stats['manual_only']} != actual {actual_manual}"
            )

            # Coverage rate should be correct
            expected_rate = (actual_automated / len(report.mappings) * 100) if report.mappings else 0.0
            assert abs(stats["coverage_rate"] - expected_rate) < 0.01, (
                f"Coverage rate {stats['coverage_rate']} != expected {expected_rate}"
            )
        finally:
            shutil.rmtree(temp_dir)
