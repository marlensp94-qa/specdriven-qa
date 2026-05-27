# Phase 1: Test Planning

## Objectives

- Define the overall test strategy and approach for the project
- Establish entry and exit criteria for test execution
- Identify risks and mitigation strategies
- Produce a test plan document that guides all subsequent testing activities

## Prerequisites

- Completed Phase 0 (App Analysis) with:
  - Feature inventory
  - Screen catalog
  - User flow diagrams
  - Scope definition

## Inputs

- Phase 0 deliverables (feature inventory, screen catalog, flows, scope)
- Project timeline and resource constraints
- Quality goals and acceptance thresholds
- Known technical constraints (platform, tools, environment)

## Outputs

- Test plan document covering scope, approach, criteria, and risks
- Test schedule with milestones
- Resource and environment requirements
- Risk register with mitigation actions

---

## Step-by-Step Instructions

### Step 1: Define Test Scope

Using the scope definition from Phase 0, formalize what will be tested:

1. List all features in scope with their priority (High, Medium, Low)
2. Identify test levels (unit, integration, system, acceptance)
3. Define test types to apply (functional, smoke, regression, negative, boundary)
4. Document any scope exclusions with justification

### Step 2: Choose Test Approach

Decide on the testing methodology:

1. Select test design techniques (equivalence partitioning, boundary value, decision table)
2. Define automation strategy (what to automate vs. keep manual)
3. Choose tools and frameworks
4. Define the test environment requirements

### Step 3: Establish Entry Criteria

Define conditions that must be met before testing begins:

1. Environment readiness (emulator configured, Appium running)
2. Build availability (APK installed and launchable)
3. Test data prepared (user credentials, product data)
4. Prerequisites verified (all tools installed, versions confirmed)

### Step 4: Establish Exit Criteria

Define conditions that signal testing is complete:

1. Test execution thresholds (e.g., 100% smoke tests pass)
2. Defect resolution requirements (e.g., no open Critical defects)
3. Coverage targets (e.g., all High-priority test cases executed)
4. Sign-off requirements

### Step 5: Perform Risk Assessment

Identify and assess risks to the testing effort:

1. List potential risks (technical, resource, schedule, quality)
2. Assess likelihood (High, Medium, Low) and impact (High, Medium, Low)
3. Define mitigation strategies for each risk
4. Assign risk owners

### Step 6: Define Schedule and Milestones

Create a timeline for testing activities:

1. Map phases to calendar time
2. Identify dependencies between phases
3. Set milestone checkpoints
4. Plan for contingency time

---

## Worked Example: Swag Labs Test Plan

### 1. Test Plan Overview

| Field | Value |
|-------|-------|
| **Project** | Swag Labs Mobile QA Demo |
| **Application** | Swag Labs Mobile (Android) |
| **Version** | Latest from Sauce Labs GitHub |
| **Test Lead** | QA Engineer (training participant) |
| **Environment** | Android Emulator (API 29+), Appium 2.x |
| **Approach** | Risk-based, automation-first |

### 2. Scope

#### In Scope

| Feature | Priority | Test Types | Automation |
|---------|----------|------------|------------|
| Authentication | High | Functional, Negative, Smoke | Automated |
| Product Catalog | High | Functional, Smoke | Automated |
| Shopping Cart | High | Functional, Negative, Smoke | Automated |
| Checkout | High | Functional, Negative, Smoke | Automated |
| Product Sorting | Medium | Functional, Regression | Automated |

#### Out of Scope

- Performance and load testing
- Security/penetration testing
- iOS platform testing
- Network failure scenarios
- Accessibility compliance audit

### 3. Test Approach

#### Test Levels

| Level | Description | Tools | Scope |
|-------|-------------|-------|-------|
| Unit | Framework component tests | pytest, Hypothesis | ConfigLoader, Markers, ReportGenerator |
| Integration | End-to-end flows against real app | pytest, Appium | Login, Checkout, Cart flows |
| System | Full regression suite | pytest, Appium | All check scripts |
| Smoke | Critical path verification | pytest, Appium | Login, Add to Cart, Checkout |

#### Test Design Techniques

- **Equivalence Partitioning:** Group inputs into valid/invalid classes (e.g., valid users vs. locked users)
- **Boundary Value Analysis:** Test field limits (empty, max length, special characters)
- **Decision Table:** Map input combinations to expected outcomes (login scenarios)
- **State Transition:** Verify navigation flows between screens
- **Error Guessing:** Based on common mobile app defects (timeouts, stale elements)

#### Automation Strategy

