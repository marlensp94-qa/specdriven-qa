# Requirements Document

## Introduction

The QA Demo/Training project ("Demo_QA") is a comprehensive showroom and onboarding tool for new QA team members. It demonstrates the complete Spec-Driven Development (SDD) process applied to QA, from receiving a new application to having a full test library, automation framework, and reporting system. The project uses Swag Labs Mobile (Sauce Labs public demo APK) as the target application, running on Android emulators via Android Studio. All documentation and code are in English. The project serves a hybrid audience: primarily experienced QAs, but with complete documentation enabling juniors and interns to follow along.

## Glossary

- **Demo_QA**: The root project directory containing all documentation, framework code, tests, and configuration
- **Mini_Framework**: A simplified mobile test automation framework based on the Leroy architecture (Python + Appium + pytest), adapted for single-project, emulator-only execution
- **Test_Library**: A structured collection of manual test cases for Swag Labs, organized by feature group with quality standards
- **Process_Journal**: Documentation of the SDD workflow including example prompts, decisions, and the full QA lifecycle
- **SDD_Guide**: The Spec-Driven Development training guide documenting all phases from app analysis through maintenance
- **Swag_Labs**: Sauce Labs' public demo e-commerce mobile application (Android APK from GitHub) used as the target app
- **Page_Object**: A design pattern class representing a screen in the application, encapsulating element locators and interaction methods
- **BasePage**: The abstract base class providing common page interaction methods (tap, type, wait, validate) inherited by all page objects
- **Check_Script**: An automated test file following the naming convention `check_T{number}_{description}.py`
- **Locator_Store**: A centralized collection of element locators (accessibility IDs, XPaths, resource IDs) for Swag Labs screens
- **Report_Generator**: The HTML report generation component that produces test execution summaries
- **Coverage_Analyzer**: The component that maps manual test cases to automated tests and identifies gaps
- **Emulator_Manager**: The simplified driver management component handling Android emulator sessions via Appium
- **Marker_System**: The pytest marker infrastructure for classifying tests (smoke, regression, component, priority, domain)

## Requirements

### Requirement 1: Project Structure and Setup

**User Story:** As a new QA team member, I want a well-organized project with clear setup instructions, so that I can get the environment running and understand the project layout without external help.

#### Acceptance Criteria

1. THE Demo_QA SHALL provide a README.md at the project root containing a project overview, directory structure description, prerequisites list with version numbers, and setup instructions that guide the user from clone to executing a sample test in 10 steps or fewer
2. THE Demo_QA SHALL organize content into the following top-level directories: docs, framework, tests, config, test_library, and reports
3. WHEN a user clones the project, THE Demo_QA SHALL include a requirements.txt file listing all Python dependencies with pinned versions (e.g., package==x.y.z format)
4. THE Demo_QA SHALL include a setup guide in docs/00-overview/ covering installation of Python 3.8+, Android Studio, Android SDK, Appium 2.x, and UiAutomator2 driver, specifying supported host operating systems (macOS, Windows, or Linux)
5. THE Demo_QA SHALL include step-by-step instructions for creating and configuring an Android emulator in Android Studio, specifying the target Android API level (minimum API 29), device profile, and system image type (Google APIs)
6. THE Demo_QA SHALL include instructions for downloading the Swag Labs APK from the official Sauce Labs GitHub repository, including the expected filename and target directory within the project
7. IF a required tool is not installed or misconfigured, THEN THE Demo_QA SHALL provide troubleshooting steps for each prerequisite in the setup guide, covering at minimum: tool not found in PATH, version mismatch, and connection failure between Appium and the emulator
8. WHEN a user completes all setup steps, THE Demo_QA SHALL include a verification procedure that runs a single smoke test to confirm the environment is correctly configured, with expected output described for both success and failure scenarios

### Requirement 2: Mini Automation Framework Core

**User Story:** As a QA engineer, I want a simplified but functional automation framework based on the Leroy architecture, so that I can learn the Page Object Model pattern and framework design without the complexity of multi-project, multi-device setups.

#### Acceptance Criteria

