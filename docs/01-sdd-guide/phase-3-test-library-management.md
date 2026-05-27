# Phase 3: Test Library Management

## Objectives

- Establish a well-organized test case library with consistent structure and naming
- Define and enforce quality standards for test case content
- Implement a review workflow that ensures test cases are executable and maintainable
- Create processes for maintaining the library as the application evolves

## Prerequisites

- Completed Phase 0 (App Analysis) with feature inventory and scope definition
- Completed Phase 1 (Test Planning) with test approach and automation strategy
- Completed Phase 2 (Test Case Design) with:
  - Test cases written for all in-scope features
  - Automation decisions documented
  - Dependency categories assigned
- Quality standards documents available:
  - `docs/standards/field-requirements.md`
  - `docs/standards/quality-checklist.md`

## Inputs

- Test cases from Phase 2 (all feature groups)
- Quality checklist (`docs/standards/quality-checklist.md`)
- Field requirements (`docs/standards/field-requirements.md`)
- Test case template (`test_library/template.md`)

## Outputs

- Organized test library directory structure
- All test cases validated against quality standards
- Review workflow documented and applied
- Coverage analysis document mapping manual cases to automation status
- Maintenance procedures for ongoing library health

---

## Step-by-Step Instructions

### Step 1: Establish Directory Structure

Organize the test library by feature group. Each feature gets its own directory containing individual test case files.

```
test_library/
├── template.md              # Canonical test case template
├── coverage_analysis.md     # Coverage mapping document
├── login/
│   ├── TC_LOGIN_001.md
│   ├── TC_LOGIN_002.md
│   ├── TC_LOGIN_003.md
│   ├── TC_LOGIN_004.md
│   └── TC_LOGIN_005.md
├── catalog/
│   ├── TC_CATALOG_001.md
│   ├── TC_CATALOG_002.md
│   ├── TC_CATALOG_003.md
│   ├── TC_CATALOG_004.md
│   └── TC_CATALOG_005.md
├── cart/
│   ├── TC_CART_001.md
│   ├── TC_CART_002.md
│   ├── TC_CART_003.md
│   ├── TC_CART_004.md
│   └── TC_CART_005.md
└── checkout/
    ├── TC_CHECKOUT_001.md
    ├── TC_CHECKOUT_002.md
    ├── TC_CHECKOUT_003.md
    ├── TC_CHECKOUT_004.md
    └── TC_CHECKOUT_005.md
```

**Naming conventions:**
- Directory names: lowercase feature group name (e.g., `login`, `cart`)
- File names: test case ID in uppercase with `.md` extension (e.g., `TC_LOGIN_001.md`)
- One test case per file — never combine multiple test cases in a single file

### Step 2: Apply Quality Standards

Run each test case through the quality checklist. For each test case:

1. Open the test case file
2. Check each field against `docs/standards/quality-checklist.md`
3. Record any violations found with their severity level
4. Fix all Critical violations immediately
5. Fix Warning violations or document exceptions
6. Note Minor violations for future improvement

**Quality validation summary table (create for each feature group):**

| Test Case ID | Critical | Warning | Minor | Status |
|-------------|----------|---------|-------|--------|
| TC_LOGIN_001 | 0 | 0 | 1 | Ready for Review |
| TC_LOGIN_002 | 0 | 1 | 0 | Draft (fixing) |
| ... | ... | ... | ... | ... |

### Step 3: Execute the Review Workflow

Follow the status workflow defined in the quality checklist:

```
Draft → Ready for Review → Valid → (Deprecated if needed)
```

#### 3a. Self-Review (Draft → Ready for Review)

Before submitting for peer review, the author verifies:

1. All mandatory fields are populated (no empty or placeholder values)
2. No Critical violations remain
3. Test case is executable from its description alone
4. ID is unique across the entire library
5. Objective starts with "Verify that..." or "Ensure that..."
6. Steps are numbered, minimum 3, one action per step
7. Expected results are specific and measurable (no "works correctly")

