# Phase 2: Test Case Design

## Objectives

- Learn and apply structured test design methodologies to produce effective test cases
- Understand when to automate vs. keep tests manual using a decision matrix
- Design test cases that are traceable, repeatable, and independently executable
- Produce a set of test cases covering the target application's core functionality

## Prerequisites

- Completed Phase 0 (App Analysis) with:
  - Feature inventory
  - Screen catalog
  - User flow diagrams
  - Scope definition
- Completed Phase 1 (Test Planning) with:
  - Test scope defined
  - Test approach documented
  - Entry/exit criteria established
  - Risk assessment completed

## Inputs

- Phase 0 deliverables (feature inventory, screen catalog, user flows, scope)
- Phase 1 deliverables (test plan, risk assessment, automation strategy)
- Quality standards from `docs/standards/field-requirements.md`
- Test case template from `test_library/template.md`

## Outputs

- Test cases for each in-scope feature (minimum 5 per feature group)
- Automation vs. manual decision for each test case
- Automation dependency classification (A, B, C, D) per test case
- Traceability mapping between features and test cases

---

## Step-by-Step Instructions

### Step 1: Select a Test Design Technique

Choose the appropriate technique based on the feature being tested. Multiple techniques can be combined for a single feature.

| Technique | Best For | Example |
|-----------|----------|---------|
| Equivalence Partitioning | Input fields with distinct valid/invalid classes | Login: valid user, locked user, invalid user |
| Boundary Value Analysis | Numeric or length-constrained inputs | Zip code: empty, 1 char, max length |
| Decision Table | Multiple inputs with combined outcomes | Login: username × password × user type |
| State Transition | Multi-screen flows with defined states | Cart: empty → has items → checkout |
| Error Guessing | Known failure patterns in mobile apps | Timeout, stale element, rotation |

**How to choose:**

1. Identify the input space for the feature
2. If inputs have clear valid/invalid groups → Equivalence Partitioning
3. If inputs have numeric limits or length constraints → Boundary Value Analysis
4. If multiple inputs combine to produce different outcomes → Decision Table
5. If the feature involves navigation between states → State Transition
6. Always supplement with Error Guessing based on domain knowledge

### Step 2: Identify Test Scenarios

For each feature, derive test scenarios from the chosen technique:

1. List all input variables and their possible values
2. Apply the technique to generate combinations
3. Add negative scenarios (invalid inputs, error paths)
4. Add boundary scenarios (edge values, empty inputs)
5. Prioritize: High (critical path), Normal (standard coverage), Low (edge cases)

### Step 3: Write Test Cases Using the Template

For each scenario, create a test case following the template at `test_library/template.md`:

1. Assign a unique ID following the `TC_[FEATURE]_[NUMBER]` pattern
2. Write a concise title (≤ 80 characters) describing the specific behavior
3. Write the objective starting with "Verify that..." or "Ensure that..."
4. List preconditions (app state, data, credentials needed)
5. Write numbered steps (minimum 3) with one action per step
6. Write one expected result per step (specific, measurable)
7. Assign priority (High, Normal, Low)
8. Assign test scope (Smoke Test, Mandatory Regression Test, Extended Regression Test)

### Step 4: Apply the Automation Decision Matrix

For each test case, evaluate whether it should be automated or kept manual using the decision matrix (see below). Record the decision as the automation status field.

### Step 5: Classify Automation Dependencies

Assign each test case an automation dependency category:

| Category | Definition | Example |
|----------|-----------|---------|
| **A** | App-only — no external systems needed | Login with valid credentials |
| **B** | External validation required — needs API/DB checks | Verify order stored in backend |
| **C** | Hardware required — needs physical device features | Camera scan, NFC tap |
| **D** | Precondition-dependent — complex state setup needed | Test with expired session |

### Step 6: Review and Validate

Before finalizing:

1. Verify each test case meets the quality checklist (`docs/standards/quality-checklist.md`)
2. Ensure no duplicate scenarios across feature groups
3. Confirm traceability: every in-scope feature has at least one test case
4. Verify priority distribution: at least 2 High-priority cases per feature group

---

## Automation vs. Manual Decision Matrix

Use this matrix to determine whether a test case should be automated, planned for automation, or kept manual. Score each factor from 1-3, then sum the scores.

### Evaluation Factors

| Factor | Score 3 (Automate) | Score 2 (Consider) | Score 1 (Keep Manual) |
|--------|-------------------|--------------------|-----------------------|
| **Execution Frequency** | Run every build/sprint | Run every release | Run quarterly or less |
| **Test Stability** | Steps are deterministic, no randomness | Mostly stable with minor variations | Highly variable, depends on timing/state |
| **Data-Driven Potential** | Same steps, many input combinations | Some parameterization possible | Unique scenario, no reuse |
| **External Dependency** | App-only (Category A) | Needs setup but automatable (Category D) | Requires hardware or external system (B, C) |
| **Regression Risk** | Feature changes frequently, high breakage risk | Moderate change frequency | Stable feature, rarely changes |
| **Setup Complexity** | Simple preconditions, easy to reset | Moderate setup, some state management | Complex state, manual intervention needed |