1. THE Mini_Framework SHALL implement a BasePage class providing common methods: tap, type_text, wait_for_element, is_displayed, scroll, and get_text, where each method accepts an element locator tuple (strategy, value) as its primary parameter
2. THE BasePage SHALL validate page instantiation by checking a key_element attribute defined in each child page object
3. WHEN a page object is instantiated and the key_element is not found within a configurable timeout (default: 10 seconds), THE BasePage SHALL raise a PageNotLoadedError with a message containing the page class name and the key_element locator that was not found
4. THE Mini_Framework SHALL implement lazy-loading element properties that locate elements only when first accessed
5. THE Emulator_Manager SHALL create an Appium driver session configured for Android with UiAutomator2 automation name
6. THE Emulator_Manager SHALL read device configuration from a YAML file located at config/emulators.yaml
7. IF the config/emulators.yaml file is missing or contains invalid YAML syntax, THEN THE Emulator_Manager SHALL raise a ConfigurationError with the file path and a description of the issue
8. THE Mini_Framework SHALL provide a conftest.py with pytest fixtures for driver session management, where the driver fixture uses function scope (one session per test) and performs driver quit in teardown
9. THE Mini_Framework SHALL provide an ensure_logged_in fixture that checks for the presence of the products screen key_element and, if not found, performs the login flow using credentials from the constants module before proceeding
10. IF the Appium server is not reachable within 15 seconds, THEN THE Emulator_Manager SHALL raise a ConnectionError with the server URL and a suggestion to verify Appium is running

### Requirement 3: Test Organization and Markers

**User Story:** As a QA engineer, I want tests organized with markers and naming conventions, so that I can run specific subsets (smoke, regression) and trace tests back to test cases.

#### Acceptance Criteria

1. THE Marker_System SHALL support the following pytest markers: smoke (no arguments), regression (no arguments), android (no arguments), component (single string argument), test_type (single string argument), priority (single string argument), and domain (single string argument)
2. THE Mini_Framework SHALL enforce the test naming convention `check_T{number}_{description}` for all test functions via documentation and examples, where {number} is a positive integer matching a test case ID from the Test_Library and {description} contains only lowercase letters, digits, and underscores with a maximum length of 60 characters
3. THE Mini_Framework SHALL configure pytest to discover test files matching the pattern `check_*.py` and test functions matching `check_*`
4. WHEN a test is executed, THE Marker_System SHALL make marker metadata (component, test_type, priority, domain) accessible to reporting hooks as key-value attributes on the test item node
5. THE Mini_Framework SHALL provide a pytest.ini file configuring test discovery paths, registered marker definitions, logging format (timestamp, level, message), and a minimum pytest version of 7.0 or higher
6. IF a test is decorated with a test_type marker whose value is not one of "functional", "smoke", "negative", "boundary", or "integration", THEN THE Marker_System SHALL raise a ValueError at collection time indicating the invalid value and the list of allowed values
7. IF a test is decorated with a priority marker whose value is not one of "critical", "high", "medium", or "low", THEN THE Marker_System SHALL raise a ValueError at collection time indicating the invalid value and the list of allowed values
8. EACH automated test SHALL be decorated with at minimum the component and priority markers; smoke or regression markers are optional but at least one scope marker (smoke or regression) SHALL be present per test

### Requirement 4: Logging and Constants

**User Story:** As a QA engineer, I want structured logging and centralized constants, so that I can debug test failures efficiently and avoid magic numbers in test code.

#### Acceptance Criteria

1. THE Mini_Framework SHALL provide a logger factory that creates named loggers with a fixed format containing, in order: ISO 8601 timestamp with milliseconds, log level, source filename, line number, and message text
2. THE Mini_Framework SHALL configure logging to output to both console and a log file in the `logs/` directory, where each log file is named with the session start timestamp to prevent overwriting previous logs
3. THE Mini_Framework SHALL support configuring the log level (DEBUG, INFO, WARNING, ERROR) via the constants module or environment variable, defaulting to INFO
4. THE Mini_Framework SHALL provide a constants module containing at minimum: default explicit wait timeout in seconds, implicit wait timeout in seconds, page load timeout in seconds, base application URL, test user credentials, and application package identifiers
5. THE Mini_Framework SHALL use no magic numbers or hardcoded strings in test code; all numeric values other than 0 and 1 used as indices, and all application-specific strings, SHALL be referenced from the constants module or configuration files

### Requirement 5: HTML Reporting

**User Story:** As a QA engineer, I want HTML test reports generated after each execution, so that I can review results visually and share them with stakeholders.

