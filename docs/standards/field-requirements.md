# Field Requirements for Test Cases

This document specifies mandatory fields, formatting rules, and examples for each field in a test case. All test cases in the Test Library must conform to these requirements.

---

## Mandatory Fields

Every test case **must** include all of the following fields. A test case missing any mandatory field cannot advance beyond Draft status.

| # | Field | Required | Format |
|---|-------|----------|--------|
| 1 | Test Case ID | Yes | `TC_[FEATURE]_[NUMBER]` |
| 2 | Title | Yes | Plain text, ≤ 80 characters |
| 3 | Objective | Yes | Sentence starting with "Verify that..." or "Ensure that..." |
| 4 | Preconditions | Yes | Markdown bullet list (≥ 1 item) |
| 5 | Test Steps | Yes | Markdown table with ≥ 3 rows |
| 6 | Expected Results | Yes | One per step (included in steps table) |
| 7 | Priority | Yes | One of: High, Normal, Low |
| 8 | Test Scope | Yes | One of: Smoke Test, Mandatory Regression Test, Extended Regression Test |
| 9 | Automation Status | Yes | One of: automated, planned, manual-only |
| 10 | Automation Dependency Category | Yes | One of: A, B, C, D |

---

## Field Specifications and Examples

### 1. Test Case ID

**Format:** `TC_[FEATURE]_[NUMBER]`

**Rules:**
- FEATURE is the module/feature name in uppercase (e.g., LOGIN, CART, CATALOG, CHECKOUT)
- NUMBER is zero-padded to 3 digits (001, 002, ..., 999)
- Must be unique across the entire Test Library

| | Example |
|---|---------|
| ✅ Good | `TC_LOGIN_001` |
| ❌ Bad | `Login-Test-1` (wrong format, not uppercase, no zero-padding) |

---

### 2. Title

**Format:** Plain text, maximum 80 characters

**Rules:**
- Describes the specific behavior or scenario being tested
- Concise but informative — a reader should understand what the test validates
- Use sentence case
- Do not include the test case ID in the title

| | Example |
|---|---------|
| ✅ Good | `Verify login with valid standard_user credentials displays products page` |
| ❌ Bad | `Test login` (too vague, does not describe the specific scenario or expected outcome) |

---

### 3. Objective

**Format:** Single sentence starting with "Verify that..." or "Ensure that..."

**Rules:**
- States exactly one testable behavior
- Describes the expected outcome, not just the action
- Must be a complete sentence
- Do not use bullet points or multiple sentences

| | Example |
|---|---------|
| ✅ Good | `Verify that entering valid credentials (standard_user / secret_sauce) and tapping LOGIN redirects the user to the Products page.` |
| ❌ Bad | `Check if login works properly.` (missing required prefix, vague outcome, not specific) |

---

### 4. Preconditions

**Format:** Markdown bullet list with at least one item

**Rules:**
- Each item describes a required state or condition before test execution begins
- Use present tense ("App is installed" not "Install the app")
- Include all environmental requirements (app state, data, credentials)
- Do not include actions the tester must perform (those belong in steps)

| | Example |
|---|---------|
| ✅ Good | `- Swag Labs app is installed on the Android emulator`<br>`- App is launched and the login screen is displayed`<br>`- Test credentials are available: standard_user / secret_sauce` |
| ❌ Bad | `None` (preconditions are always required — at minimum the app must be in a known state) |

---

### 5. Test Steps

**Format:** Markdown table with columns: Step, Action, Expected Result

**Rules:**
- Minimum 3 steps per test case
- Steps are numbered sequentially starting from 1
- Each step describes exactly one user action
- Use imperative verbs: Tap, Enter, Navigate, Select, Scroll, Verify
- Reference specific UI elements by name or label
- Each step has a corresponding expected result in the same row

| | Example |
|---|---------|
| ✅ Good | See table below |

```markdown
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Enter "standard_user" in the Username field | Username field displays "standard_user" |
| 2 | Enter "secret_sauce" in the Password field | Password field displays masked characters |
| 3 | Tap the LOGIN button | Products page loads with title "PRODUCTS" visible |
```

