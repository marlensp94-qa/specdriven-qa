# Automation Plan and Coverage Gap Analysis

## Overview

This document defines the automation strategy for the Swag Labs Mobile test suite. It assigns each test case to a priority tier based on scored factors, identifies coverage gaps with technical constraints, and provides decision criteria for determining when to automate versus keep manual.

**Total Test Cases:** 23  
**Currently Automated:** 15  
**Planned for Automation:** 6  
**Manual-Only:** 2  
**Current Coverage Rate:** 65.2%

---

## 1. Priority Tier Definitions

| Tier | Label | Timeline | Criteria |
|------|-------|----------|----------|
| **P1** | Immediate | Current sprint | High frequency + High risk + High feasibility |
| **P2** | Next Sprint | 1–2 sprints | Medium-to-high frequency + Medium risk + Medium-to-high feasibility |
| **P3** | Backlog | 3+ sprints or deferred | Low frequency + Low risk OR Low feasibility |

---

## 2. Scoring Factors

Each test case is evaluated on three dimensions, each scored 1–3:

### 2.1 Execution Frequency

| Score | Label | Definition |
|-------|-------|------------|
| 3 | High | Executed every sprint (smoke, critical regression) |
| 2 | Medium | Executed every release cycle |
| 1 | Low | Executed quarterly or less (extended regression, exploratory) |

### 2.2 Risk Level

| Score | Label | Definition |
|-------|-------|------------|
| 3 | High | Failure blocks release; affects revenue or core user flow |
| 2 | Medium | Affects core flow but has workarounds; impacts user experience |
| 1 | Low | Edge case; cosmetic or non-critical path |

### 2.3 Automation Feasibility

| Score | Label | Definition |
|-------|-------|------------|
| 3 | High | Category A (app-only); straightforward element assertions |
| 2 | Medium | Category B or D; requires additional fixtures or external validation |
| 1 | Low | Category C (hardware required); requires visual/manual judgment |

### 2.4 Tier Assignment Rules

| Total Score (sum of 3 factors) | Assigned Tier |
|-------------------------------|---------------|
| 7–9 | P1 — Immediate |
| 5–6 | P2 — Next Sprint |
| 3–4 | P3 — Backlog |

---

## 3. Test Case Scoring Matrix

### 3.1 Login Test Cases

| Test Case ID | Title | Frequency | Risk | Feasibility | Total | Tier | Status |
|--------------|-------|-----------|------|-------------|-------|------|--------|
| TC_LOGIN_001 | Valid login with standard user credentials | 3 | 3 | 3 | 9 | P1 | automated |
| TC_LOGIN_002 | Login fails with invalid password | 3 | 3 | 3 | 9 | P1 | automated |
| TC_LOGIN_003 | Login fails for locked out user account | 3 | 2 | 3 | 8 | P1 | automated |
| TC_LOGIN_004 | Login fails when fields are empty | 2 | 2 | 3 | 7 | P1 | automated |
| TC_LOGIN_005 | User can log out and return to Login screen | 2 | 2 | 2 | 6 | P2 | planned |

### 3.2 Catalog Test Cases

| Test Case ID | Title | Frequency | Risk | Feasibility | Total | Tier | Status |
|--------------|-------|-----------|------|-------------|-------|------|--------|
| TC_CATALOG_001 | Verify product listing displays all items | 3 | 3 | 3 | 9 | P1 | automated |
| TC_CATALOG_002 | Verify sorting products by name A to Z | 2 | 2 | 3 | 7 | P1 | automated |
| TC_CATALOG_003 | Verify sorting products by price low to high | 2 | 2 | 3 | 7 | P1 | automated |
| TC_CATALOG_004 | Verify product detail page displays correct info | 2 | 2 | 3 | 7 | P1 | automated |
| TC_CATALOG_005 | Verify sorting products by name Z to A | 1 | 1 | 3 | 5 | P2 | planned |
| TC_CATALOG_006 | Verify sorting products by price high to low | 1 | 1 | 3 | 5 | P2 | planned |

### 3.3 Cart Test Cases

| Test Case ID | Title | Frequency | Risk | Feasibility | Total | Tier | Status |
|--------------|-------|-----------|------|-------------|-------|------|--------|
| TC_CART_001 | Verify adding a single product to the cart | 3 | 3 | 3 | 9 | P1 | automated |
| TC_CART_002 | Verify removing a product from the cart | 3 | 2 | 3 | 8 | P1 | automated |
| TC_CART_003 | Verify cart badge updates with multiple items | 2 | 2 | 3 | 7 | P1 | automated |
| TC_CART_004 | Verify continue shopping returns to products | 2 | 2 | 3 | 7 | P1 | automated |
| TC_CART_005 | Verify removing product from cart via Products page | 1 | 1 | 3 | 5 | P2 | automated |
| TC_CART_006 | Verify cart persists items after navigating away | 1 | 2 | 2 | 5 | P2 | planned |