#### Acceptance Criteria

1. WHEN a test suite execution completes, THE Report_Generator SHALL create the reports/ directory if it does not exist and produce a self-contained HTML report (no external CSS or JavaScript dependencies) in that directory
2. THE Report_Generator SHALL include in each report: execution date in ISO 8601 format (YYYY-MM-DD HH:MM:SS), total tests, passed count, failed count, skipped count, and execution duration displayed in seconds with two decimal places of precision
3. THE Report_Generator SHALL display individual test results with test name, status (passed, failed, skipped), duration in seconds, and for failed tests the full Python traceback captured during execution
4. THE Report_Generator SHALL generate reports with a unique filename following the pattern `report_YYYYMMDD_HHMMSS.html` using the execution start timestamp to prevent overwriting previous reports
5. THE Demo_QA SHALL include the reports/ directory in .gitignore to prevent committing generated reports
6. IF the Report_Generator fails to write the HTML report due to a file system error, THEN THE Report_Generator SHALL log an error message indicating the failure reason and the intended file path without interrupting the test session exit
7. WHEN a test suite execution completes with zero tests collected, THE Report_Generator SHALL still produce a valid HTML report indicating that no tests were executed

### Requirement 6: Jira and Zephyr Integration (Prepared)

**User Story:** As a QA engineer, I want to see how Jira/Zephyr integration is structured in the framework, so that I can understand the pattern and enable it when I have access to a Jira instance.

#### Acceptance Criteria

1. THE Mini_Framework SHALL include a jira_connector module with placeholder functions for: testing the connection, searching issues by JQL, creating an issue, and updating an issue — with all function bodies commented out and replaced by placeholder logging that describes what the real implementation would do
2. THE Mini_Framework SHALL include a zephyr_reporter module with placeholder functions for: retrieving a test case by key, searching test cases by project, and reporting a test execution result — with all function bodies commented out and replaced by placeholder logging that describes what the real implementation would do
3. THE Mini_Framework SHALL include a config/integrations.yaml file containing placeholder keys for: Jira base URL, project key, API token, and Zephyr Scale test cycle key, each with a descriptive comment indicating the expected value format
4. EACH placeholder function in the jira_connector and zephyr_reporter modules SHALL include a docstring specifying: the function's purpose, required parameters with types, expected return value, and which credential from config/integrations.yaml is needed to enable it
5. THE Mini_Framework SHALL include a docs section explaining the Jira/Zephyr integration flow, including: the sequence of operations from test execution to result reporting, the authentication mechanism, and a text-based diagram showing data flow between the Mini_Framework, Jira, and Zephyr Scale

### Requirement 7: Page Objects for Swag Labs

**User Story:** As a QA engineer, I want complete page objects for all Swag Labs screens, so that I can see the POM pattern applied to a real application and write tests against it.

#### Acceptance Criteria

1. THE Mini_Framework SHALL provide page objects inheriting from BasePage for the following Swag Labs screens: LoginPage, ProductsPage, ProductDetailPage, CartPage, CheckoutInfoPage, CheckoutOverviewPage, and CheckoutCompletePage
2. EACH page object SHALL define a key_element attribute used for page load validation
3. EACH page object SHALL encapsulate all element locators as class-level properties using the lazy-loading pattern, with a minimum of 3 locator properties per page object
4. EACH page object SHALL provide action methods representing user interactions specific to that screen: LoginPage (login, clear_credentials), ProductsPage (open_product, sort_products, open_cart), ProductDetailPage (add_to_cart, remove_from_cart, go_back), CartPage (remove_item, proceed_to_checkout, continue_shopping), CheckoutInfoPage (fill_checkout_info, cancel), CheckoutOverviewPage (finish_checkout, cancel), CheckoutCompletePage (back_to_products)
5. WHEN an action method triggers navigation to a different screen, THE page object SHALL return the corresponding destination page object instance to enable method chaining
6. THE Mini_Framework SHALL provide a Locator_Store with all element locators for Swag Labs organized by screen, using accessibility IDs as the primary locator strategy and resource IDs or XPath as the fallback when accessibility IDs are not available on an element
7. EACH page object SHALL reference locators from the Locator_Store rather than defining locator values inline within the page object class

### Requirement 8: Automated Test Suite for Swag Labs

