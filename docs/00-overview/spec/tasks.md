# Implementation Plan: QA Demo/Training (Demo_QA)

## Overview

This plan builds the Demo_QA project from the ground up in the `Demo_QA/` directory. It starts with project scaffolding and configuration, then builds the framework core, page objects, test suite, manual test library, and documentation layers. Each task builds incrementally so there is no orphaned code.

## Tasks

- [x] 1. Project scaffolding and configuration
  - [x] 1.1 Create directory structure and project files
    - Create `Demo_QA/` root with subdirectories: `docs/`, `framework/`, `tests/`, `config/`, `test_library/`, `reports/`, `logs/`
    - Create `framework/core/`, `framework/pages/`, `framework/utils/`, `framework/reporting/`, `framework/integrations/`
    - Create `tests/check_scripts/`, `tests/flows/`, `tests/unit/`, `tests/integration/`, `tests/smoke/`
    - Create `test_library/login/`, `test_library/cart/`, `test_library/catalog/`, `test_library/checkout/`
    - Create `docs/00-overview/`, `docs/01-sdd-guide/`, `docs/02-process-journal/`, `docs/03-extensibility/`, `docs/standards/`
    - Add `__init__.py` files in all Python package directories
    - Create `.gitignore` (exclude `reports/`, `logs/`, `*.pyc`, `__pycache__/`, `.env`, `*.apk`)
    - _Requirements: 1.1, 1.2, 5.5_

  - [x] 1.2 Create requirements.txt with pinned dependencies
    - Include: appium-python-client, pytest, PyYAML, hypothesis, Jinja2 (for HTML reports)
    - All versions pinned (e.g., `appium-python-client==3.1.0`, `pytest==7.4.0`, `PyYAML==6.0.1`, `hypothesis==6.92.0`)
    - _Requirements: 1.3_

  - [x] 1.3 Create YAML configuration files
    - Create `config/apps.yaml` with Swag Labs APK path, package name (`com.swaglabsmobileapp`), activity name, app version
    - Create `config/emulators.yaml` with emulator name, platform version (11.0), Appium URL (`http://localhost:4723`), port
    - Create `config/integrations.yaml` with placeholder Jira/Zephyr keys and descriptive comments
    - Create `config/README.md` explaining each parameter and valid values
    - _Requirements: 13.1, 13.2, 13.5, 6.3_

  - [x] 1.4 Create constants module and pytest configuration
    - Create `framework/utils/constants.py` with: DEFAULT_TIMEOUT, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, APP_PACKAGE, APP_ACTIVITY, TEST_USER credentials, LOG_LEVEL
    - Create `pytest.ini` with test discovery paths (`tests/`), patterns (`check_*`), registered markers (smoke, regression, android, component, test_type, priority, domain), logging format, minimum pytest version 7.0
    - _Requirements: 4.4, 4.5, 3.3, 3.5_

- [x] 2. Framework core components
  - [x] 2.1 Implement ConfigLoader
    - Create `framework/core/config_loader.py` with `ConfigLoader` class and `ConfigurationError` exception
    - Implement `load_app_config()`, `load_emulator_config()`, `load_integrations_config()`
    - Implement `get()` method with environment variable override (`DEMO_QA_<SECTION>_<KEY>`)
    - Implement `_validate_required_keys()` and `_load_yaml()` helper methods
    - Raise `ConfigurationError` for missing files, invalid YAML, missing/empty required keys
    - _Requirements: 2.6, 2.7, 13.3, 13.4, 13.6_

  - [x] 2.2 Write property tests for ConfigLoader
    - **Property 1: Configuration Round-Trip**
    - **Property 2: Configuration Error Handling**
    - **Property 3: Configuration Environment Variable Override**
    - **Validates: Requirements 2.6, 2.7, 13.3, 13.4, 13.6**

  - [x] 2.3 Implement Logger Factory
    - Create `framework/utils/logger_factory.py` with `get_logger()` function
    - ISO 8601 format with milliseconds, log level, filename, line number, message
    - Dual output: console + `logs/session_{timestamp}.log`
    - Configurable level via constants or environment variable, default INFO
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 2.4 Implement Emulator Manager
    - Create `framework/core/emulator_manager.py` with `EmulatorManager` class
    - Implement `create_session()` returning Appium WebDriver with UiAutomator2 capabilities
    - Implement `quit_session()`, `_build_capabilities()`, `_check_appium_connection()`
    - Raise `ConnectionError` if Appium unreachable within 15 seconds
    - Log INFO message about real-device support availability at session startup
    - _Requirements: 2.5, 2.6, 2.7, 2.10, 15.1, 15.5_

  - [x] 2.5 Implement BasePage abstract class
    - Create `framework/pages/base_page.py` with `BasePage` ABC and `PageNotLoadedError`
    - Implement: `tap()`, `type_text()`, `wait_for_element()`, `is_displayed()`, `scroll()`, `get_text()`, `validate_page()`
    - Implement lazy-loading element properties pattern
    - Raise `PageNotLoadedError` with page name and locator on validation timeout
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 2.6 Write property tests for BasePage
    - **Property 4: Page Load Validation Error**
    - **Property 5: Lazy-Loading Deferred Element Location**
    - **Validates: Requirements 2.3, 2.4**