#### 3b. Peer Review (Ready for Review → Valid)

The reviewer checks:

1. **Executability:** Can a tester who has never seen this test case execute it without asking questions?
2. **Completeness:** Are all preconditions stated? Are all steps present?
3. **Specificity:** Are expected results measurable? Do they reference specific text, values, or UI states?
4. **Independence:** Can this test case run without depending on another test case's execution?
5. **Consistency:** Does it follow the same patterns as other test cases in the library?

**Review outcomes:**
- **Approve** → Status moves to Valid
- **Request changes** → Status returns to Draft with specific feedback
- **Waive warning** → Reviewer documents justification, status moves to Valid

#### 3c. Deprecation (Valid → Deprecated)

A test case is deprecated when:
- The feature it tests has been removed from the application
- It has been superseded by a more comprehensive test case
- The application behavior has permanently changed making the test irrelevant

**Deprecation process:**
1. Add a `Deprecated` header to the test case file
2. Document the reason for deprecation
3. Reference the superseding test case (if applicable)
4. Do NOT delete the file — retain for historical reference

### Step 4: Create Coverage Analysis

Produce a coverage analysis document (`test_library/coverage_analysis.md`) that maps each manual test case to its automation status:

1. List every test case ID and title
2. For automated cases: reference the corresponding `check_T{number}_{description}.py` script
3. For planned cases: note the target priority tier (P1, P2, P3)
4. For manual-only cases: provide a one-sentence justification explaining why automation is not feasible

### Step 5: Establish Maintenance Procedures

Define how the library stays current as the application evolves:

1. **Trigger events:** When does a test case need updating?
   - Application UI changes (locators, flow, text)
   - New feature added (new test cases needed)
   - Bug found not covered by existing tests (gap identified)
   - Test case fails repeatedly (may need revision)

2. **Update process:**
   - Identify affected test cases
   - Move status back to Draft
   - Apply changes
   - Re-run through review workflow
   - Update coverage analysis if automation status changes

3. **Periodic review cadence:**
   - Monthly: Check for deprecated test cases
   - Per release: Verify all Valid test cases still pass
   - Quarterly: Review coverage gaps and prioritize automation

---

## Worked Example: Swag Labs Test Library Management

### Library Organization

The Swag Labs test library is organized into 4 feature groups with 5+ test cases each:

| Feature Group | Directory | Test Cases | High Priority | Coverage |
|--------------|-----------|-----------|---------------|----------|
| Login | `test_library/login/` | 5 | 2 | 100% of login scenarios |
| Catalog | `test_library/catalog/` | 5 | 2 | Core browsing + sorting |
| Cart | `test_library/cart/` | 5 | 2 | Add, remove, badge |
| Checkout | `test_library/checkout/` | 5 | 2 | Complete flow + errors |

### Quality Validation Example

**Reviewing TC_LOGIN_001:**

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| T1 | Title present and non-empty | ✅ | "Verify login with valid standard_user credentials displays products page" |
| T2 | Title ≤ 80 characters | ✅ | 72 characters |
| O1 | Objective present | ✅ | |
| O2 | Starts with "Verify that..." | ✅ | |
| P1 | Preconditions present | ✅ | 3 bullet points |
| S1 | Steps present | ✅ | |
| S2 | Minimum 3 steps | ✅ | 4 steps |
| E1 | Expected results present | ✅ | |
| E2 | One per step | ✅ | 4 results for 4 steps |

**Result:** 0 Critical, 0 Warning, 0 Minor → Status: **Valid**

### Review Workflow in Practice

**Scenario: TC_LOGIN_004 has a Warning violation**

Initial version (Draft):
```markdown
## Expected Results
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Leave Username field empty | Field remains empty |
| 2 | Leave Password field empty | Field remains empty |
| 3 | Tap LOGIN button | Error appears |
```

**Reviewer feedback:** Step 3 expected result violates E3 (not specific/measurable). Which error? What text? Where is it displayed?