**User Story:** As a QA engineer, I want a complete set of automated tests covering Swag Labs core flows, so that I can see how tests are structured, how they use page objects, and how they map to manual test cases.

#### Acceptance Criteria

1. THE Demo_QA SHALL provide at least one automated test for each of the following flows: login with valid credentials, login with invalid credentials, product catalog browsing, product detail viewing, add to cart, remove from cart, complete checkout, and sorting products
2. EACH automated test SHALL follow the naming convention `check_T{number}_{description}` where `{number}` corresponds to the related manual test case ID in the Test_Library, and SHALL include a docstring with preconditions, steps, and expected results
3. EACH automated test SHALL use page objects for all interactions and assertions, with no direct Appium driver calls in test functions, and SHALL contain at least one explicit assertion validating the expected outcome
4. THE Demo_QA SHALL mark tests with markers from the Marker_System: smoke for critical-path flows (login with valid credentials, add to cart, complete checkout), and regression for all remaining flows (invalid login, catalog browsing, product detail, remove from cart, sorting)
5. THE Demo_QA SHALL provide at least 3 smoke tests and at least 10 regression tests covering the Swag Labs feature set
6. WHEN a test fails, THE Mini_Framework SHALL capture a screenshot saved to the reports/ directory with the filename format `{test_name}_{timestamp}.png` and include the screenshot file path in the HTML test report
7. EACH automated test SHALL be independently executable without dependency on the execution order of other tests

### Requirement 9: Manual Test Case Library

**User Story:** As a QA engineer, I want a structured manual test case library for Swag Labs, so that I can understand test case design methodology and see how manual cases map to automated tests.

#### Acceptance Criteria

1. THE Test_Library SHALL organize test cases into feature-group directories: login, catalog, cart, and checkout, with each directory containing markdown files where each file represents one test case
2. EACH test case SHALL follow a structured format containing: ID (following the pattern TC_[feature]_[number], e.g., TC_LOGIN_001), title (maximum 80 characters), objective (starting with "Verify that..." or "Ensure that..."), preconditions (as a bullet list of all required setup conditions), test steps (numbered sequentially, minimum 3 steps per test case), expected results (one per step, specific and measurable), priority (High, Normal, or Low), test scope (Mandatory Regression Test, Smoke Test, or Extended Regression Test), and automation status (automated, planned, or manual-only)
3. THE Test_Library SHALL include at least 5 test cases per feature group (minimum 20 total), with at least 2 test cases per group classified as High priority
4. THE Test_Library SHALL classify each test case by automation dependency: A (app-only, no external systems needed), B (external validation required), C (hardware required), or D (precondition-dependent, requires specific state setup)
5. THE Test_Library SHALL include a coverage analysis document mapping each manual test case ID to its corresponding automated test function name (check_T{number}_{description}), stating the automation status (automated, planned, or manual-only), and providing a one-sentence justification for each gap where no automated test exists
6. THE Test_Library SHALL follow the quality standards defined in docs/standards/ including the quality checklist and field requirements, ensuring each test case can be executed by a tester from its description alone without requiring additional information

### Requirement 10: Test Case Quality Standards

**User Story:** As a QA engineer, I want documented quality standards for test cases, so that I can write consistent, high-quality test cases and review others' work against a clear benchmark.

#### Acceptance Criteria

1. THE Demo_QA SHALL provide a quality checklist document in docs/standards/ defining validation criteria for test case fields (title, objective, preconditions, steps, expected results) and classifying each violation by severity level: Critical (blocks Valid status), Warning (should fix before Valid), and Minor (advisory improvement)
2. THE Demo_QA SHALL provide a field requirements document specifying mandatory fields, formatting rules, and at least 1 good and 1 bad example per mandatory field demonstrating correct and incorrect test case content
3. THE Demo_QA SHALL define a status workflow for test cases with the states Draft, Ready for Review, Valid, and Deprecated, including the allowed transitions between states and the criteria that must be satisfied before each transition (e.g., all Critical violations resolved before moving from Ready for Review to Valid)
4. THE Demo_QA SHALL provide at least 1 example of a common quality violation with a corrected version for each test case field (title, objective, preconditions, steps, expected results)
5. THE Demo_QA SHALL include a test case template file in test_library/ containing all mandatory fields defined in the field requirements document, with placeholder text indicating what content is expected in each field