### 3.4 Checkout Test Cases

| Test Case ID | Title | Frequency | Risk | Feasibility | Total | Tier | Status |
|--------------|-------|-----------|------|-------------|-------|------|--------|
| TC_CHECKOUT_001 | Complete checkout with valid shipping info | 3 | 3 | 3 | 9 | P1 | automated |
| TC_CHECKOUT_002 | Checkout fails when required fields are empty | 3 | 3 | 3 | 9 | P1 | automated |
| TC_CHECKOUT_003 | Cancel checkout returns user to Cart screen | 2 | 2 | 3 | 7 | P1 | automated |
| TC_CHECKOUT_004 | Checkout overview displays correct totals | 2 | 2 | 3 | 7 | P1 | planned |
| TC_CHECKOUT_005 | Order confirmation and return to products | 2 | 2 | 3 | 7 | P1 | planned |
| TC_CHECKOUT_006 | Continue shopping from cart navigates to catalog | 1 | 1 | 3 | 5 | P2 | automated |

---

## 4. Worked Examples (One Per Tier)

### 4.1 P1 Example: TC_LOGIN_001 — Valid login with standard user credentials

**Scoring Rationale:**

| Factor | Score | Justification |
|--------|-------|---------------|
| Execution Frequency | 3 (High) | Login is the gateway to all other tests; executed in every smoke run, every sprint |
| Risk Level | 3 (High) | If login fails, no other functionality is testable; blocks release |
| Automation Feasibility | 3 (High) | Category A — app-only, uses standard element assertions (text fields, button tap, page title verification) |

**Total Score:** 9 → **P1 (Immediate)**

**Decision:** Automate immediately. This test validates the most critical user flow, runs in every test cycle, and requires only basic UI interactions with no external dependencies. It was among the first tests automated in the framework.

---

### 4.2 P2 Example: TC_LOGIN_005 — User can log out and return to Login screen

**Scoring Rationale:**

| Factor | Score | Justification |
|--------|-------|---------------|
| Execution Frequency | 2 (Medium) | Logout is tested every release but not in every sprint's smoke run |
| Risk Level | 2 (Medium) | Logout failure affects session management but doesn't block core purchasing flow |
| Automation Feasibility | 2 (Medium) | Category D — requires authenticated state as precondition; needs side menu interaction (hamburger menu → LOGOUT) which adds complexity |

**Total Score:** 6 → **P2 (Next Sprint)**

**Decision:** Plan for automation in the next sprint. The test requires an `ensure_logged_in` fixture and side menu navigation that isn't covered by existing page objects. Once the side menu interaction is added to the page object layer, this becomes straightforward to automate.

---

### 4.3 P3 Example: TC_CATALOG_005 (hypothetical manual-only scenario)

> Note: In the current library, no test cases score low enough for P3 because all are Category A or D. This worked example illustrates how a Category B/C test case would be evaluated.

**Hypothetical Test Case:** "Verify product images render correctly with proper resolution"

**Scoring Rationale:**

| Factor | Score | Justification |
|--------|-------|---------------|
| Execution Frequency | 1 (Low) | Visual validation is performed quarterly during major UI updates |
| Risk Level | 1 (Low) | Image rendering issues are cosmetic; do not block functionality |
| Automation Feasibility | 1 (Low) | Category B — requires visual comparison tooling (e.g., Applitools, Percy) not included in the current framework; element presence alone cannot validate image correctness |

**Total Score:** 3 → **P3 (Backlog)**

**Decision:** Keep manual. The cost of integrating visual comparison tooling exceeds the benefit given the low execution frequency and low risk. Revisit if the framework adds image comparison capabilities or if visual regressions become a recurring issue.

---

## 5. Coverage Gap Analysis

### 5.1 Unautomated Test Cases

The following test cases do not have a corresponding automated check script:

| Test Case ID | Title | Dependency | Technical Constraint | Target Tier |
|--------------|-------|------------|---------------------|-------------|
| TC_LOGIN_005 | User can log out and return to Login screen | D | Requires side menu page object and authenticated state fixture; hamburger menu interaction not yet implemented | P2 |
| TC_CATALOG_005 | Verify sorting products by name Z to A | A | No technical constraint; deferred due to lower priority (Z-A sort is inverse of existing A-Z test) | P2 |
| TC_CATALOG_006 | Verify sorting products by price high to low | A | No technical constraint; deferred due to lower priority (high-to-low is inverse of existing low-to-high test) | P2 |
| TC_CART_006 | Verify cart persists items after navigating away | D | Requires multi-screen navigation state verification; needs enhanced fixture for cart pre-population and navigation tracking | P2 |
| TC_CHECKOUT_004 | Checkout overview displays correct totals | A | No technical constraint; requires price parsing and arithmetic validation logic in assertions | P2 |
| TC_CHECKOUT_005 | Order confirmation and return to products | A | No technical constraint; requires CheckoutCompletePage assertions not yet exercised in existing tests | P2 |

### 5.2 Manual-Only Test Cases (No Automation Planned)

Based on the coverage analysis document, the following test cases from the original 21-case analysis are designated manual-only:

| Test Case ID | Title | Dependency | Technical Constraint | Justification |
|--------------|-------|------------|---------------------|---------------|
| TC_CATALOG_005* | Verify product images load correctly | B | Requires visual validation of image rendering; element presence assertions cannot verify image content, resolution, or correct rendering | Visual comparison tooling (Applitools, Percy) not in scope for current framework |
| TC_CART_005* | Verify cart persists after navigating away and returning | D | Complex multi-screen navigation state verification; requires specific precondition setup across multiple page transitions | Better validated through exploratory testing; automation ROI is low given complexity |

> *Note: The coverage_analysis.md references a different mapping for TC_CATALOG_005 and TC_CART_005 than the actual test case files. The gap analysis above reflects both the coverage_analysis.md designations and the actual test case file contents.*

---

## 6. Decision Criteria: Automate vs. Keep Manual

### 6.1 Decision Flowchart (Rule Set)

```
START: Evaluate test case for automation
│
├─ Q1: What is the Automation Dependency Category?
│   ├─ Category C (hardware required) ──────────────────────► KEEP MANUAL
│   │   Reason: Hardware dependencies cannot be satisfied in emulator-only CI
│   │
│   ├─ Category B (external validation required)
│   │   ├─ Q2: Is the external tool available in the framework?
│   │   │   ├─ Yes ──► Continue to Q4
│   │   │   └─ No ───► Q3: Is the tool planned for integration?
│   │   │       ├─ Yes ──► PLAN FOR AUTOMATION (P3)
│   │   │       └─ No ───► KEEP MANUAL
│   │   │
│   ├─ Category D (precondition-dependent)
│   │   ├─ Q4: Can the precondition be set up via existing fixtures?
│   │   │   ├─ Yes ──► Continue to Q5
│   │   │   └─ No ───► Q4b: Can a new fixture be created in ≤1 sprint?
│   │   │       ├─ Yes ──► PLAN FOR AUTOMATION (P2)
│   │   │       └─ No ───► KEEP MANUAL
│   │   │
│   └─ Category A (app-only) ──► Continue to Q5
│
├─ Q5: What is the Execution Frequency?
│   ├─ High (every sprint) ──► AUTOMATE (P1)
│   ├─ Medium (every release)
│   │   ├─ Q6: What is the Risk Level?
│   │   │   ├─ High (blocks release) ──► AUTOMATE (P1)
│   │   │   ├─ Medium (affects core flow) ──► AUTOMATE (P1 or P2)
│   │   │   └─ Low (edge case) ──► PLAN FOR AUTOMATION (P2)
│   │   │
│   └─ Low (quarterly or less)
│       ├─ Q7: What is the Risk Level?
│       │   ├─ High ──► AUTOMATE (P2)
│       │   ├─ Medium ──► PLAN FOR AUTOMATION (P2 or P3)
│       │   └─ Low ──► EVALUATE ROI
│       │       ├─ Automation effort < 30 min ──► PLAN FOR AUTOMATION (P3)
│       │       └─ Automation effort > 30 min ──► KEEP MANUAL
│
└─ END
```

### 6.2 Decision Summary Table

| Condition | Recommendation |
|-----------|---------------|
| Category A + High frequency + Any risk | Automate immediately (P1) |
| Category A + Medium frequency + High/Medium risk | Automate (P1) |
| Category A + Medium frequency + Low risk | Plan for automation (P2) |
| Category A + Low frequency + Low risk | Evaluate ROI; likely P3 or manual |
| Category D + Fixture achievable in 1 sprint | Plan for automation (P2) |
| Category D + Fixture requires significant effort | Keep manual |
| Category B + Tool available | Treat as Category A |
| Category B + Tool not available | Keep manual or P3 if tool is planned |
| Category C | Keep manual |