| | Example |
|---|---------|
| ❌ Bad | See table below |

```markdown
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login to the app | It works |
```

(Only 1 step, vague action, vague result, not measurable)

---

### 6. Expected Results

**Format:** One specific, measurable outcome per test step

**Rules:**
- Describes an observable state (what the user sees or the system displays)
- Uses specific text values, element names, or UI states
- Avoids vague terms: "works", "is correct", "looks good", "is fine"
- Describes positive state (what IS visible) rather than negative (what is NOT visible), unless testing error states

| | Example |
|---|---------|
| ✅ Good | `Error message "Username and Password do not match any user in this service" is displayed below the login form in red text` |
| ❌ Bad | `An error shows up` (not specific — which error? where? what text?) |

---

### 7. Priority

**Format:** One of: `High`, `Normal`, `Low`

**Rules:**
- **High**: Critical path functionality. Failure blocks release. Login, checkout completion, core navigation.
- **Normal**: Standard feature coverage. Important but not release-blocking. Sorting, filtering, detail views.
- **Low**: Edge cases, cosmetic validations, rarely-used paths.

| | Example |
|---|---------|
| ✅ Good | `High` (for a login test case — login is critical path) |
| ❌ Bad | `Medium` (not a valid value — must be High, Normal, or Low) |

---

### 8. Test Scope

**Format:** One of: `Smoke Test`, `Mandatory Regression Test`, `Extended Regression Test`

**Rules:**
- **Smoke Test**: Minimal set verifying the app is functional. Run on every build.
- **Mandatory Regression Test**: Standard regression coverage. Run every sprint/release.
- **Extended Regression Test**: Comprehensive coverage. Run before major releases.

| | Example |
|---|---------|
| ✅ Good | `Smoke Test` (for valid login — critical path, run on every build) |
| ❌ Bad | `Regression` (not a valid value — must use the full label) |

---

### 9. Automation Status

**Format:** One of: `automated`, `planned`, `manual-only`

**Rules:**
- **automated**: A corresponding `check_T{number}_{description}.py` script exists
- **planned**: Will be automated in a future sprint (include target in notes if known)
- **manual-only**: Cannot be automated due to technical constraints (document reason)

| | Example |
|---|---------|
| ✅ Good | `automated` (when check_T001_login_valid_credentials.py exists) |
| ❌ Bad | `Auto` (not a valid value — must be lowercase full word) |

---

### 10. Automation Dependency Category

**Format:** One of: `A`, `B`, `C`, `D`

**Rules:**
- **A** — App-only: No external systems needed. Can be automated with Appium alone.
- **B** — External validation required: Needs API calls, database checks, or third-party verification.
- **C** — Hardware required: Needs physical device features (camera, NFC, biometrics).
- **D** — Precondition-dependent: Requires specific app state that is complex to set up programmatically.

| | Example |
|---|---------|
| ✅ Good | `A` (for a login test — only needs the app and Appium) |
| ❌ Bad | `E` (not a valid category — only A through D are defined) |

---

## Formatting Rules Summary

| Rule | Applies To | Description |
|------|-----------|-------------|
| Markdown headers | All fields | Each field uses `##` header level |
| Bullet lists | Preconditions | Use `- ` prefix for each item |
| Tables | Test Steps | Use pipe-delimited markdown table |
| Character limit | Title | Maximum 80 characters |
| Prefix requirement | Objective | Must start with "Verify that..." or "Ensure that..." |
| Numbering | Steps | Sequential integers starting from 1 |
| Minimum count | Steps | At least 3 steps per test case |
| One-to-one mapping | Expected Results | Exactly one result per step |
| Valid values only | Priority, Scope, Status, Category | Must match defined enumerations exactly |

---

## Template Reference

The canonical test case template is located at: `test_library/template.md`

All new test cases should be created by copying this template and filling in each field according to the rules defined in this document.