### Requirement 11: SDD Process Documentation (Training Guide)

**User Story:** As a new QA team member, I want a complete training guide documenting the SDD process applied to QA, so that I can learn the methodology and apply it to future projects.

#### Acceptance Criteria

1. THE SDD_Guide SHALL document the following phases in sequential order: Phase 0 (App Analysis), Phase 1 (Test Planning), Phase 2 (Test Case Design), Phase 3 (Test Library Management), Phase 4 (Automation Framework Setup), Phase 5 (Test Automation), Phase 6 (Execution and Reporting), Phase 7 (Maintenance and CI/CD)
2. EACH phase document SHALL include: objectives, inputs, outputs, step-by-step instructions, at least 1 worked example per section, a checklist of deliverables, and a list of prerequisites from prior phases that must be completed before starting
3. THE SDD_Guide SHALL be self-contained so that a reader can follow the entire process without access to external repositories or documentation; all referenced templates, command sequences, configuration snippets, and example outputs SHALL be included inline within the guide
4. THE SDD_Guide SHALL include the Swag Labs app analysis as a worked example demonstrating Phase 0, covering at least 3 identified features, at least 5 screens, at least 2 end-to-end user flows, and the criteria used to define test boundaries (what is in scope vs. out of scope for testing)
5. THE SDD_Guide SHALL include a test plan document for Swag Labs demonstrating Phase 1 (scope, approach, entry/exit criteria, risk assessment)
6. THE SDD_Guide SHALL include a decision matrix for automation vs. manual testing that lists at least 3 evaluation factors (such as execution frequency, test stability, and external dependency complexity) and demonstrates how each factor applies to Swag Labs test cases
7. THE SDD_Guide SHALL include setup guides for all tools used in the project (Android Studio emulator creation, Appium installation and configuration, Python virtual environment setup)
8. THE SDD_Guide SHALL include a table of contents listing all phases with their document locations within the project, enabling sequential navigation from Phase 0 through Phase 7

### Requirement 12: Process Journal

**User Story:** As a QA team member learning SDD, I want to see the actual prompts, decisions, and iterations that produced this project, so that I can replicate the process on new projects.

#### Acceptance Criteria

1. THE Process_Journal SHALL document at least 2 example prompts per SDD phase, each including the goal of the prompt, the context or input provided, and the outcome or response summary
2. THE Process_Journal SHALL include a decision log with at least 4 entries (including Android over iOS, emulator over real device, pytest over unittest, POM over screenplay pattern), where each entry states the decision made, the alternatives considered, and the rationale for the chosen approach
3. THE Process_Journal SHALL include at least 3 Q&A examples showing iterative refinement, where each example presents the initial version, the question or feedback that triggered refinement, and the revised version for requirements, test cases, or framework design
4. THE Process_Journal SHALL be organized chronologically following the SDD phases defined in the SDD_Guide (Phase 0 through Phase 7), with a dedicated section header for each phase
5. THE Process_Journal SHALL include at least 3 lessons learned and at least 3 pitfalls, where each entry states the situation encountered, the impact or consequence, and the recommended action to avoid or address it

### Requirement 13: Configuration Management

**User Story:** As a QA engineer, I want centralized configuration files for the app and emulator settings, so that I can modify test parameters without changing code.

#### Acceptance Criteria

1. THE Demo_QA SHALL provide a config/apps.yaml file containing: APK file path, app package name, app activity name, and app version for Swag Labs
2. THE Demo_QA SHALL provide a config/emulators.yaml file containing: emulator name, platform version, Appium server URL, and port (valid range: 1024–65535)
3. IF a required configuration key is absent or its value is null or empty in the YAML file, THEN THE Mini_Framework SHALL raise a ConfigurationError indicating the missing key name and the file path
4. THE Mini_Framework SHALL support overriding any configuration value via environment variables using the naming convention `DEMO_QA_<SECTION>_<KEY>` (uppercase, underscores replacing dots), where environment variables take precedence over YAML file values
5. THE Demo_QA SHALL include a config/README.md explaining each configuration parameter and its valid values
6. IF a configuration YAML file does not exist at the expected path or contains invalid YAML syntax, THEN THE Mini_Framework SHALL raise a ConfigurationError indicating the file path and whether the file is missing or malformed

### Requirement 14: Reusable Test Flows

