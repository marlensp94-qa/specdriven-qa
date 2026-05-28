"""
HTML Report Generator — Demo_QA
==================================
Generates self-contained HTML test reports after execution.
Reports include no external CSS/JS dependencies and can be shared as standalone files.

Usage:
    from framework.reporting.html_report import ReportGenerator, TestResult

    generator = ReportGenerator()
    results = [
        TestResult(name="check_T001_login_valid", status="passed", duration=3.45),
        TestResult(name="check_T002_login_invalid", status="failed", duration=2.10,
                   traceback="AssertionError: Expected home screen"),
    ]
    report_path = generator.generate(results, start_time, end_time)
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from framework.utils.constants import REPORTS_DIR
from framework.utils.logger_factory import get_logger

log = get_logger(__name__)


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class TestResult:
    """Represents the result of a single test execution.

    Attributes:
        name: Test function name (e.g., "check_T001_login_valid_credentials").
        status: Execution status — "passed", "failed", or "skipped".
        duration: Execution time in seconds.
        traceback: Full Python traceback for failed tests. None for passed/skipped.
        screenshot_path: Path to failure screenshot. None if not captured.
        markers: Dictionary of marker metadata (component, priority, etc.).
    """
    name: str
    status: str  # "passed", "failed", "skipped"
    duration: float
    traceback: Optional[str] = None
    screenshot_path: Optional[str] = None
    markers: Optional[dict] = field(default_factory=dict)


# =============================================================================
# Report Generator
# =============================================================================

class ReportGenerator:
    """Generates self-contained HTML test reports after execution.

    Reports are saved to the reports/ directory with timestamped filenames
    to prevent overwriting. The HTML is fully self-contained with inline CSS.

    Args:
        output_dir: Directory for report output relative to project root.
                    Created automatically if it doesn't exist.
    """

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            # Resolve relative to project root
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            self._output_dir = os.path.join(project_root, REPORTS_DIR)
        else:
            self._output_dir = output_dir

    def generate(
        self,
        results: List[TestResult],
        start_time: datetime,
        end_time: datetime,
    ) -> Optional[str]:
        """Generate HTML report from test results.

        Creates the reports/ directory if needed, builds the HTML content,
        and writes it to a timestamped file.

        Args:
            results: List of TestResult objects (can be empty).
            start_time: Execution start timestamp.
            end_time: Execution end timestamp.

        Returns:
            Absolute path to the generated report file, or None on write failure.

        Note:
            On file system errors, logs the error and returns None without
            raising an exception (does not interrupt test session exit).
        """
        # Calculate metadata
        total = len(results)
        passed = sum(1 for r in results if r.status == "passed")
        failed = sum(1 for r in results if r.status == "failed")
        skipped = sum(1 for r in results if r.status == "skipped")
        duration = (end_time - start_time).total_seconds()

        metadata = {
            "execution_date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": f"{duration:.2f}",
            "pass_rate": f"{(passed / total * 100):.1f}" if total > 0 else "0.0",
        }

        # Build HTML
        html_content = self._build_html(results, metadata)

        # Write to file
        try:
            os.makedirs(self._output_dir, exist_ok=True)
            timestamp = start_time.strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.html"
            filepath = os.path.join(self._output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            log.info("Report generated: %s", filepath)
            return filepath

        except (IOError, OSError) as e:
            log.error(
                "Failed to write HTML report to '%s': %s",
                self._output_dir,
                e,
            )
            return None

    def _build_html(self, results: List[TestResult], metadata: dict) -> str:
        """Build complete self-contained HTML string with inline CSS.

        Args:
            results: List of TestResult objects.
            metadata: Aggregated execution metadata dictionary.

        Returns:
            Complete HTML document as a string.
        """
        # Build individual test rows
        test_rows = ""
        for r in results:
            status_class = r.status
            status_icon = {"passed": "✅", "failed": "❌", "skipped": "⏭️"}.get(r.status, "❓")

            traceback_html = ""
            if r.traceback:
                escaped_tb = (
                    r.traceback
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                traceback_html = f'<pre class="traceback">{escaped_tb}</pre>'

            screenshot_html = ""
            if r.screenshot_path:
                screenshot_html = f'<p class="screenshot">📸 Screenshot: <code>{r.screenshot_path}</code></p>'

            markers_html = ""
            if r.markers:
                marker_parts = [
                    f'<span class="marker">{k}: {v}</span>'
                    for k, v in r.markers.items() if v
                ]
                if marker_parts:
                    markers_html = f'<div class="markers">{" ".join(marker_parts)}</div>'

            test_rows += f"""
            <tr class="{status_class}">
                <td class="status">{status_icon}</td>
                <td class="name">{r.name}</td>
                <td class="duration">{r.duration:.2f}s</td>
                <td class="details">
                    {traceback_html}
                    {screenshot_html}
                    {markers_html}
                </td>
            </tr>"""

        # Handle empty results
        if not results:
            test_rows = """
            <tr>
                <td colspan="4" class="empty">No tests were executed.</td>
            </tr>"""

        # Build full HTML document
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo_QA Test Report — {metadata['execution_date']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            padding: 2rem;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            color: #1a1a2e;
            margin-bottom: 0.5rem;
            font-size: 1.8rem;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 2rem;
            font-size: 0.95rem;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .summary-card {{
            background: white;
            border-radius: 8px;
            padding: 1.2rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card .value {{
            font-size: 2rem;
            font-weight: bold;
            display: block;
        }}
        .summary-card .label {{
            font-size: 0.85rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .summary-card.passed .value {{ color: #27ae60; }}
        .summary-card.failed .value {{ color: #e74c3c; }}
        .summary-card.skipped .value {{ color: #f39c12; }}
        .summary-card.total .value {{ color: #2c3e50; }}
        .summary-card.duration .value {{ color: #3498db; font-size: 1.5rem; }}
        .summary-card.rate .value {{ color: #8e44ad; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background: #1a1a2e;
            color: white;
            padding: 0.8rem 1rem;
            text-align: left;
            font-weight: 500;
        }}
        td {{
            padding: 0.7rem 1rem;
            border-bottom: 1px solid #eee;
            vertical-align: top;
        }}
        tr:last-child td {{ border-bottom: none; }}
        tr.passed {{ background: #f0fff4; }}
        tr.failed {{ background: #fff5f5; }}
        tr.skipped {{ background: #fffbf0; }}
        .status {{ width: 40px; text-align: center; font-size: 1.2rem; }}
        .name {{ font-family: 'SF Mono', Monaco, monospace; font-size: 0.9rem; }}
        .duration {{ width: 80px; text-align: right; color: #666; }}
        .details {{ font-size: 0.85rem; }}
        .traceback {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 0.8rem;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.8rem;
            margin-top: 0.5rem;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        .screenshot {{ color: #666; margin-top: 0.3rem; }}
        .screenshot code {{ background: #eee; padding: 0.2rem 0.4rem; border-radius: 3px; }}
        .markers {{ margin-top: 0.3rem; }}
        .marker {{
            display: inline-block;
            background: #e8f4fd;
            color: #2980b9;
            padding: 0.15rem 0.5rem;
            border-radius: 3px;
            font-size: 0.75rem;
            margin-right: 0.3rem;
        }}
        .empty {{
            text-align: center;
            color: #999;
            padding: 2rem;
            font-style: italic;
        }}
        .footer {{
            margin-top: 2rem;
            text-align: center;
            color: #999;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Demo_QA Test Report</h1>
        <p class="subtitle">Execution: {metadata['execution_date']} | Duration: {metadata['duration']}s</p>

        <div class="summary">
            <div class="summary-card total">
                <span class="value">{metadata['total']}</span>
                <span class="label">Total Tests</span>
            </div>
            <div class="summary-card passed">
                <span class="value">{metadata['passed']}</span>
                <span class="label">Passed</span>
            </div>
            <div class="summary-card failed">
                <span class="value">{metadata['failed']}</span>
                <span class="label">Failed</span>
            </div>
            <div class="summary-card skipped">
                <span class="value">{metadata['skipped']}</span>
                <span class="label">Skipped</span>
            </div>
            <div class="summary-card duration">
                <span class="value">{metadata['duration']}s</span>
                <span class="label">Duration</span>
            </div>
            <div class="summary-card rate">
                <span class="value">{metadata['pass_rate']}%</span>
                <span class="label">Pass Rate</span>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Test Name</th>
                    <th>Duration</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {test_rows}
            </tbody>
        </table>

        <p class="footer">
            Generated by Demo_QA Report Generator | Swag Labs Mobile — Android Emulator
        </p>
    </div>
</body>
</html>"""

        return html

    def _format_duration(self, seconds: float) -> str:
        """Format duration to 2 decimal places.

        Args:
            seconds: Duration in seconds.

        Returns:
            Formatted string (e.g., "3.45").
        """
        return f"{seconds:.2f}"
