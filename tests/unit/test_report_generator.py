"""
Property-Based Tests for Report Generator — Demo_QA
=====================================================
Validates correctness properties of the HTML report generator
using Hypothesis for property-based testing.

Properties tested:
- Property 9: Report Generation Correctness

Run with:
    pytest tests/unit/test_report_generator.py -v
"""

import re
import tempfile
from datetime import datetime, timedelta

import pytest
from hypothesis import given, settings, HealthCheck, assume
from hypothesis import strategies as st

from framework.reporting.html_report import ReportGenerator, TestResult


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Valid test statuses
valid_statuses = st.sampled_from(["passed", "failed", "skipped"])

# Test names — realistic function names
test_names = st.from_regex(
    r"check_T[0-9]{1,4}_[a-z][a-z0-9_]{2,30}", fullmatch=True
)

# Durations — positive floats representing seconds
durations = st.floats(min_value=0.0, max_value=600.0, allow_nan=False, allow_infinity=False)

# Tracebacks for failed tests
tracebacks = st.text(
    min_size=10, max_size=500,
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z"), whitelist_characters="\n:./\\")
)

# Build TestResult objects
def build_test_result_strategy():
    """Strategy that generates valid TestResult objects."""
    return st.builds(
        TestResult,
        name=test_names,
        status=valid_statuses,
        duration=durations,
        traceback=st.one_of(st.none(), tracebacks),
        screenshot_path=st.none(),
        markers=st.just({}),
    ).map(_fix_traceback_for_status)


def _fix_traceback_for_status(result: TestResult) -> TestResult:
    """Ensure traceback is only set for failed tests (matches real behavior)."""
    if result.status == "failed" and result.traceback is None:
        # Failed tests should have a traceback
        return TestResult(
            name=result.name,
            status=result.status,
            duration=result.duration,
            traceback="AssertionError: Expected condition not met",
            screenshot_path=result.screenshot_path,
            markers=result.markers,
        )
    elif result.status != "failed" and result.traceback is not None:
        # Non-failed tests should not have a traceback
        return TestResult(
            name=result.name,
            status=result.status,
            duration=result.duration,
            traceback=None,
            screenshot_path=result.screenshot_path,
            markers=result.markers,
        )
    return result


# List of TestResult objects (including empty lists)
test_results_lists = st.lists(build_test_result_strategy(), min_size=0, max_size=20)


# =============================================================================
# Property 9: Report Generation Correctness
# =============================================================================
# For any list of TestResult objects (including empty lists), the ReportGenerator
# SHALL produce a valid self-contained HTML string that:
# (a) contains no external CSS/JS references,
# (b) displays aggregate counts (total, passed, failed, skipped) that exactly
#     match the input data, and
# (c) for each TestResult in the input, contains the test name, status, and
#     duration — and for failed tests, includes the traceback.

