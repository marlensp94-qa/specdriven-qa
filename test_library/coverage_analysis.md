# Test Coverage Analysis

## Overview

This document maps each manual test case in the Test Library to its corresponding automated check script, states the automation status, and provides justification for any gaps where no automated test exists.

---

## Coverage Summary

| Metric | Count |
|--------|-------|
| Total Manual Test Cases | 21 |
| Automated | 13 |
| Planned | 6 |
| Manual-Only | 2 |
| Coverage Rate | 61.9% |

---

## Automation Dependency Categories

| Category | Description | Count |
|----------|-------------|-------|
| A | App-only, no external systems needed | 18 |
| B | External validation required | 1 |
| C | Hardware required | 0 |
| D | Precondition-dependent, requires specific state setup | 2 |

---

## Login Test Cases

| Test Case ID | Title | Check Script | Status | Gap Justification |
|--------------|-------|--------------|--------|-------------------|
| TC_LOGIN_001 | Login with valid credentials | check_T001_login_valid_credentials | automated | — |
| TC_LOGIN_002 | Login with invalid password | check_T002_login_invalid_credentials | automated | — |
| TC_LOGIN_003 | Login with empty username and password fields | check_T003_login_empty_fields | automated | — |
| TC_LOGIN_004 | Login with locked out user account | — | planned | Category A; will be automated in next sprint as negative test expansion |
| TC_LOGIN_005 | Logout from the application | — | planned | Category D; requires authenticated state setup, planned for P2 tier |

---

## Catalog Test Cases

| Test Case ID | Title | Check Script | Status | Gap Justification |
|--------------|-------|--------------|--------|-------------------|
| TC_CATALOG_001 | Browse product catalog and verify product listing | check_T004_catalog_browsing | automated | — |
| TC_CATALOG_002 | View product detail from catalog | check_T006_product_detail_view | automated | — |
| TC_CATALOG_003 | Sort products alphabetically A to Z | check_T008_sort_products_az | automated | — |
| TC_CATALOG_004 | Sort products by price low to high | check_T009_sort_products_price | automated | — |
| TC_CATALOG_005 | Verify product images load correctly | — | manual-only | Category B; requires visual validation of image rendering not feasible with element assertions alone |

---

## Cart Test Cases

| Test Case ID | Title | Check Script | Status | Gap Justification |
|--------------|-------|--------------|--------|-------------------|
| TC_CART_001 | Add product to cart from catalog | check_T005_add_product_to_cart | automated | — |
| TC_CART_002 | Remove product from cart | check_T007_remove_from_cart | automated | — |
| TC_CART_003 | Continue shopping from cart returns to products | check_T012_continue_shopping | automated | — |
| TC_CART_004 | Add multiple products and verify cart badge count | — | planned | Category A; planned for P2 tier as cart badge validation enhancement |
| TC_CART_005 | Verify cart persists after navigating away and returning | — | manual-only | Category D; requires complex navigation state verification across multiple screens |

---

## Checkout Test Cases

| Test Case ID | Title | Check Script | Status | Gap Justification |
|--------------|-------|--------------|--------|-------------------|
| TC_CHECKOUT_001 | Complete checkout with valid shipping information | check_T010_complete_checkout | automated | — |
| TC_CHECKOUT_002 | Checkout fails when required shipping fields are empty | check_T013_checkout_missing_info | automated | — |
| TC_CHECKOUT_003 | Cancel checkout returns user to the Cart screen | check_T011_checkout_cancel | automated | — |
| TC_CHECKOUT_004 | Checkout overview displays correct item total, tax, and grand total | — | planned | Category A; planned for P2 tier as pricing validation enhancement |
| TC_CHECKOUT_005 | Order confirmation screen displays success and allows return | — | planned | Category A; planned for P2 tier as post-checkout flow validation |
| TC_CHECKOUT_006 | Continue shopping from cart navigates back to products catalog | check_T012_continue_shopping | automated | — |

---

## Gap Analysis Summary

### Planned Automation (P2 Tier)

| Test Case ID | Reason for Delay | Target |
|--------------|------------------|--------|
| TC_LOGIN_004 | Negative test expansion — locked user scenario | Next sprint |
| TC_LOGIN_005 | Requires authenticated state setup (Category D) | Next sprint |
| TC_CART_004 | Cart badge count validation across multiple items | Next sprint |
| TC_CHECKOUT_004 | Pricing calculation verification on overview screen | Next sprint |
| TC_CHECKOUT_005 | Post-checkout confirmation and navigation flow | Next sprint |

### Manual-Only Justification

| Test Case ID | Technical Constraint |
|--------------|---------------------|
| TC_CATALOG_005 | Visual validation of image rendering requires human judgment or image comparison tools not included in the current framework (Category B) |
| TC_CART_005 | Complex multi-screen navigation state persistence requires specific precondition setup and is better validated through exploratory testing (Category D) |

---

## Notes

- Coverage rate is calculated as: (automated count / total count) × 100
- All Category A test cases are candidates for automation
- Category B and C test cases require additional tooling or hardware not available in the current emulator-only setup
- Category D test cases may be automated with additional fixture support in future sprints
- Check script naming follows the pattern: `check_T{number}_{description}.py`