- [x] 3. Checkpoint - Core framework verification
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Marker system and reporting
  - [x] 4.1 Implement Marker System
    - Create `framework/utils/markers.py` with decorator functions: `component()`, `test_type()`, `priority()`, `domain()`
    - Implement validation: `test_type` must be in {functional, smoke, negative, boundary, integration}
    - Implement validation: `priority` must be in {critical, high, medium, low}
    - Raise `ValueError` with invalid value and allowed values list
    - Implement `get_test_metadata()` to extract all marker data from pytest items
    - Create naming validator utility for `check_T{n}_{desc}` pattern
    - _Requirements: 3.1, 3.2, 3.4, 3.6, 3.7_

  - [x] 4.2 Write property tests for Marker System and Naming Validator
    - **Property 6: Test Naming Convention Validation**
    - **Property 7: Marker Validation Rejects Invalid Values**
    - **Property 8: Marker Metadata Extraction**
    - **Validates: Requirements 3.2, 3.4, 3.6, 3.7**

  - [x] 4.3 Implement Report Generator
    - Create `framework/reporting/html_report.py` with `ReportGenerator` class
    - Generate self-contained HTML with inline CSS/JS
    - Include: execution date (ISO 8601), total/passed/failed/skipped counts, duration (2 decimal places)
    - Display individual test results with name, status, duration, traceback for failures
    - Filename pattern: `report_YYYYMMDD_HHMMSS.html`
    - Handle empty results list (produce valid report with "no tests executed")
    - Log error and return None on file write failure (no exception)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7_

  - [x] 4.4 Write property tests for Report Generator
    - **Property 9: Report Generation Correctness**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.7**

- [x] 5. Page objects and locator store
  - [x] 5.1 Create Locator Store
    - Create `framework/pages/locators.py` with all Swag Labs element locators organized by screen
    - Use accessibility IDs as primary strategy (≥80% of locators)
    - Fallback to resource-id or XPath where accessibility IDs unavailable
    - Cover all 7 screens: Login, Products, ProductDetail, Cart, CheckoutInfo, CheckoutOverview, CheckoutComplete
    - _Requirements: 7.6, 7.7, 15.4_

  - [x] 5.2 Implement LoginPage and ProductsPage
    - Create `framework/pages/login_page.py` with `LoginPage` class inheriting `BasePage`
    - Implement: `login()` returning ProductsPage, `clear_credentials()`
    - Create `framework/pages/products_page.py` with `ProductsPage` class
    - Implement: `open_product()` returning ProductDetailPage, `sort_products()`, `open_cart()` returning CartPage
    - Define `key_element` for each, use locators from Locator Store, minimum 3 locator properties per page
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 5.3 Implement remaining page objects
    - Create `framework/pages/product_detail_page.py`: `add_to_cart()`, `remove_from_cart()`, `go_back()` → ProductsPage
    - Create `framework/pages/cart_page.py`: `remove_item()`, `proceed_to_checkout()` → CheckoutInfoPage, `continue_shopping()` → ProductsPage
    - Create `framework/pages/checkout_info_page.py`: `fill_checkout_info()`, `cancel()` → CartPage
    - Create `framework/pages/checkout_overview_page.py`: `finish_checkout()` → CheckoutCompletePage, `cancel()` → ProductsPage
    - Create `framework/pages/checkout_complete_page.py`: `back_to_products()` → ProductsPage
    - All inherit BasePage, define key_element, use Locator Store, return destination page objects
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.7_