### Scoring Guide

| Total Score | Decision | Automation Status |
|-------------|----------|-------------------|
| 15-18 | **Automate immediately** | `automated` |
| 10-14 | **Plan for automation** | `planned` |
| 6-9 | **Keep manual** | `manual-only` |

### Decision Rules (Override Conditions)

Even if the score suggests automation, keep manual if:
- The test requires visual/aesthetic judgment (layout, color, animation quality)
- The test is a one-time validation that won't be repeated
- The test requires real-time human observation (performance perception)

Even if the score suggests manual, automate if:
- The test is on the critical path (smoke test) regardless of complexity
- The test has caused production incidents in the past
- The test blocks other team members when not executed promptly

---

## Worked Example: Swag Labs Test Case Design

### Feature: Authentication (Login)

#### Technique Applied: Decision Table

**Input Variables:**
- Username: {valid (standard_user), locked (locked_out_user), invalid (unknown_user), empty}
- Password: {valid (secret_sauce), invalid (wrong_pass), empty}

**Decision Table (subset):**

| # | Username | Password | Expected Outcome |
|---|----------|----------|-----------------|
| 1 | valid | valid | Products page displayed |
| 2 | valid | invalid | Error message shown |
| 3 | locked | valid | Locked out error shown |
| 4 | invalid | valid | Error message shown |
| 5 | empty | valid | Error: username required |
| 6 | valid | empty | Error: password required |
| 7 | empty | empty | Error: username required |

#### Derived Test Cases

**TC_LOGIN_001 — Valid login with standard_user**

| Field | Value |
|-------|-------|
| ID | TC_LOGIN_001 |
| Title | Verify login with valid standard_user credentials displays products page |
| Objective | Verify that entering valid credentials (standard_user / secret_sauce) and tapping LOGIN redirects the user to the Products page. |
| Priority | High |
| Test Scope | Smoke Test |
| Automation Status | automated |
| Automation Dependency | A |

**Automation Decision Score:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Execution Frequency | 3 | Run every build (smoke test) |
| Test Stability | 3 | Deterministic — same credentials always work |
| Data-Driven Potential | 3 | Can parameterize with multiple user types |
| External Dependency | 3 | App-only, no external systems |
| Regression Risk | 3 | Login is critical path, any break is severe |
| Setup Complexity | 3 | Simple — just launch app |
| **Total** | **18** | **Automate immediately** |

---

**TC_LOGIN_003 — Login with locked_out_user**

| Field | Value |
|-------|-------|
| ID | TC_LOGIN_003 |
| Title | Verify login with locked_out_user displays locked out error message |
| Objective | Verify that entering locked_out_user credentials and tapping LOGIN displays the "locked out" error message without navigating away from the login screen. |
| Priority | Normal |
| Test Scope | Mandatory Regression Test |
| Automation Status | automated |
| Automation Dependency | A |

**Automation Decision Score:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Execution Frequency | 2 | Run every release (regression) |
| Test Stability | 3 | Deterministic — locked user always fails |
| Data-Driven Potential | 2 | Part of login parameterization |
| External Dependency | 3 | App-only |
| Regression Risk | 2 | Important but not critical path |
| Setup Complexity | 3 | Simple — just launch app |
| **Total** | **15** | **Automate immediately** |

---

### Feature: Shopping Cart

#### Technique Applied: State Transition

**States:**
- Empty Cart (badge not shown)
- Cart with Items (badge shows count)
- Checkout Started (info form displayed)

**Transitions:**

```
[Empty Cart] --add item--> [Cart with Items]
[Cart with Items] --remove all--> [Empty Cart]
[Cart with Items] --add more--> [Cart with Items] (badge increments)
[Cart with Items] --checkout--> [Checkout Started]
[Checkout Started] --cancel--> [Cart with Items]
```

**Derived Test Case Example:**

**TC_CART_001 — Add single product to cart**

| Field | Value |
|-------|-------|
| ID | TC_CART_001 |
| Title | Verify adding a product from catalog updates cart badge to 1 |
| Objective | Verify that tapping "Add to Cart" on a product in the catalog increments the cart badge counter from 0 to 1. |
| Priority | High |
| Test Scope | Smoke Test |
| Automation Status | automated |
| Automation Dependency | A |

