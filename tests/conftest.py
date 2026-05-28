"""
conftest.py — Demo_QA
========================
Pytest fixtures and hooks for the Demo_QA test suite.

Provides:
- driver fixture: function-scoped Appium session with teardown
- Screenshot-on-failure: captures evidence when tests fail
- ensure_logged_in: checks products screen, performs login if needed
- Report generation hook: produces HTML report after session
- Marker metadata collection: extracts marker data for reporting

Requirements: 2.8, 2.9, 8.6, 3.4
"""

import os
import time
from datetime import datetime
from typing import Optional

import pytest

from framework.core.config_loader import ConfigLoader, ConfigurationError
from framework.core.emulator_manager import EmulatorManager
from framework.pages.locators import ProductsLocators
from framework.reporting.html_report import ReportGenerator, TestResult
from framework.utils.constants import (
    REPORTS_DIR,
    TEST_USER_STANDARD,
    TEST_PASSWORD_STANDARD,
    SHORT_TIMEOUT,
)
from framework.utils.logger_factory import get_logger
from framework.utils.markers import get_test_metadata

log = get_logger(__name__)


# =============================================================================
# Session-level state
# =============================================================================

# Collect test results for report generation
_session_results: list = []
_session_start_time: Optional[datetime] = None


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="session")
def config_loader():
    """Session-scoped ConfigLoader instance.

    Loads configuration once per test session and shares it across all tests.

    Returns:
        ConfigLoader instance with validated configuration.

    Raises:
        ConfigurationError: If configuration files are missing or invalid.
    """
    loader = ConfigLoader()
    # Pre-load configs to fail fast if misconfigured
    loader.load_app_config()
    loader.load_emulator_config()
    log.info("Configuration loaded successfully")
    return loader


@pytest.fixture(scope="session")
def emulator_manager(config_loader):
    """Session-scoped EmulatorManager instance.

    Creates the manager once per session. Individual driver sessions
    are created/destroyed per test via the `driver` fixture.

    Args:
        config_loader: ConfigLoader fixture.

    Returns:
        EmulatorManager instance ready to create sessions.
    """
    manager = EmulatorManager(config_loader)
    log.info("EmulatorManager initialized")
    return manager


@pytest.fixture(scope="function")
def driver(request, emulator_manager):
    """Function-scoped Appium driver fixture.

    Creates a fresh Appium session for each test and quits it in teardown.
    On test failure, captures a screenshot before quitting the driver.

    Args:
        request: pytest request object (provides test name and outcome).
        emulator_manager: EmulatorManager fixture.

    Yields:
        Appium WebDriver instance.

    Requirements: 2.8 (function scope, teardown quits driver)
    """
    # Create a new driver session
    drv = emulator_manager.create_session()
    log.info("Driver session created for test: %s", request.node.name)

    yield drv

    # Teardown: screenshot on failure, then quit
    _capture_screenshot_on_failure(request, drv)
    emulator_manager.quit_session()
    log.info("Driver session closed for test: %s", request.node.name)


def _capture_screenshot_on_failure(request, drv):
    """Capture a screenshot if the test failed.

    Saves to reports/{test_name}_{timestamp}.png.

    Args:
        request: pytest request object.
        drv: Appium WebDriver instance.

    Requirements: 8.6 (screenshot on failure)
    """
    # Check if the test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            test_name = request.node.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{timestamp}.png"

            # Resolve reports directory relative to project root
            project_root = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            reports_path = os.path.join(project_root, REPORTS_DIR)
            os.makedirs(reports_path, exist_ok=True)

            filepath = os.path.join(reports_path, filename)
            drv.save_screenshot(filepath)
            log.info("Failure screenshot saved: %s", filepath)

            # Store screenshot path on the node for report access
            request.node.screenshot_path = filepath
        except Exception as e:
            log.warning("Failed to capture screenshot: %s", e)


@pytest.fixture(scope="function")
def ensure_logged_in(driver):
    """Ensure the app is on the Products screen (logged in).

    Checks if the Products screen key_element is visible. If not,
    performs login using standard test credentials from constants.

    Args:
        driver: Appium WebDriver fixture.

    Returns:
        The Appium driver instance (already on Products screen).

    Requirements: 2.9 (ensure_logged_in fixture)
    """
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    # Check if already on Products screen
    try:
        WebDriverWait(driver, SHORT_TIMEOUT).until(
            EC.visibility_of_element_located(ProductsLocators.PRODUCTS_TITLE)
        )
        log.info("Already on Products screen — skipping login")
    except TimeoutException:
        # Not on products screen — perform login
        log.info("Products screen not visible — performing login")
        from tests.flows.login_flow import login_flow
        login_flow(driver, TEST_USER_STANDARD, TEST_PASSWORD_STANDARD)
        log.info("Login completed via ensure_logged_in fixture")

    return driver


# =============================================================================
# Pytest Hooks
# =============================================================================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test outcome and attach it to the test node.

    Makes the test result accessible in fixture finalizers (for screenshot
    capture) and collects results for HTML report generation.

    Also extracts marker metadata and attaches it to the report.

    Requirements: 3.4 (marker metadata accessible to reporting hooks)
    """
    outcome = yield
    report = outcome.get_result()

    # Store the report phase on the node for fixture access
    setattr(item, f"rep_{report.when}", report)

    # Collect results only from the "call" phase (actual test execution)
    if report.when == "call":
        # Extract marker metadata
        metadata = get_test_metadata(item)

        # Build TestResult for report generation
        result = TestResult(
            name=item.name,
            status="passed" if report.passed else ("failed" if report.failed else "skipped"),
            duration=report.duration,
            traceback=str(report.longrepr) if report.failed else None,
            screenshot_path=getattr(item, "screenshot_path", None),
            markers=metadata,
        )
        _session_results.append(result)

    elif report.when == "setup" and report.failed:
        # Capture setup failures as well
        metadata = get_test_metadata(item)
        result = TestResult(
            name=item.name,
            status="failed",
            duration=report.duration,
            traceback=str(report.longrepr) if report.longrepr else "Setup failed",
            markers=metadata,
        )
        _session_results.append(result)


def pytest_sessionstart(session):
    """Record session start time for report generation."""
    global _session_start_time
    _session_start_time = datetime.now()
    log.info("Test session started at %s", _session_start_time.isoformat())


def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report at the end of the test session.

    Produces a self-contained HTML report with all collected test results,
    marker metadata, and failure details.

    Requirements: 5.1 (report generation after execution)
    """
    global _session_start_time

    end_time = datetime.now()
    start_time = _session_start_time or end_time

    # Only generate report if there are results or tests were collected
    if _session_results or session.testscollected > 0:
        try:
            generator = ReportGenerator()
            report_path = generator.generate(
                results=_session_results,
                start_time=start_time,
                end_time=end_time,
            )
            if report_path:
                log.info("HTML report generated: %s", report_path)
            else:
                log.warning("Report generation returned None (possible write failure)")
        except Exception as e:
            log.error("Failed to generate HTML report: %s", e)
    else:
        log.info("No test results to report")


def pytest_configure(config):
    """Register custom markers to avoid warnings."""
    config.addinivalue_line("markers", "component(name): Jira component for traceability")
    config.addinivalue_line("markers", "test_type(name): Test classification")
    config.addinivalue_line("markers", "priority(level): Test priority level")
    config.addinivalue_line("markers", "domain(name): Test domain grouping")
