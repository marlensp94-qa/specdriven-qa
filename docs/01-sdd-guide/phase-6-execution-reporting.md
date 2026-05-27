# Phase 6: Execution and Reporting

## Objectives

By the end of this phase you will:

- Run automated tests using pytest with marker-based filtering
- Generate self-contained HTML reports after each test execution
- Analyze test failures using reports, screenshots, and logs
- Understand the test execution lifecycle from session creation to report generation
- Produce coverage reports mapping automated tests to manual test cases

## Prerequisites

Before starting Phase 6, ensure you have completed:

- [ ] Phase 4 — Automation Framework Setup (all framework components implemented)
- [ ] Phase 5 — Test Automation (check scripts and flows implemented)
- [ ] Android emulator running (API 29+)
- [ ] Appium server running on configured port (default: `http://localhost:4723`)
- [ ] Swag Labs APK installed on the emulator
- [ ] Python virtual environment activated with all dependencies installed
- [ ] Configuration files populated (`config/apps.yaml`, `config/emulators.yaml`)

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Check scripts | `tests/check_scripts/` (Phase 5) | Tests to execute |
| Reusable flows | `tests/flows/` (Phase 5) | Multi-step operations used by tests |
| conftest.py | `tests/conftest.py` (Phase 4-5) | Fixtures, hooks, report generation |
| Configuration | `config/` (Phase 4) | App and emulator settings |
| Manual test cases | `test_library/` (Phase 2-3) | Coverage mapping reference |

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| HTML test reports | `reports/report_YYYYMMDD_HHMMSS.html` | Self-contained execution reports |
| Failure screenshots | `reports/{test_name}_{timestamp}.png` | Visual evidence of failures |
| Session logs | `logs/session_{timestamp}.log` | Detailed execution logs |
| Coverage report | `test_library/coverage_analysis.md` | Manual-to-automated mapping |

---

## Step-by-Step Instructions

### Step 1: Verify the Test Environment

Before running tests, confirm all prerequisites are met:

```bash
# 1. Check emulator is running
adb devices
# Expected: emulator-5554  device

# 2. Check Appium server is running
curl http://localhost:4723/status
# Expected: JSON response with "ready": true

# 3. Verify Python environment
python --version
# Expected: Python 3.8+

pip list | grep -E "appium|pytest|PyYAML"
# Expected: All packages listed with correct versions

# 4. Verify configuration loads without error
python -c "from framework.core.config_loader import ConfigLoader; ConfigLoader().load_app_config(); print('OK')"
# Expected: OK
```

If any check fails, refer to the troubleshooting section in `docs/00-overview/setup-guide.md`.

### Step 2: Run Tests with pytest

pytest provides flexible test execution through command-line options and marker filtering.

**Basic execution commands:**

```bash
# Run all tests
pytest tests/check_scripts/

# Run with verbose output
pytest tests/check_scripts/ -v

# Run a single test file
pytest tests/check_scripts/check_T001_login_valid_credentials.py

# Run a single test function
pytest tests/check_scripts/check_T001_login_valid_credentials.py::check_T001_login_valid_credentials
```

**Marker-based filtering:**

```bash
# Run only smoke tests (critical path)
pytest tests/check_scripts/ -m smoke

# Run only regression tests
pytest tests/check_scripts/ -m regression

# Run tests for a specific component
pytest tests/check_scripts/ -m "component('authentication')"

# Run critical-priority tests only
pytest tests/check_scripts/ -m "priority('critical')"

# Combine markers with boolean logic
pytest tests/check_scripts/ -m "smoke and priority('critical')"
pytest tests/check_scripts/ -m "smoke or priority('critical')"
pytest tests/check_scripts/ -m "regression and not priority('low')"
```

**Useful pytest options:**