class TestReportGenerationCorrectness:
    """Property 9: Report Generation Correctness."""

    # Feature: qa-demo-training, Property 9: Report Generation Correctness

    @given(results=test_results_lists)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.too_slow])
    def test_report_is_self_contained_no_external_references(self, results):
        """
        For any list of TestResult objects, the generated HTML SHALL contain
        no external CSS or JavaScript references (no <link rel="stylesheet">,
        no <script src="...">).

        **Validates: Requirements 5.1, 5.7**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            start_time = datetime(2025, 1, 15, 10, 0, 0)
            end_time = start_time + timedelta(seconds=30.0)

            report_path = generator.generate(results, start_time, end_time)
            assert report_path is not None, "Report generation should succeed"

            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        # (a) No external CSS references
        assert '<link' not in html_content.lower() or 'rel="stylesheet"' not in html_content.lower(), (
            "Report should not contain external CSS stylesheet references"
        )
        # No external JS references (script tags with src attribute)
        script_src_pattern = re.compile(r'<script[^>]+src\s*=', re.IGNORECASE)
        assert not script_src_pattern.search(html_content), (
            "Report should not contain external JavaScript references"
        )

    @given(results=test_results_lists)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.too_slow])
    def test_report_aggregate_counts_match_input(self, results):
        """
        For any list of TestResult objects, the HTML report SHALL display
        aggregate counts (total, passed, failed, skipped) that exactly match
        the input data.

        **Validates: Requirements 5.2**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            start_time = datetime(2025, 1, 15, 10, 0, 0)
            end_time = start_time + timedelta(seconds=45.5)

            report_path = generator.generate(results, start_time, end_time)
            assert report_path is not None, "Report generation should succeed"

            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        # Calculate expected counts
        expected_total = len(results)
        expected_passed = sum(1 for r in results if r.status == "passed")
        expected_failed = sum(1 for r in results if r.status == "failed")
        expected_skipped = sum(1 for r in results if r.status == "skipped")

        # Verify aggregate counts are present in the HTML
        # The report uses summary cards with class="value" containing the count
        # Pattern: <span class="value">{count}</span>
        total_pattern = re.compile(
            r'<div class="summary-card total">\s*<span class="value">'
            + str(expected_total)
            + r'</span>'
        )
        passed_pattern = re.compile(
            r'<div class="summary-card passed">\s*<span class="value">'
            + str(expected_passed)
            + r'</span>'
        )
        failed_pattern = re.compile(
            r'<div class="summary-card failed">\s*<span class="value">'
            + str(expected_failed)
            + r'</span>'
        )
        skipped_pattern = re.compile(
            r'<div class="summary-card skipped">\s*<span class="value">'
            + str(expected_skipped)
            + r'</span>'
        )

        assert total_pattern.search(html_content), (
            f"Report should display total={expected_total}"
        )
        assert passed_pattern.search(html_content), (
            f"Report should display passed={expected_passed}"
        )
        assert failed_pattern.search(html_content), (
            f"Report should display failed={expected_failed}"
        )
        assert skipped_pattern.search(html_content), (
            f"Report should display skipped={expected_skipped}"
        )

    @given(results=st.lists(build_test_result_strategy(), min_size=1, max_size=15))
    @settings(max_examples=25, suppress_health_check=[HealthCheck.too_slow])
    def test_report_contains_each_test_name_status_duration(self, results):
        """
        For each TestResult in the input, the HTML report SHALL contain
        the test name, status, and duration.

        **Validates: Requirements 5.3**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            start_time = datetime(2025, 1, 15, 10, 0, 0)
            end_time = start_time + timedelta(seconds=60.0)

            report_path = generator.generate(results, start_time, end_time)
            assert report_path is not None, "Report generation should succeed"

            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        for result in results:
            # Test name should appear in the report
            assert result.name in html_content, (
                f"Report should contain test name '{result.name}'"
            )

            # Duration formatted to 2 decimal places should appear
            formatted_duration = f"{result.duration:.2f}s"
            assert formatted_duration in html_content, (
                f"Report should contain duration '{formatted_duration}' "
                f"for test '{result.name}'"
            )

            # Status should be reflected (via CSS class on the row)
            # The row has class matching the status: <tr class="passed">, etc.
            status_row_pattern = re.compile(
                r'<tr class="' + re.escape(result.status) + r'">'
            )
            assert status_row_pattern.search(html_content), (
                f"Report should contain a row with status class '{result.status}' "
                f"for test '{result.name}'"
            )

    @given(results=st.lists(
        st.builds(
            TestResult,
            name=test_names,
            status=st.just("failed"),
            duration=durations,
            traceback=tracebacks,
            screenshot_path=st.none(),
            markers=st.just({}),
        ),
        min_size=1,
        max_size=10,
    ))
    @settings(max_examples=25, suppress_health_check=[HealthCheck.too_slow])
    def test_report_includes_traceback_for_failed_tests(self, results):
        """
        For failed tests, the HTML report SHALL include the traceback.

        **Validates: Requirements 5.3**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            start_time = datetime(2025, 1, 15, 10, 0, 0)
            end_time = start_time + timedelta(seconds=30.0)

            report_path = generator.generate(results, start_time, end_time)
            assert report_path is not None, "Report generation should succeed"

            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        for result in results:
            assert result.traceback is not None, "Failed tests should have traceback"
            # The traceback is HTML-escaped in the report
            escaped_tb = (
                result.traceback
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            assert escaped_tb in html_content, (
                f"Report should contain escaped traceback for failed test "
                f"'{result.name}'"
            )

    @given(results=st.just([]))
    @settings(max_examples=5)
    def test_report_handles_empty_results(self, results):
        """
        For an empty list of TestResult objects, the ReportGenerator SHALL
        produce a valid HTML report indicating no tests were executed.

        **Validates: Requirements 5.7**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            start_time = datetime(2025, 1, 15, 10, 0, 0)
            end_time = start_time + timedelta(seconds=0.5)

            report_path = generator.generate(results, start_time, end_time)
            assert report_path is not None, "Report generation should succeed even with empty results"

            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        # Should be valid HTML
        assert "<!DOCTYPE html>" in html_content
        assert "</html>" in html_content

        # Should show zero counts
        total_pattern = re.compile(
            r'<div class="summary-card total">\s*<span class="value">0</span>'
        )
        assert total_pattern.search(html_content), (
            "Empty results report should show total=0"
        )

        # Should indicate no tests were executed
        assert "No tests were executed" in html_content, (
            "Empty results report should indicate no tests were executed"
        )

    @given(results=test_results_lists)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.too_slow])
    def test_report_is_valid_html_structure(self, results):
        """
        For any list of TestResult objects, the generated report SHALL be
        a valid HTML document with proper structure.

        **Validates: Requirements 5.1**
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            start_time = datetime(2025, 1, 15, 10, 0, 0)
            end_time = start_time + timedelta(seconds=10.0)

            report_path = generator.generate(results, start_time, end_time)
            assert report_path is not None, "Report generation should succeed"

            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        # Valid HTML structure
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content
        assert "</html>" in html_content
        assert "<head>" in html_content
        assert "</head>" in html_content
        assert "<body>" in html_content
        assert "</body>" in html_content

        # Contains inline CSS (self-contained)
        assert "<style>" in html_content
        assert "</style>" in html_content