- [x] 6. Test flows and conftest
  - [x] 6.1 Implement reusable test flows
    - Create `tests/flows/login_flow.py` with `login_flow(driver, username, password)` → ProductsPage
    - Create `tests/flows/cart_flow.py` with `add_product_to_cart_flow(driver, product_name)` → CartPage
    - Create `tests/flows/checkout_flow.py` with `complete_checkout_flow(driver, first, last, zip)` → CheckoutCompletePage
    - Validate all string params: raise ValueError for None, empty, or whitespace-only
    - Raise PageNotLoadedError on failed page transitions
    - Add `__init__.py` with flow imports
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

  - [x] 6.2 Write property tests for flow parameter validation
    - **Property 10: Flow Parameter Validation**
    - **Validates: Requirements 14.3**

  - [x] 6.3 Implement conftest.py with fixtures
    - Create `tests/conftest.py` with driver fixture (function scope, teardown quits driver)
    - Implement screenshot-on-failure in fixture finalizer (saves to `reports/{test_name}_{timestamp}.png`)
    - Implement `ensure_logged_in` fixture checking products screen, performing login if needed
    - Wire ConfigLoader and EmulatorManager into fixtures
    - Implement pytest hooks for report generation and marker metadata collection
    - _Requirements: 2.8, 2.9, 8.6, 3.4_

- [x] 7. Checkpoint - Framework and page objects complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Automated test suite
  - [x] 8.1 Implement smoke tests (check scripts)
    - Create `tests/check_scripts/check_T001_login_valid_credentials.py` — login with standard_user
    - Create `tests/check_scripts/check_T005_add_product_to_cart.py` — add item and verify cart badge
    - Create `tests/check_scripts/check_T010_complete_checkout.py` — full checkout flow
    - Mark all with `@pytest.mark.smoke`, `@component`, `@priority("critical")`
    - Each uses page objects only, includes docstring with preconditions/steps/expected results, has explicit assertions
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7_

  - [x] 8.2 Implement regression tests (check scripts)
    - Create `tests/check_scripts/check_T002_login_invalid_credentials.py` — locked_out_user
    - Create `tests/check_scripts/check_T003_login_empty_fields.py` — empty username/password
    - Create `tests/check_scripts/check_T004_catalog_browsing.py` — verify product list loads
    - Create `tests/check_scripts/check_T006_product_detail_view.py` — open product, verify details
    - Create `tests/check_scripts/check_T007_remove_from_cart.py` — add then remove item
    - Create `tests/check_scripts/check_T008_sort_products_az.py` — sort A-Z and verify order
    - Create `tests/check_scripts/check_T009_sort_products_price.py` — sort by price low-high
    - Create `tests/check_scripts/check_T011_checkout_cancel.py` — start checkout then cancel
    - Create `tests/check_scripts/check_T012_continue_shopping.py` — from cart back to products
    - Create `tests/check_scripts/check_T013_checkout_missing_info.py` — submit with empty fields
    - Mark all with `@pytest.mark.regression`, appropriate `@component`, `@priority`
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7_

- [x] 9. Integration placeholders
  - [x] 9.1 Implement Jira and Zephyr placeholder modules
    - Create `framework/integrations/jira_connector.py` with `JiraConnector` class
    - Implement placeholder methods: `test_connection()`, `search_issues()`, `create_issue()`, `update_issue()`
    - Create `framework/integrations/zephyr_reporter.py` with `ZephyrReporter` class
    - Implement placeholder methods: `get_test_case()`, `search_test_cases()`, `report_execution()`
    - All methods log intended behavior, include full docstrings with purpose, params, return type, required credentials
    - Add `__init__.py` for integrations package
    - _Requirements: 6.1, 6.2, 6.4_