| Option | Purpose | Example |
|--------|---------|---------|
| `-v` | Verbose output (show test names) | `pytest -v` |
| `-s` | Show print/log output | `pytest -s` |
| `--tb=short` | Shorter tracebacks | `pytest --tb=short` |
| `--tb=line` | One-line tracebacks | `pytest --tb=line` |
| `-x` | Stop on first failure | `pytest -x` |
| `--lf` | Re-run only last failures | `pytest --lf` |
| `-k` | Filter by test name pattern | `pytest -k "login"` |
| `--co` | Collect only (list tests without running) | `pytest --co` |

### Step 3: Understand the Execution Lifecycle

When pytest runs a check script, the following sequence occurs:

```
1. pytest collects test functions matching check_* pattern
2. For each test:
   a. conftest.py driver fixture creates Appium session
      → ConfigLoader reads apps.yaml + emulators.yaml
      → EmulatorManager connects to Appium server
      → Driver session created with UiAutomator2 capabilities
      → Swag Labs APK launched on emulator
   b. Test function executes
      → Page objects interact with app via driver
      → Assertions validate expected state
   c. On FAILURE:
      → Screenshot captured → reports/{test_name}_{timestamp}.png
      → Traceback recorded for report
   d. Fixture teardown
      → Driver session quit
      → Resources cleaned up
3. After all tests complete:
   → ReportGenerator produces HTML report
   → Report saved to reports/report_YYYYMMDD_HHMMSS.html
```

### Step 4: Generate HTML Reports

The `ReportGenerator` produces self-contained HTML reports automatically after each test run. The report includes:

- **Header:** Execution date (ISO 8601), total duration
- **Summary:** Total tests, passed, failed, skipped counts
- **Details:** Each test with name, status, duration, and traceback for failures
- **Self-contained:** All CSS and JavaScript inline (no external dependencies)

**Report filename pattern:** `report_YYYYMMDD_HHMMSS.html`

The report is generated by a pytest plugin hook in `conftest.py`:

```python
# In tests/conftest.py — simplified illustration
from framework.reporting.html_report import ReportGenerator

def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report after all tests complete."""
    generator = ReportGenerator(output_dir="reports")
    report_path = generator.generate(
        results=session._test_results,
        start_time=session._start_time,
        end_time=datetime.now(),
    )
    if report_path:
        print(f"\nHTML Report: {report_path}")
```

**Report structure:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Report - 2024-01-15 14:30:00</title>
    <style>
        /* All CSS inline — no external dependencies */
        .passed { color: green; }
        .failed { color: red; }
        .skipped { color: orange; }
    </style>
</head>
<body>
    <h1>Test Execution Report</h1>
    <div class="summary">
        <p>Date: 2024-01-15 14:30:00</p>
        <p>Duration: 45.23 seconds</p>
        <p>Total: 13 | Passed: 11 | Failed: 1 | Skipped: 1</p>
    </div>
    <table class="results">
        <tr><th>Test</th><th>Status</th><th>Duration</th></tr>
        <tr class="passed">
            <td>check_T001_login_valid_credentials</td>
            <td>PASSED</td>
            <td>3.45s</td>
        </tr>
        <tr class="failed">
            <td>check_T002_login_invalid_credentials</td>
            <td>FAILED</td>
            <td>5.12s</td>
        </tr>
        <!-- Failed test includes full traceback -->
    </table>
