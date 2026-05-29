"""
Property-Based Tests for Test Case Parser — Demo_QA
=====================================================
Validates correctness properties of the test case parser within the
CoverageAnalyzer, ensuring all markdown test case files in the test_library/
directory yield mandatory fields with correct constraints.

Properties tested:
- Property 11: Test Case Structure Validation

Run with:
    pytest tests/unit/test_case_parser.py -v
"""

import re
from pathlib import Path

import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

# =============================================================================
# Constants
# =============================================================================

# Valid values for constrained fields
VALID_PRIORITIES = {"High", "Normal", "Low"}
VALID_AUTOMATION_DEPENDENCIES = {"A", "B", "C", "D"}

# Pattern for test case IDs
TC_ID_PATTERN = re.compile(r"^TC_[A-Z]+_\d{3}$")

# Test library path relative to project root
TEST_LIBRARY_PATH = Path(__file__).resolve().parent.parent.parent / "test_library"

# Feature subdirectories
FEATURE_DIRS = ["login", "cart", "catalog", "checkout"]


# =============================================================================
# Helper: Full Test Case Parser
# =============================================================================

def parse_test_case_full(file_path: Path) -> dict:
    """Parse a markdown test case file and extract all mandatory fields.

    This parser handles both formats found in the test library:
    1. Section-based (## Test Case ID, ## Title, etc.)
    2. Table-based (## Test Case Information with | Field | Value | table)

    Returns a dict with keys:
        id, title, objective, preconditions, steps, expected_results,
        priority, test_scope, automation_status, automation_dependency
    """
    content = file_path.read_text(encoding="utf-8")
    result = {
        "id": None,
        "title": None,
        "objective": None,
        "preconditions": [],
        "steps": [],
        "expected_results": [],
        "priority": None,
        "test_scope": None,
        "automation_status": None,
        "automation_dependency": None,
    }

    # --- Try table-based format (## Test Case Information) ---
    table_match = re.search(
        r"##\s+Test Case Information\s*\n\s*\|.*\|.*\|\s*\n\s*\|[-\s|]+\|\s*\n((?:\s*\|.*\|.*\n)+)",
        content,
    )
    if table_match:
        table_rows = table_match.group(1)
        for row in table_rows.strip().split("\n"):
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if len(cells) >= 2:
                field_name = re.sub(r"\*+", "", cells[0]).strip().lower()
                value = cells[1].strip()

                if field_name == "id":
                    result["id"] = value
                elif field_name == "title":
                    result["title"] = value
                elif field_name == "priority":
                    result["priority"] = value
                elif field_name == "test scope":
                    result["test_scope"] = value
                elif field_name == "automation status":
                    result["automation_status"] = value
                elif field_name in ("automation dependency", "automation dependency category"):
                    result["automation_dependency"] = value

    # --- Section-based format fallbacks ---
    if not result["id"]:
        id_match = re.search(r"##\s+Test Case ID\s*\n\s*(.+)", content)
        if id_match:
            result["id"] = id_match.group(1).strip()

    if not result["title"]:
        title_match = re.search(r"##\s+Title\s*\n\s*(.+)", content)
        if title_match:
            result["title"] = title_match.group(1).strip()

    if not result["objective"]:
        obj_match = re.search(r"##\s+Objective\s*\n\s*(.+)", content)
        if obj_match:
            result["objective"] = obj_match.group(1).strip()

    if not result["preconditions"]:
        prec_match = re.search(
            r"##\s+Preconditions\s*\n((?:\s*[-*]\s+.+\n?)+)", content
        )
        if prec_match:
            prec_text = prec_match.group(1)
            result["preconditions"] = [
                line.strip().lstrip("-*").strip()
                for line in prec_text.strip().split("\n")
                if line.strip() and line.strip().startswith(("-", "*"))
            ]

    # Parse test steps table
    steps_match = re.search(
        r"##\s+Test Steps\s*\n\s*\|.*\|.*\|.*\|\s*\n\s*\|[-\s|]+\|\s*\n((?:\s*\|.*\|.*\|.*\n?)+)",
        content,
    )
    if steps_match:
        steps_text = steps_match.group(1)
        for row in steps_text.strip().split("\n"):
            cells = [c.strip() for c in row.split("|") if c.strip()]
            if len(cells) >= 3:
                step_num = cells[0].strip()
                action = cells[1].strip()
                expected = cells[2].strip()
                if step_num.isdigit():
                    result["steps"].append(action)
                    result["expected_results"].append(expected)

    if not result["priority"]:
        priority_match = re.search(r"##\s+Priority\s*\n\s*(.+)", content)
        if priority_match:
            result["priority"] = priority_match.group(1).strip()

    if not result["test_scope"]:
        scope_match = re.search(r"##\s+Test Scope\s*\n\s*(.+)", content)
        if scope_match:
            result["test_scope"] = scope_match.group(1).strip()

    if not result["automation_status"]:
        status_match = re.search(r"##\s+Automation Status\s*\n\s*(.+)", content)
        if status_match:
            result["automation_status"] = status_match.group(1).strip()

    if not result["automation_dependency"]:
        dep_match = re.search(
            r"##\s+Automation Dependency(?:\s+Category)?\s*\n\s*(.+)", content
        )
        if dep_match:
            result["automation_dependency"] = dep_match.group(1).strip()

    # Fallback: extract ID from filename
    if not result["id"]:
        result["id"] = file_path.stem

    # Fallback: extract title from first heading
    if not result["title"]:
        heading_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
        if heading_match:
            raw_title = heading_match.group(1).strip()
            raw_title = re.sub(r"^Test Case:\s*", "", raw_title)
            raw_title = re.sub(r"^TC_\w+\s*[—–-]\s*", "", raw_title)
            result["title"] = raw_title if raw_title else file_path.stem

    return result