**User Story:** As a QA engineer, I want reusable test flows for common multi-step operations, so that I can avoid code duplication across tests and see how flow composition works.

#### Acceptance Criteria

1. THE Mini_Framework SHALL provide reusable flow functions for: login_flow (driver, username, password) returning ProductsPage, add_product_to_cart_flow (driver, product_name) returning CartPage, and complete_checkout_flow (driver, first_name, last_name, zip_code) returning CheckoutCompletePage
2. EACH flow function SHALL use page objects internally and return the resulting page object instance so that subsequent flow calls or assertions can chain from the returned page
3. IF a flow function receives an empty string, a None value, or a whitespace-only string for any required parameter, THEN THE flow function SHALL raise a ValueError indicating which parameter failed validation
4. IF a page transition within a flow fails due to an unexpected application state, THEN THE flow function SHALL raise a PageNotLoadedError identifying the expected page and the flow step that failed
5. THE Mini_Framework SHALL document the flow composition pattern with at least 2 examples showing how flows combine in test scenarios that chain 2 or more flow functions in sequence (e.g., login_flow followed by add_product_to_cart_flow followed by complete_checkout_flow)

### Requirement 15: Extensibility for Real Devices and Additional Platforms

**User Story:** As a QA engineer, I want the framework structured to support future expansion to real devices and iOS, so that I can understand how to scale the architecture without rewriting it.

#### Acceptance Criteria

1. THE Mini_Framework SHALL separate driver creation logic from test logic through a configuration-driven factory pattern, so that adding a new platform requires only a new entry in the device configuration YAML file and no modifications to existing test files or page objects
2. THE Demo_QA SHALL include a docs section explaining how to extend the framework for real Android devices, covering at minimum: USB debugging setup, device UDID discovery and configuration, required capabilities changes, and a step-by-step example of adding a real device entry to emulators.yaml
3. THE Demo_QA SHALL include a docs section explaining how to extend the framework for iOS, covering at minimum: Xcode and command-line tools installation, WebDriverAgent build and signing, iOS-specific desired capabilities, and a step-by-step example of adding an iOS device entry to the configuration
4. THE Mini_Framework SHALL use accessibility IDs as the locator strategy for at least 80% of element locators in the Locator_Store, falling back to XPath or resource-id only when an accessibility ID is not available on the target element
5. WHEN a new Appium driver session is created while the framework operates in emulator-only mode, THE Emulator_Manager SHALL log an INFO-level message at session startup indicating that real-device support is available through configuration changes

### Requirement 16: Coverage Analysis and Automation Planning

**User Story:** As a QA engineer, I want to see how test coverage is analyzed and automation priorities are determined, so that I can apply the same methodology to other projects.

#### Acceptance Criteria

1. THE Coverage_Analyzer SHALL produce a document containing a table that maps each manual test case in the Test_Library (by ID and title) to its automation status: automated (with reference to the corresponding check script), planned (with target priority tier), or manual-only (with justification referencing the automation dependency category or a specific technical constraint)
2. THE Coverage_Analyzer SHALL categorize test cases by automation dependency following the classification: A (app-only), B (external validation required), C (hardware required), D (hardware in preconditions only), and SHALL include the estimated test case count per category
3. THE Demo_QA SHALL include an automation plan document that assigns each candidate test case to a priority tier (P1-immediate, P2-next sprint, P3-backlog) based on three scored factors: frequency of execution (high: run every sprint, medium: run every release, low: run quarterly or less), risk level (high: blocks release, medium: affects core flow, low: edge case), and automation feasibility (high: category A, medium: category B or D, low: category C)
4. THE Demo_QA SHALL include a coverage gap analysis identifying each manual test case that has no corresponding automated test, and for each gap SHALL state the automation dependency category (A, B, C, or D) and the specific technical constraint that prevents automation (e.g., requires BLE hardware, requires external SMS verification, requires proxy tooling)
5. THE Demo_QA SHALL document the decision criteria for determining when a test case should remain manual versus being automated, structured as a decision flowchart or ordered rule set that takes as inputs the automation dependency category, execution frequency, risk level, and feasibility score, and produces a recommend action (automate, plan for automation, or keep manual)
6. THE Demo_QA SHALL include in the automation plan at least one worked example per priority tier (P1, P2, P3) showing how the scoring factors were applied to arrive at the assigned tier