</body>
</html>
```

### Step 5: Analyze Test Failures

When a test fails, use these resources to diagnose the issue:

#### 5.1 Read the HTML Report

Open the latest report in `reports/`. For each failed test:
- Check the **traceback** — identifies the exact line and assertion that failed
- Check the **duration** — unusually long duration may indicate a timeout issue
- Look for patterns — multiple failures in the same component suggest a systemic issue

#### 5.2 Review the Screenshot

Failed tests automatically capture a screenshot at the moment of failure:

```
reports/check_T002_login_invalid_credentials_20240115_143012.png
```

The screenshot shows the actual application state when the assertion failed. Compare it to the expected state described in the test's docstring.

#### 5.3 Check the Session Log

Detailed logs are in `logs/session_{timestamp}.log`:

```
2024-01-15T14:30:00.123 INFO     emulator_manager.py:45 Creating Appium session...
2024-01-15T14:30:02.456 INFO     emulator_manager.py:52 Session created: abc-123
2024-01-15T14:30:02.789 INFO     base_page.py:34 Validating page: LoginPage
2024-01-15T14:30:03.012 INFO     base_page.py:38 Page validated: LoginPage
2024-01-15T14:30:05.345 ERROR    base_page.py:42 Element not found: ('accessibility_id', 'test-Error message')
```

The log shows the exact sequence of framework operations, making it easy to identify where the flow diverged from expectations.

#### 5.4 Common Failure Patterns

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| `PageNotLoadedError` | Page didn't load in time | Increase timeout or check navigation |
| `NoSuchElementException` | Locator changed or element not rendered | Verify locator in Locator Store |
| `TimeoutException` | Explicit wait expired | Check if element is conditionally rendered |
| `StaleElementReferenceException` | Page refreshed after element was found | Re-locate element or use fresh page object |
| `WebDriverException: session not created` | Appium/emulator not ready | Restart Appium and emulator |
| All tests fail | Environment issue | Run entry criteria checks (Step 1) |

#### 5.5 Failure Triage Decision Tree

```
Test Failed
├── Is it a timeout/element-not-found error?
│   ├── Yes → Check if locator is correct in Locator Store
│   │         Check if page navigation occurred correctly
│   │         Try increasing timeout temporarily
│   └── No → Continue
├── Is it an assertion error?
│   ├── Yes → Compare screenshot to expected state
│   │         Check if app behavior changed
│   │         Verify test data is correct
│   └── No → Continue
├── Is it a connection error?
│   ├── Yes → Verify Appium is running
│   │         Verify emulator is responsive
│   │         Check config/emulators.yaml
│   └── No → Continue
└── Is it a framework error?
    └── Yes → Check logs for stack trace
              Review recent framework changes
              Run unit tests for affected component
```

### Step 6: Run Coverage Analysis

After executing the full test suite, generate a coverage report mapping manual test cases to automated tests:

```python
from framework.utils.coverage_analyzer import CoverageAnalyzer

analyzer = CoverageAnalyzer(
    test_library_path="test_library/",
    tests_path="tests/check_scripts/"
)
report = analyzer.analyze()

print(f"Total manual test cases: {report.total_cases}")
print(f"Automated: {report.automated_count}")
print(f"Planned: {report.planned_count}")
print(f"Manual-only: {report.manual_only_count}")
print(f"Coverage: {report.coverage_percentage:.1f}%")
```

The coverage analysis document (`test_library/coverage_analysis.md`) maps each manual test case to its automation status:

| Test Case ID | Title | Check Script | Status | Gap Justification |
|-------------|-------|--------------|--------|-------------------|
| TC_LOGIN_001 | Valid login | check_T001_login_valid_credentials | Automated | — |
| TC_LOGIN_002 | Invalid password | check_T002_login_invalid_credentials | Automated | — |
| TC_CART_003 | Cart badge count | — | Planned | P2 priority, requires multi-item setup |

---

## Worked Example: Full Execution Cycle

This example demonstrates a complete execution cycle from running tests to analyzing results.

### 1. Run the Smoke Suite

```bash
$ pytest tests/check_scripts/ -m smoke -v

========================= test session starts =========================
platform darwin -- Python 3.10.0, pytest-7.4.0
collected 13 items / 10 deselected / 3 selected

tests/check_scripts/check_T001_login_valid_credentials.py::check_T001_login_valid_credentials PASSED  [ 33%]
tests/check_scripts/check_T005_add_product_to_cart.py::check_T005_add_product_to_cart PASSED           [ 66%]
tests/check_scripts/check_T010_complete_checkout.py::check_T010_complete_checkout PASSED               [100%]

========================= 3 passed in 28.45s =========================

HTML Report: reports/report_20240115_143000.html
```

All smoke tests pass — proceed to regression.

### 2. Run the Full Regression Suite

```bash
$ pytest tests/check_scripts/ -v

========================= test session starts =========================
collected 13 items