# =============================================================================
# Discover all test case files
# =============================================================================

def discover_test_case_files() -> list:
    """Discover all TC_*.md files in the test_library/ subdirectories."""
    files = []
    if not TEST_LIBRARY_PATH.exists():
        return files

    for feature_dir in FEATURE_DIRS:
        dir_path = TEST_LIBRARY_PATH / feature_dir
        if dir_path.exists():
            for md_file in sorted(dir_path.glob("TC_*.md")):
                files.append(md_file)

    return files


# All test case files for parametrization
ALL_TEST_CASE_FILES = discover_test_case_files()


# =============================================================================
# Property 11: Test Case Structure Validation
# =============================================================================
# For any markdown file in the test_library/ directory, parsing it SHALL yield
# all mandatory fields (ID matching TC_[feature]_[number], title ≤80 chars,
# objective starting with "Verify that..." or "Ensure that...",
# preconditions as list, steps numbered with ≥3 entries, expected results
# one per step, priority in {High, Normal, Low}, test scope, automation status,
# automation dependency in {A, B, C, D}).
#
# **Validates: Requirements 9.2, 9.4**


class TestTestCaseStructureValidation:
    """Property 11: Test Case Structure Validation."""

    # Feature: qa-demo-training, Property 11: Test Case Structure Validation

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_id_matches_pattern(self, tc_file):
        """Test case ID matches TC_[feature]_[number] pattern."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["id"] is not None, f"ID is missing in {tc_file.name}"
        assert TC_ID_PATTERN.match(parsed["id"]), (
            f"ID '{parsed['id']}' does not match TC_[FEATURE]_[NNN] pattern in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_title_within_80_chars(self, tc_file):
        """Test case title is present and ≤80 characters."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["title"] is not None, f"Title is missing in {tc_file.name}"
        assert len(parsed["title"]) <= 80, (
            f"Title '{parsed['title']}' exceeds 80 chars ({len(parsed['title'])}) in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_objective_starts_with_verify_or_ensure(self, tc_file):
        """Test case objective starts with 'Verify that...' or 'Ensure that...'."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["objective"] is not None, f"Objective is missing in {tc_file.name}"
        assert (
            parsed["objective"].startswith("Verify that")
            or parsed["objective"].startswith("Ensure that")
        ), (
            f"Objective '{parsed['objective'][:50]}...' does not start with "
            f"'Verify that...' or 'Ensure that...' in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_preconditions_is_nonempty_list(self, tc_file):
        """Test case preconditions is a non-empty list."""
        parsed = parse_test_case_full(tc_file)
        assert isinstance(parsed["preconditions"], list), (
            f"Preconditions is not a list in {tc_file.name}"
        )
        assert len(parsed["preconditions"]) >= 1, (
            f"Preconditions list is empty in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_steps_minimum_three(self, tc_file):
        """Test case has at least 3 numbered steps."""
        parsed = parse_test_case_full(tc_file)
        assert len(parsed["steps"]) >= 3, (
            f"Steps count is {len(parsed['steps'])} (minimum 3 required) in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_expected_results_one_per_step(self, tc_file):
        """Expected results count matches steps count (one per step)."""
        parsed = parse_test_case_full(tc_file)
        assert len(parsed["expected_results"]) == len(parsed["steps"]), (
            f"Expected results count ({len(parsed['expected_results'])}) != "
            f"steps count ({len(parsed['steps'])}) in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_priority_valid_value(self, tc_file):
        """Test case priority is one of {High, Normal, Low}."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["priority"] is not None, f"Priority is missing in {tc_file.name}"
        assert parsed["priority"] in VALID_PRIORITIES, (
            f"Priority '{parsed['priority']}' not in {VALID_PRIORITIES} in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_test_scope_present(self, tc_file):
        """Test case has a test scope field."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["test_scope"] is not None and parsed["test_scope"].strip() != "", (
            f"Test scope is missing or empty in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_automation_status_present(self, tc_file):
        """Test case has an automation status field."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["automation_status"] is not None and parsed["automation_status"].strip() != "", (
            f"Automation status is missing or empty in {tc_file.name}"
        )

    @pytest.mark.parametrize("tc_file", ALL_TEST_CASE_FILES, ids=lambda f: f.stem)
    def test_automation_dependency_valid(self, tc_file):
        """Test case automation dependency is one of {A, B, C, D}."""
        parsed = parse_test_case_full(tc_file)
        assert parsed["automation_dependency"] is not None, (
            f"Automation dependency is missing in {tc_file.name}"
        )
        assert parsed["automation_dependency"] in VALID_AUTOMATION_DEPENDENCIES, (
            f"Automation dependency '{parsed['automation_dependency']}' "
            f"not in {VALID_AUTOMATION_DEPENDENCIES} in {tc_file.name}"
        )

    # =========================================================================
    # Hypothesis-based property: generated test cases must parse correctly
    # =========================================================================

    @given(
        feature=st.sampled_from(["LOGIN", "CART", "CATALOG", "CHECKOUT"]),
        number=st.integers(min_value=1, max_value=999),
        title=st.text(
            min_size=5, max_size=80,
            alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z"))
        ).filter(lambda s: len(s.strip()) >= 5),
        priority=st.sampled_from(["High", "Normal", "Low"]),
        scope=st.sampled_from(["Mandatory Regression Test", "Smoke Test", "Extended Regression Test"]),
        status=st.sampled_from(["automated", "planned", "manual-only"]),
        dependency=st.sampled_from(["A", "B", "C", "D"]),
        num_steps=st.integers(min_value=3, max_value=10),
        num_preconditions=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture])
    def test_generated_test_cases_parse_correctly(
        self, feature, number, title, priority, scope, status, dependency,
        num_steps, num_preconditions, tmp_path
    ):
        """Any well-formed test case markdown parses to yield all mandatory fields.

        **Validates: Requirements 9.2, 9.4**
        """
        tc_id = f"TC_{feature}_{number:03d}"

        # Normalize title (parser strips leading/trailing whitespace)
        normalized_title = title.strip()

        # Build preconditions
        preconditions = "\n".join(
            f"- Precondition {i+1}" for i in range(num_preconditions)
        )

        # Build steps table
        steps_rows = "\n".join(
            f"| {i+1} | Action step {i+1} | Expected result {i+1} |"
            for i in range(num_steps)
        )

        # Build markdown content
        md_content = f"""# Test Case: {tc_id}

## Test Case ID
{tc_id}

## Title
{normalized_title}

## Objective
Verify that the system behaves correctly under test conditions.

## Preconditions
{preconditions}

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
{steps_rows}

## Priority
{priority}

## Test Scope
{scope}

## Automation Status
{status}

## Automation Dependency Category
{dependency}
"""

        # Write to temp file
        tc_file = tmp_path / f"{tc_id}.md"
        tc_file.write_text(md_content, encoding="utf-8")

        # Parse
        parsed = parse_test_case_full(tc_file)

        # Validate all mandatory fields
        assert parsed["id"] == tc_id
        assert parsed["title"] == normalized_title
        assert len(parsed["title"]) <= 80
        assert parsed["objective"].startswith("Verify that")
        assert len(parsed["preconditions"]) == num_preconditions
        assert len(parsed["steps"]) == num_steps
        assert len(parsed["expected_results"]) == num_steps
        assert parsed["priority"] in VALID_PRIORITIES
        assert parsed["test_scope"] is not None and parsed["test_scope"].strip() != ""
        assert parsed["automation_status"] is not None
        assert parsed["automation_dependency"] in VALID_AUTOMATION_DEPENDENCIES