- [x] 10. Manual test case library
  - [x] 10.1 Create test case template and login test cases
    - Create `test_library/template.md` with all mandatory fields and placeholder text
    - Create 5+ login test cases in `test_library/login/` (TC_LOGIN_001 through TC_LOGIN_005)
    - Cover: valid login, invalid password, locked user, empty fields, logout
    - Each follows structured format: ID, title (≤80 chars), objective ("Verify that..."), preconditions, steps (≥3), expected results, priority, scope, automation status, dependency category
    - At least 2 High priority per group
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.6, 10.5_

  - [x] 10.2 Create catalog and cart test cases
    - Create 5+ catalog test cases in `test_library/catalog/` (TC_CATALOG_001 through TC_CATALOG_005)
    - Create 5+ cart test cases in `test_library/cart/` (TC_CART_001 through TC_CART_005)
    - Cover: product listing, sorting, filtering, product details, add to cart, remove from cart, cart badge, multiple items
    - Follow same structured format, assign automation dependency (A, B, C, D)
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

  - [x] 10.3 Create checkout test cases and coverage analysis
    - Create 5+ checkout test cases in `test_library/checkout/` (TC_CHECKOUT_001 through TC_CHECKOUT_005)
    - Cover: complete checkout, missing info, cancel, verify totals, order confirmation
    - Create `test_library/coverage_analysis.md` mapping each TC ID to check script name, automation status, gap justification
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 11. Checkpoint - Test library and automation complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Coverage analyzer
  - [x] 12.1 Implement Coverage Analyzer
    - Create `framework/utils/coverage_analyzer.py` with `CoverageAnalyzer` class
    - Implement `analyze()` returning coverage report with mappings, gaps, statistics
    - Implement `_parse_test_cases()` to parse markdown test case files
    - Implement `_discover_check_scripts()` to find `check_T{id}_*` functions
    - Implement `_match_cases_to_scripts()` for ID-based matching
    - _Requirements: 16.1, 16.2_

  - [x] 12.2 Write property tests for Coverage Analyzer
    - **Property 12: Coverage Mapping Correctness**
    - **Validates: Requirements 16.1**

  - [x] 12.3 Write property tests for Test Case Parser
    - **Property 11: Test Case Structure Validation**
    - **Validates: Requirements 9.2, 9.4**

- [x] 13. Quality standards documentation
  - [x] 13.1 Create quality checklist and field requirements
    - Create `docs/standards/quality-checklist.md` with validation criteria per field (title, objective, preconditions, steps, expected results)
    - Define severity levels: Critical (blocks Valid), Warning (fix before Valid), Minor (advisory)
    - Create `docs/standards/field-requirements.md` with mandatory fields, formatting rules, 1 good + 1 bad example per field
    - Define status workflow: Draft → Ready for Review → Valid → Deprecated with transition criteria
    - Include common quality violations with corrected versions for each field
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 14. SDD training guide
  - [x] 14.1 Create SDD Guide Phase 0-3 documents
    - Create `docs/01-sdd-guide/00-table-of-contents.md` listing all phases with document locations
    - Create `docs/01-sdd-guide/phase-0-app-analysis.md` — Swag Labs worked example (3+ features, 5+ screens, 2+ flows, scope criteria)
    - Create `docs/01-sdd-guide/phase-1-test-planning.md` — test plan (scope, approach, entry/exit criteria, risk assessment)
    - Create `docs/01-sdd-guide/phase-2-test-case-design.md` — methodology, decision matrix (automation vs manual, 3+ factors)
    - Create `docs/01-sdd-guide/phase-3-test-library-management.md` — organization, quality standards, review workflow
    - Each includes: objectives, inputs, outputs, step-by-step instructions, worked example, deliverables checklist, prerequisites
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.8_

  - [x] 14.2 Create SDD Guide Phase 4-7 documents
    - Create `docs/01-sdd-guide/phase-4-automation-framework.md` — framework setup, POM pattern, config management
    - Create `docs/01-sdd-guide/phase-5-test-automation.md` — writing check scripts, flows, markers
    - Create `docs/01-sdd-guide/phase-6-execution-reporting.md` — running tests, HTML reports, failure analysis
    - Create `docs/01-sdd-guide/phase-7-maintenance-cicd.md` — maintenance patterns, CI/CD integration concepts
    - Each includes: objectives, inputs, outputs, step-by-step instructions, worked example, deliverables checklist, prerequisites
    - _Requirements: 11.1, 11.2, 11.3, 11.7, 11.8_