tests/check_scripts/check_T001_login_valid_credentials.py PASSED       [  7%]
tests/check_scripts/check_T002_login_invalid_credentials.py PASSED     [ 15%]
tests/check_scripts/check_T003_login_empty_fields.py PASSED            [ 23%]
tests/check_scripts/check_T004_catalog_browsing.py PASSED              [ 30%]
tests/check_scripts/check_T005_add_product_to_cart.py PASSED           [ 38%]
tests/check_scripts/check_T006_product_detail_view.py PASSED           [ 46%]
tests/check_scripts/check_T007_remove_from_cart.py PASSED              [ 53%]
tests/check_scripts/check_T008_sort_products_az.py FAILED              [ 61%]
tests/check_scripts/check_T009_sort_products_price.py PASSED           [ 69%]
tests/check_scripts/check_T010_complete_checkout.py PASSED             [ 76%]
tests/check_scripts/check_T011_checkout_cancel.py PASSED               [ 84%]
tests/check_scripts/check_T012_continue_shopping.py PASSED             [ 92%]
tests/check_scripts/check_T013_checkout_missing_info.py PASSED         [100%]

========================= 12 passed, 1 failed in 156.78s =========================

HTML Report: reports/report_20240115_143500.html
```

### 3. Analyze the Failure

One test failed: `check_T008_sort_products_az`. Let's investigate.

**From the HTML report traceback:**
```
AssertionError: Products should be sorted A-Z, but got: ['Sauce Labs Bolt T-Shirt', 'Sauce Labs Backpack', ...]
    assert sorted_names == expected_names
```

**From the screenshot:** `reports/check_T008_sort_products_az_20240115_143245.png`
- Shows the Products screen with sort dropdown set to "Name (A to Z)"
- Product list appears unsorted

**From the log:**
```
2024-01-15T14:32:40.123 INFO  products_page.py:28 Sorting products by: Name (A to Z)
2024-01-15T14:32:40.456 INFO  base_page.py:55 Tapped element: sort_dropdown
2024-01-15T14:32:41.789 INFO  products_page.py:35 Reading product names from list...
```

**Diagnosis:** The sort action was performed but the product list wasn't refreshed before reading names. The test needs a brief wait after sorting for the UI to update.

**Fix:** Add a short wait in the `sort_products` page object method or in the test after calling sort.

### 4. Review the Report

Open `reports/report_20240115_143500.html` in a browser:

- **Summary:** 13 total, 12 passed, 1 failed, 0 skipped
- **Duration:** 156.78 seconds
- **Failed test:** Full traceback visible with assertion details
- **All other tests:** Green with individual durations

---

## Deliverables Checklist

- [ ] Full test suite executed successfully (smoke tests: 100% pass rate)
- [ ] HTML report generated in `reports/` directory with correct filename pattern
- [ ] Report contains: execution date, total/passed/failed/skipped counts, duration
- [ ] Report displays individual test results with name, status, and duration
- [ ] Failed tests include full traceback in the report
- [ ] Failure screenshots captured in `reports/` with `{test_name}_{timestamp}.png` format
- [ ] Session logs generated in `logs/` directory
- [ ] Coverage analysis document updated with automation status for all test cases
- [ ] At least one failure analyzed using report + screenshot + log (documented or demonstrated)
- [ ] `reports/` directory listed in `.gitignore`

---

## Tips and Common Pitfalls

- **Run smoke tests first:** If smoke tests fail, don't waste time on regression — fix the environment or critical bugs first
- **Don't ignore flaky tests:** A test that passes sometimes and fails sometimes has a timing issue. Fix it with explicit waits, not by re-running until it passes.
- **Keep reports for comparison:** Even though reports are gitignored, keep a few locally to compare trends across runs
- **Check the emulator state:** If many tests fail unexpectedly, the emulator may have crashed or the app may be in an unexpected state
- **Use `--lf` for efficiency:** After fixing a failure, use `pytest --lf` to re-run only the previously failed tests
- **Screenshot timing matters:** The screenshot captures the state at failure time — if the app navigated away before the assertion, the screenshot may not show the relevant screen