---

## 7. Automation Dependency Categorization

### 7.1 Category Definitions

| Category | Description | Automation Approach |
|----------|-------------|---------------------|
| **A** | App-only — all validation through UI element assertions | Direct automation with page objects and standard assertions |
| **B** | External validation required — needs tools beyond element assertions | Requires additional tooling (visual comparison, API mocking, network inspection) |
| **C** | Hardware required — needs physical device capabilities | Cannot automate in emulator-only environment; requires real device farm |
| **D** | Precondition-dependent — requires specific application state setup | Automatable with enhanced fixtures and state management |

### 7.2 Category Distribution

| Category | Count | Percentage | Test Case IDs |
|----------|-------|------------|---------------|
| **A** | 20 | 87.0% | TC_LOGIN_001, TC_LOGIN_002, TC_LOGIN_003, TC_LOGIN_004, TC_CATALOG_001, TC_CATALOG_002, TC_CATALOG_003, TC_CATALOG_004, TC_CATALOG_005, TC_CATALOG_006, TC_CART_001, TC_CART_002, TC_CART_003, TC_CART_004, TC_CART_005, TC_CHECKOUT_001, TC_CHECKOUT_002, TC_CHECKOUT_003, TC_CHECKOUT_004, TC_CHECKOUT_005 |
| **B** | 0 | 0.0% | — |
| **C** | 0 | 0.0% | — |
| **D** | 3 | 13.0% | TC_LOGIN_005, TC_CART_006, TC_CHECKOUT_006 |

> **Note:** The original coverage_analysis.md references 1 Category B test case (image validation) and 2 Category D cases. The actual test case files show TC_CATALOG_005 as Category A (sort Z-A) and TC_CART_005 as Category A (remove via Products page). The counts above reflect the actual test case file contents. The coverage_analysis.md gap entries for visual validation and cart persistence refer to scenarios not represented as standalone test case files.

### 7.3 Automation Potential

| Metric | Value |
|--------|-------|
| Total automatable (Category A + D with feasible fixtures) | 23 (100%) |
| Currently automated | 15 (65.2%) |
| Planned for next sprint (P2) | 6 (26.1%) |
| Projected coverage after P2 completion | 21 (91.3%) |
| Remaining manual-only (per coverage_analysis.md) | 2 (8.7%) |

---

## 8. Automation Roadmap

### Sprint 1 (Current) — P1 Complete

All P1 test cases are automated:
- 4 Login tests (TC_LOGIN_001–004)
- 4 Catalog tests (TC_CATALOG_001–004)
- 4 Cart tests (TC_CART_001–004)
- 3 Checkout tests (TC_CHECKOUT_001–003)

### Sprint 2 (Next) — P2 Targets

| Test Case ID | Effort Estimate | Prerequisite |
|--------------|-----------------|--------------|
| TC_CATALOG_005 | Low (< 30 min) | Reuse existing sort test pattern with Z-A option |
| TC_CATALOG_006 | Low (< 30 min) | Reuse existing sort test pattern with price high-to-low option |
| TC_CHECKOUT_004 | Medium (30–60 min) | Add price parsing utility; verify arithmetic in assertions |
| TC_CHECKOUT_005 | Low (< 30 min) | Add assertions to CheckoutCompletePage; verify "Back Home" navigation |
| TC_LOGIN_005 | Medium (30–60 min) | Implement side menu interaction in page object layer |
| TC_CART_006 | Medium (30–60 min) | Create cart pre-population fixture; add navigation state tracking |

### Sprint 3+ (Backlog) — P3 / Manual-Only

- Integrate visual comparison tooling if image validation becomes a priority
- Evaluate real-device testing needs if hardware-dependent scenarios are added
- Reassess manual-only cases quarterly based on defect trends

---

## 9. Maintenance and Review

- **Review cadence:** Re-score test cases at the start of each quarter
- **Trigger for re-evaluation:** New test cases added, framework capabilities expanded, or defect patterns change
- **Graduation criteria:** A planned test case moves to automated when its check script passes in CI
- **Deprecation criteria:** A test case moves to Deprecated when the feature it validates is removed from the application

---

## References

- [Test Library Coverage Analysis](../../test_library/coverage_analysis.md)
- [Quality Standards](../standards/quality-checklist.md)
- [SDD Guide — Phase 2: Test Case Design](../01-sdd-guide/phase-2-test-case-design.md)