- **Automate:** All smoke tests, regression tests for stable features, data-driven scenarios
- **Keep Manual:** Exploratory testing, visual verification, one-time setup validation
- **Framework:** Python + Appium + pytest with Page Object Model
- **Execution:** Local emulator, on-demand (no CI/CD in initial phase)

### 4. Entry Criteria

| # | Criterion | Verification Method |
|---|-----------|-------------------|
| 1 | Android emulator created and running (API 29+) | `adb devices` shows emulator |
| 2 | Appium server running on configured port | `curl http://localhost:4723/status` returns OK |
| 3 | Swag Labs APK installed on emulator | App launches successfully |
| 4 | Python environment set up with all dependencies | `pip list` shows all packages |
| 5 | Configuration files populated with correct values | ConfigLoader loads without error |
| 6 | Test user credentials verified | Manual login with `standard_user` succeeds |

### 5. Exit Criteria

| # | Criterion | Threshold |
|---|-----------|-----------|
| 1 | Smoke tests pass rate | 100% (all 3 smoke tests pass) |
| 2 | Regression tests pass rate | ≥ 90% (at most 1 failure allowed) |
| 3 | Critical defects | 0 open Critical defects |
| 4 | High-priority test cases executed | 100% executed |
| 5 | Test case coverage | All manual test cases have execution status |
| 6 | Documentation complete | All phase deliverables checked off |

### 6. Risk Assessment

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | Appium session instability (random disconnects) | Medium | High | Implement retry logic in fixtures; add session health check before each test |
| 2 | Emulator performance degradation over time | Medium | Medium | Restart emulator between test suites; use cold boot for consistency |
| 3 | Swag Labs APK update breaks locators | Low | High | Use accessibility IDs (stable); maintain Locator Store as single source of truth |
| 4 | Element timing issues (flaky tests) | High | Medium | Use explicit waits with configurable timeouts; avoid implicit waits |
| 5 | Test environment setup complexity | Medium | Medium | Provide detailed setup guide; include verification steps |
| 6 | Test data dependency (user state) | Low | Medium | Each test starts from login; use function-scoped fixtures for isolation |

### 7. Test Environment

| Component | Specification |
|-----------|--------------|
| Host OS | macOS / Windows / Linux |
| Python | 3.8+ |
| Android Studio | Latest stable |
| Android SDK | API 29+ (Android 10+) |
| Emulator | Pixel 4 profile, Google APIs system image |
| Appium | 2.x |
| Appium Driver | UiAutomator2 |
| Test Runner | pytest 7.0+ |
| APK | Swag Labs Mobile (Sauce Labs GitHub) |

### 8. Test Schedule

| Phase | Activities | Duration | Dependencies |
|-------|-----------|----------|--------------|
| Phase 0 | App Analysis | 1 day | Application access |
| Phase 1 | Test Planning | 1 day | Phase 0 complete |
| Phase 2 | Test Case Design | 2 days | Phase 1 complete |
| Phase 3 | Test Library Management | 1 day | Phase 2 complete |
| Phase 4 | Framework Setup | 2 days | Phase 1 complete |
| Phase 5 | Test Automation | 3 days | Phase 3, 4 complete |
| Phase 6 | Execution & Reporting | 1 day | Phase 5 complete |
| Phase 7 | Maintenance & CI/CD | 1 day | Phase 6 complete |

### 9. Deliverables

| Deliverable | Location | Phase |
|-------------|----------|-------|
| Test Plan | `docs/01-sdd-guide/phase-1-test-planning.md` | 1 |
| Manual Test Cases | `test_library/` | 2-3 |
| Automation Framework | `framework/` | 4 |
| Automated Tests | `tests/check_scripts/` | 5 |
| Test Reports | `reports/` | 6 |
| Coverage Analysis | `test_library/coverage_analysis.md` | 6 |

---

## Deliverables Checklist

- [ ] Test scope defined (features, test levels, test types, exclusions)
- [ ] Test approach documented (techniques, automation strategy, tools)
- [ ] Entry criteria established with verification methods
- [ ] Exit criteria established with measurable thresholds
- [ ] Risk assessment completed (at least 4 risks with likelihood, impact, mitigation)
- [ ] Test environment specified (all components with versions)
- [ ] Test schedule with milestones and dependencies
- [ ] Deliverables list with locations

---

## Tips and Common Pitfalls

- **Don't over-plan:** The test plan should guide, not constrain. Keep it living and update as you learn more
- **Be realistic with exit criteria:** Setting 100% pass rate for all tests is unrealistic — focus on smoke/critical tests
- **Prioritize risks early:** The risks you identify now will save you debugging time later
- **Entry criteria prevent wasted effort:** Don't start testing until the environment is verified
- **Keep the plan accessible:** Store it where the team can find and reference it easily