- [x] 15. Process journal and extensibility docs
  - [x] 15.1 Create Process Journal
    - Create `docs/02-process-journal/process-journal.md`
    - Document 2+ example prompts per SDD phase (goal, context, outcome)
    - Include decision log with 4+ entries (Android over iOS, emulator over real device, pytest over unittest, POM over screenplay)
    - Include 3+ Q&A iterative refinement examples (initial version, feedback, revised version)
    - Organize chronologically by SDD phases (Phase 0-7)
    - Include 3+ lessons learned and 3+ pitfalls (situation, impact, recommendation)
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

  - [x] 15.2 Create extensibility documentation
    - Create `docs/03-extensibility/real-devices.md` — USB debugging, UDID discovery, capabilities changes, step-by-step example
    - Create `docs/03-extensibility/ios-support.md` — Xcode setup, WebDriverAgent, iOS capabilities, step-by-step example
    - _Requirements: 15.2, 15.3_

  - [x] 15.3 Create Jira/Zephyr integration documentation
    - Create `docs/03-extensibility/jira-zephyr-integration.md`
    - Document integration flow: test execution → result reporting sequence
    - Explain authentication mechanism
    - Include text-based data flow diagram (Mini_Framework → Jira → Zephyr Scale)
    - _Requirements: 6.5_

- [x] 16. Setup guide and README
  - [x] 16.1 Create setup guide and overview documentation
    - Create `docs/00-overview/setup-guide.md` covering: Python 3.8+, Android Studio, Android SDK, Appium 2.x, UiAutomator2 driver
    - Include emulator creation steps (API 29+, device profile, Google APIs system image)
    - Include APK download instructions (Sauce Labs GitHub, expected filename, target directory)
    - Include troubleshooting: tool not in PATH, version mismatch, Appium-emulator connection failure
    - Include verification procedure (run single smoke test, expected output for success/failure)
    - Specify supported OS (macOS, Windows, Linux)
    - _Requirements: 1.4, 1.5, 1.6, 1.7, 1.8, 11.7_

  - [x] 16.2 Create project README.md
    - Create `Demo_QA/README.md` with: project overview, directory structure, prerequisites with versions, setup instructions (≤10 steps from clone to running a test)
    - _Requirements: 1.1_

- [x] 17. Automation planning documents
  - [x] 17.1 Create automation plan and coverage gap analysis
    - Create `docs/00-overview/automation-plan.md` with priority tiers (P1, P2, P3)
    - Score each test case on: execution frequency, risk level, automation feasibility
    - Include 1 worked example per tier (P1, P2, P3)
    - Create coverage gap analysis identifying unautomated test cases with dependency category and technical constraint
    - Document decision criteria (flowchart/rule set) for automate vs. keep manual
    - Categorize test cases by automation dependency (A, B, C, D) with counts
    - _Requirements: 16.2, 16.3, 16.4, 16.5, 16.6_

- [x] 18. Final checkpoint - All artifacts complete
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Integration tests (against real Appium/emulator) are excluded from automated CI — run manually
- All code is Python 3.8+ targeting the Swag Labs Mobile APK on Android emulators
- The project is self-contained in the `Demo_QA/` directory at workspace root

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3", "1.4"] },
    { "id": 2, "tasks": ["2.1", "2.3"] },
    { "id": 3, "tasks": ["2.2", "2.4", "2.5"] },
    { "id": 4, "tasks": ["2.6", "4.1"] },
    { "id": 5, "tasks": ["4.2", "4.3", "5.1"] },
    { "id": 6, "tasks": ["4.4", "5.2", "5.3"] },
    { "id": 7, "tasks": ["6.1", "6.3"] },
    { "id": 8, "tasks": ["6.2", "8.1", "8.2"] },
    { "id": 9, "tasks": ["9.1", "10.1", "10.2", "10.3"] },
    { "id": 10, "tasks": ["12.1", "13.1"] },
    { "id": 11, "tasks": ["12.2", "12.3", "14.1", "14.2"] },
    { "id": 12, "tasks": ["15.1", "15.2", "15.3"] },
    { "id": 13, "tasks": ["16.1", "16.2", "17.1"] }
  ]
}
```