Revised version:
```markdown
## Expected Results
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Leave Username field empty | Username field shows no text |
| 2 | Leave Password field empty | Password field shows no text |
| 3 | Tap LOGIN button | Error message "Username is required" is displayed below the login form in red |
```

**Result:** Warning resolved → Status moves to **Valid**

### Coverage Analysis Example

Excerpt from `test_library/coverage_analysis.md`:

| Test Case ID | Title | Check Script | Status | Gap Justification |
|-------------|-------|-------------|--------|-------------------|
| TC_LOGIN_001 | Valid login with standard_user | `check_T001_login_valid_credentials.py` | automated | — |
| TC_LOGIN_002 | Login with invalid credentials | `check_T002_login_invalid_credentials.py` | automated | — |
| TC_LOGIN_003 | Login with locked_out_user | `check_T002_login_invalid_credentials.py` | automated | — |
| TC_LOGIN_004 | Login with empty fields | `check_T003_login_empty_fields.py` | automated | — |
| TC_LOGIN_005 | Logout from products page | — | planned | P2: Requires menu interaction automation |
| TC_CATALOG_005 | Product images display correctly | — | manual-only | Visual judgment required; pixel comparison is brittle |

### Maintenance Trigger Example

**Scenario:** Swag Labs updates their APK and the login error message text changes from "Username and Password do not match" to "Invalid credentials."

**Impact assessment:**
1. TC_LOGIN_002 — Expected result references old error text → needs update
2. TC_LOGIN_003 — Expected result references "locked out" text → verify still correct
3. `check_T002_login_invalid_credentials.py` — Assertion string needs update

**Update process:**
1. Move TC_LOGIN_002 status from Valid → Draft
2. Update expected result text to match new error message
3. Self-review: all fields still valid
4. Move to Ready for Review
5. Peer review: approve → Valid
6. Update corresponding check script assertion
7. Run check script to verify it passes

---

## Library Health Metrics

Track these metrics to monitor library quality over time:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Valid test cases | ≥ 90% of total | Count Valid / Total |
| Coverage (automated) | ≥ 60% of test cases | Count automated / Total |
| Orphaned test cases | 0 | Test cases with no matching feature |
| Stale test cases | 0 | Valid cases that haven't been executed in 2+ releases |
| Average steps per case | 3-8 | Sum of steps / Total cases |
| High-priority coverage | 100% automated | All High-priority cases have check scripts |

---

## Deliverables Checklist

- [ ] Test library directory structure created with feature group subdirectories
- [ ] All test cases organized into correct feature group directories
- [ ] Each test case file contains one test case with all mandatory fields
- [ ] Quality validation completed for all test cases (no Critical violations)
- [ ] Review workflow applied: all test cases have a documented status (Draft, Ready for Review, Valid)
- [ ] At least 2 High-priority test cases per feature group
- [ ] Coverage analysis document created mapping all test cases to automation status
- [ ] Manual-only test cases have documented justification
- [ ] Maintenance procedures documented (triggers, update process, review cadence)
- [ ] File naming conventions followed consistently (TC_[FEATURE]_[NUMBER].md)

---

## Tips and Common Pitfalls

- **One file per test case:** Never combine multiple test cases in a single file. It makes maintenance, review, and status tracking much harder
- **Don't skip peer review:** Self-review catches formatting issues, but peer review catches executability problems. A fresh pair of eyes will find ambiguities you missed
- **Keep the coverage analysis current:** Update it whenever a test case is automated or a new test case is added. Stale coverage documents lose their value quickly
- **Deprecate, don't delete:** Removing test case files loses history. Mark them deprecated with a reason so future team members understand what changed
- **Automate the quality check where possible:** The field requirements are mechanical enough to validate with a script. Consider building a linter for test case files
- **Review in batches:** Don't review one test case at a time. Review an entire feature group together to catch inconsistencies and duplicates
- **Track metrics monthly:** Library health degrades silently. Regular metric checks surface problems before they compound
