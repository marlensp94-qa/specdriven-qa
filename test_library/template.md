# Test Case Template

## Test Case ID
TC_[FEATURE]_[NUMBER]

## Title
[Short descriptive title — maximum 80 characters]

## Objective
Verify that [expected behavior or outcome being validated].

## Preconditions
- [Required setup condition 1]
- [Required setup condition 2]
- [Additional conditions as needed]

## Test Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | [First action to perform] | [Expected outcome of step 1] |
| 2 | [Second action to perform] | [Expected outcome of step 2] |
| 3 | [Third action to perform] | [Expected outcome of step 3] |

## Priority
[High | Normal | Low]

## Test Scope
[Mandatory Regression Test | Smoke Test | Extended Regression Test]

## Automation Status
[automated | planned | manual-only]

## Automation Dependency Category
[A | B | C | D]

---

### Field Reference

- **ID**: Format `TC_[FEATURE]_[NUMBER]` where FEATURE is the module name and NUMBER is zero-padded to 3 digits
- **Title**: Maximum 80 characters, concise description of what is tested
- **Objective**: Must start with "Verify that..." or "Ensure that..."
- **Preconditions**: Bullet list of all required setup conditions before execution
- **Test Steps**: Numbered sequentially, minimum 3 steps per test case
- **Expected Results**: One per step, specific and measurable
- **Priority**: High (critical path), Normal (standard coverage), Low (edge case)
- **Test Scope**: Smoke Test (critical path), Mandatory Regression Test (standard), Extended Regression Test (comprehensive)
- **Automation Status**: automated (has check script), planned (will be automated), manual-only (cannot be automated)
- **Automation Dependency Category**:
  - A — App-only, no external systems needed
  - B — External validation required
  - C — Hardware required
  - D — Precondition-dependent, requires specific state setup