**Automation Decision Score:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Execution Frequency | 3 | Run every build (smoke test) |
| Test Stability | 3 | Deterministic — add always works |
| Data-Driven Potential | 2 | Can test with different products |
| External Dependency | 3 | App-only |
| Regression Risk | 3 | Core e-commerce functionality |
| Setup Complexity | 2 | Requires login first |
| **Total** | **16** | **Automate immediately** |

---

### Feature: Checkout

#### Technique Applied: Boundary Value Analysis

**Input: Checkout Information Form**

| Field | Boundary Values |
|-------|----------------|
| First Name | empty, 1 char, typical (5-10 chars), very long (50+ chars) |
| Last Name | empty, 1 char, typical, very long |
| Zip Code | empty, 1 char, typical (5 digits), alphanumeric |

**Derived Test Case Example:**

**TC_CHECKOUT_005 — Checkout with missing required fields**

| Field | Value |
|-------|-------|
| ID | TC_CHECKOUT_005 |
| Title | Verify checkout form shows error when all fields are empty |
| Objective | Verify that tapping Continue on the checkout information form with all fields empty displays an error message indicating the first name is required. |
| Priority | High |
| Test Scope | Mandatory Regression Test |
| Automation Status | automated |
| Automation Dependency | A |

**Automation Decision Score:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Execution Frequency | 2 | Run every release |
| Test Stability | 3 | Deterministic — empty fields always fail |
| Data-Driven Potential | 3 | Multiple field combinations |
| External Dependency | 3 | App-only |
| Regression Risk | 2 | Important validation |
| Setup Complexity | 2 | Requires login + items in cart |
| **Total** | **15** | **Automate immediately** |

---

### Manual-Only Example

**TC_CATALOG_005 — Verify product images load correctly**

| Field | Value |
|-------|-------|
| ID | TC_CATALOG_005 |
| Title | Verify all product images display correctly without distortion |
| Objective | Verify that all product images on the catalog page load completely and display without cropping, stretching, or placeholder icons. |
| Priority | Low |
| Test Scope | Extended Regression Test |
| Automation Status | manual-only |
| Automation Dependency | A |

**Automation Decision Score:**

| Factor | Score | Rationale |
|--------|-------|-----------|
| Execution Frequency | 1 | Run quarterly (visual check) |
| Test Stability | 1 | Subjective — "correct" is visual judgment |
| Data-Driven Potential | 1 | Each image is unique |
| External Dependency | 3 | App-only |
| Regression Risk | 1 | Cosmetic, not functional |
| Setup Complexity | 2 | Requires login |
| **Total** | **9** | **Keep manual** |

**Justification:** Image quality assessment requires human visual judgment. Automated pixel comparison is brittle and produces false positives with minor rendering differences.

---

## Traceability Matrix

After designing all test cases, create a traceability matrix mapping features to test cases:

| Feature | Test Cases | High Priority | Automated | Planned | Manual-Only |
|---------|-----------|---------------|-----------|---------|-------------|
| Authentication | TC_LOGIN_001 – TC_LOGIN_005 | 2 | 4 | 0 | 1 |
| Product Catalog | TC_CATALOG_001 – TC_CATALOG_005 | 2 | 3 | 1 | 1 |
| Shopping Cart | TC_CART_001 – TC_CART_005 | 2 | 4 | 1 | 0 |
| Checkout | TC_CHECKOUT_001 – TC_CHECKOUT_005 | 2 | 4 | 0 | 1 |

This matrix confirms:
- Every in-scope feature has test coverage
- Each feature group has ≥ 2 High-priority test cases
- Automation decisions are documented and justified

---

## Deliverables Checklist

- [ ] Test design technique selected and documented for each feature
- [ ] Test scenarios derived from the chosen technique(s)
- [ ] Test cases written following the template format (all mandatory fields populated)
- [ ] Automation decision matrix applied to each test case with scores documented
- [ ] Automation dependency category (A, B, C, D) assigned to each test case
- [ ] At least 5 test cases per feature group (minimum 20 total)
- [ ] At least 2 High-priority test cases per feature group
- [ ] Traceability matrix showing feature-to-test-case mapping
- [ ] No duplicate scenarios across feature groups
- [ ] All test cases pass the quality checklist validation

---

## Tips and Common Pitfalls

- **Don't write tests for everything:** Focus on behaviors that matter. A test for "page loads" is less valuable than "login with locked user shows specific error"
- **One behavior per test case:** If your objective contains "and", split it into two test cases
- **Be specific in expected results:** "Error message appears" is not testable. "Error message 'Username is required' is displayed below the form" is testable
- **Score honestly:** Don't inflate automation scores to justify automating everything. Some tests genuinely belong as manual
- **Consider maintenance cost:** A test that's easy to automate but breaks every sprint may cost more than running it manually
- **Start with smoke tests:** Automate the critical path first, then expand to regression coverage
