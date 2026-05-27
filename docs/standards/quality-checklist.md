# Quality Checklist for Test Cases

This document defines the validation criteria applied to each test case field, severity classifications for violations, and the status workflow governing test case lifecycle.

---

## Severity Levels

| Level | Label | Impact |
|-------|-------|--------|
| 🔴 | **Critical** | Blocks transition to Valid status. Must be resolved before approval. |
| 🟡 | **Warning** | Should be fixed before Valid status. Reviewer may grant exception with justification. |
| 🟢 | **Minor** | Advisory improvement. Does not block approval but improves consistency. |

---

## Field Validation Criteria

### Title

| # | Criterion | Severity |
|---|-----------|----------|
| T1 | Title is present and non-empty | Critical |
| T2 | Title is ≤ 80 characters | Critical |
| T3 | Title describes the specific behavior being tested (not generic) | Warning |
| T4 | Title does not duplicate another test case title in the same feature group | Warning |
| T5 | Title uses sentence case (first word capitalized, rest lowercase unless proper noun) | Minor |

**Common Violations:**

| Violation | Corrected Version |
|-----------|-------------------|
| ❌ `Login test` (too generic) | ✅ `Verify login with valid standard_user credentials` |
| ❌ `Verify that the user can successfully log in to the application using valid credentials and see the products page displayed correctly` (exceeds 80 chars) | ✅ `Verify successful login displays products page` |

---

### Objective

| # | Criterion | Severity |
|---|-----------|----------|
| O1 | Objective is present and non-empty | Critical |
| O2 | Objective starts with "Verify that..." or "Ensure that..." | Critical |
| O3 | Objective states a single, testable behavior | Warning |
| O4 | Objective does not repeat the title verbatim | Warning |
| O5 | Objective is one sentence (no line breaks or bullet points) | Minor |

**Common Violations:**

| Violation | Corrected Version |
|-----------|-------------------|
| ❌ `Test the login functionality` (missing required prefix) | ✅ `Verify that a user can log in with valid credentials and is redirected to the products page` |
| ❌ `Verify that login works and cart works and checkout works` (multiple behaviors) | ✅ `Verify that a user can log in with valid credentials` |

---

### Preconditions

| # | Criterion | Severity |
|---|-----------|----------|
| P1 | Preconditions section is present | Critical |
| P2 | At least one precondition is listed | Warning |
| P3 | Each precondition is a bullet point (markdown list item) | Warning |
| P4 | Preconditions include app state (e.g., "App is installed and launched") | Warning |
| P5 | Preconditions are specific enough to reproduce (no ambiguous references) | Warning |
| P6 | Preconditions do not include test steps (actions to perform) | Minor |

**Common Violations:**

| Violation | Corrected Version |
|-----------|-------------------|
| ❌ `User is ready` (ambiguous) | ✅ `- Swag Labs app is installed on the emulator`<br>`- App is launched and login screen is displayed`<br>`- Valid test credentials are available (standard_user / secret_sauce)` |
| ❌ `1. Open the app 2. Navigate to login` (contains steps, not conditions) | ✅ `- App is launched and login screen is displayed` |

---

### Test Steps

| # | Criterion | Severity |
|---|-----------|----------|
| S1 | Steps section is present and non-empty | Critical |
| S2 | Minimum 3 steps are defined | Critical |
| S3 | Steps are numbered sequentially starting from 1 | Warning |
| S4 | Each step describes a single user action | Warning |
| S5 | Steps use imperative verbs (Tap, Enter, Navigate, Select) | Warning |
| S6 | Steps reference specific UI elements or values (not "click the button") | Warning |
| S7 | Steps are formatted as a markdown table with Step, Action, Expected Result columns | Minor |

**Common Violations:**

| Violation | Corrected Version |
|-----------|-------------------|
| ❌ `1. Login and add item to cart and checkout` (multiple actions in one step) | ✅ `1. Enter "standard_user" in the Username field`<br>`2. Enter "secret_sauce" in the Password field`<br>`3. Tap the LOGIN button` |
| ❌ `1. Do the thing` (vague, no specific element) | ✅ `1. Tap the "Sauce Labs Backpack" product title on the Products screen` |

---

### Expected Results

| # | Criterion | Severity |
|---|-----------|----------|
| E1 | Expected results section is present | Critical |
| E2 | One expected result exists per test step | Critical |
| E3 | Each result is specific and measurable (observable state or value) | Warning |
| E4 | Results describe what IS displayed/visible, not what is NOT | Warning |
| E5 | Results do not use vague terms ("works correctly", "is fine", "looks good") | Warning |
| E6 | Results include specific text, values, or UI states where applicable | Minor |

**Common Violations:**

| Violation | Corrected Version |
|-----------|-------------------|
| ❌ `Login works` (not measurable) | ✅ `Products page is displayed with the title "PRODUCTS" visible` |
| ❌ `Error message appears` (not specific) | ✅ `Error message "Username and Password do not match any user in this service" is displayed below the login form` |

---

## Status Workflow

```
┌───────┐      ┌──────────────────┐      ┌───────┐      ┌────────────┐
│ Draft │ ───► │ Ready for Review │ ───► │ Valid │ ───► │ Deprecated │
└───────┘      └──────────────────┘      └───────┘      └────────────┘
                        │                      │
                        ▼                      │
                   ┌───────┐                   │
                   │ Draft │ ◄─────────────────┘
                   └───────┘   (if rework needed)
```

### Transition Criteria

| From | To | Criteria |
|------|----|----------|
| **Draft** | **Ready for Review** | All mandatory fields are populated. No Critical violations remain. Author self-review completed. |
| **Ready for Review** | **Valid** | Peer review completed. All Critical violations resolved. All Warning violations resolved or explicitly waived with justification. Test case is executable by a tester from its description alone. |
| **Ready for Review** | **Draft** | Reviewer identifies Critical violations or fundamental issues requiring rework. |
| **Valid** | **Deprecated** | Feature removed, test case superseded by another, or application behavior permanently changed making the test case irrelevant. Deprecation reason documented. |
| **Valid** | **Draft** | Application change requires test case update. Previous Valid status revoked until re-review. |

### Status Definitions

| Status | Description |
|--------|-------------|
| **Draft** | Test case is being written or revised. Not ready for execution or review. |
| **Ready for Review** | Author considers the test case complete. Awaiting peer review. |
| **Valid** | Peer-reviewed and approved. Ready for execution. Meets all quality standards. |
| **Deprecated** | No longer applicable. Retained for historical reference but excluded from execution. |

---

## Review Checklist (Quick Reference)

Use this checklist during peer review. A test case passes review when all Critical items are ✅ and all Warning items are either ✅ or explicitly waived.

- [ ] **Title**: Present, ≤80 chars, specific behavior described
- [ ] **Objective**: Present, starts with "Verify that..." or "Ensure that...", single behavior
- [ ] **Preconditions**: Present, bullet list, specific and reproducible
- [ ] **Steps**: Present, ≥3 steps, numbered, single action per step, specific elements referenced
- [ ] **Expected Results**: Present, one per step, specific and measurable
- [ ] **Priority**: Set to High, Normal, or Low
- [ ] **Test Scope**: Set to valid value (Smoke Test, Mandatory Regression Test, Extended Regression Test)
- [ ] **Automation Status**: Set to automated, planned, or manual-only
- [ ] **Automation Dependency**: Set to A, B, C, or D
- [ ] **Executable**: A tester can execute this test case from its description alone without additional information
