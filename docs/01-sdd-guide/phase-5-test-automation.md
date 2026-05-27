# Phase 5: Test Automation

## Objectives

By the end of this phase you will:

- Write automated check scripts that map to manual test cases from the Test Library
- Implement reusable test flows for common multi-step operations
- Apply the pytest marker system for test classification and traceability
- Structure tests using the Page Object Model with no direct driver calls in test code
- Compose flows to build complex end-to-end scenarios from simple building blocks

## Prerequisites

Before starting Phase 5, ensure you have completed:

- [ ] Phase 0 — App Analysis (screens and flows identified)
- [ ] Phase 1 — Test Planning (scope and automation strategy defined)
- [ ] Phase 2 — Test Case Design (manual test cases written)
- [ ] Phase 3 — Test Library Management (test cases organized and reviewed)
- [ ] Phase 4 — Automation Framework Setup (BasePage, ConfigLoader, EmulatorManager, Locator Store all implemented)
- [ ] All page objects implemented and referencing the Locator Store
- [ ] `conftest.py` with driver fixture and `ensure_logged_in` fixture ready
- [ ] pytest.ini configured with marker registrations and test discovery patterns

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Manual test cases | `test_library/` (Phase 2-3) | Define what to automate and expected behavior |
| Page objects | `framework/pages/` (Phase 4) | Provide screen interaction methods |
| Locator Store | `framework/pages/locators.py` (Phase 4) | Element identification |
| Marker system | `framework/utils/markers.py` (Phase 4) | Test classification |
| Constants | `framework/utils/constants.py` (Phase 4) | Credentials, timeouts, identifiers |
| Coverage analysis | `test_library/coverage_analysis.md` (Phase 3) | Prioritize which tests to automate first |

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Smoke check scripts | `tests/check_scripts/check_T001_*.py` etc. | Critical-path automated tests |
| Regression check scripts | `tests/check_scripts/check_T002_*.py` etc. | Full regression automated tests |
| Reusable flows | `tests/flows/` | Composable multi-step operations |
| Flow documentation | Inline docstrings + examples | How to compose flows |

---

## Step-by-Step Instructions

### Step 1: Understand the Naming Convention

All automated test files and functions follow a strict naming convention that links them to manual test cases:

**File naming:** `check_T{number}_{description}.py`  
**Function naming:** `check_T{number}_{description}`

Rules:
- `{number}` is a positive integer matching a test case ID from the Test Library
- `{description}` contains only lowercase letters, digits, and underscores
- Maximum length of `{description}` is 60 characters

Examples:
```
✓ check_T001_login_valid_credentials.py
✓ check_T005_add_product_to_cart.py
✓ check_T010_complete_checkout.py
✗ check_T001_Login_Valid.py          (uppercase not allowed)
✗ check_login_valid.py               (missing T{number} prefix)
✗ check_T001_login-valid.py          (hyphens not allowed)
```

### Step 2: Structure a Check Script

Every check script follows this structure:

```python
"""
Check Script: check_T{number}_{description}
Maps to: TC_{FEATURE}_{number} from test_library/

Preconditions:
- List all required setup conditions

Steps:
1. Step description
2. Step description
3. Step description

Expected Results:
- What should be true after execution
"""
import pytest
from framework.utils.markers import component, test_type, priority, domain


@pytest.mark.smoke  # or @pytest.mark.regression
@component("feature-name")
@test_type("functional")
@priority("critical")
@domain("authentication")
def check_T001_login_valid_credentials(driver, ensure_logged_in):
    """Verify successful login with standard_user credentials."""
    # Test implementation using page objects only
    ...
```

Key rules:
1. **No direct driver calls** — Use page objects for all interactions
2. **At least one assertion** — Every test must validate an expected outcome
3. **Independent execution** — No test depends on another test's execution order
4. **Docstring required** — Include preconditions, steps, and expected results
5. **Markers required** — At minimum `component` and `priority`; plus `smoke` or `regression`

### Step 3: Implement Smoke Tests

Smoke tests cover the critical path — the minimum set of tests that confirm the application's core functionality works. These run first and must all pass before regression testing begins.

**Criteria for smoke tests:**
- Tests the most critical user journey
- Failure would block all other testing
- Covers the "happy path" of core features
- Typically 3-5 tests for a small application

For Swag Labs, the smoke tests are:

| Test | Flow | Why Smoke? |
|------|------|-----------|
| `check_T001_login_valid_credentials` | Login → Products | Can't test anything without login |
| `check_T005_add_product_to_cart` | Products → Add → Cart badge | Core e-commerce action |
| `check_T010_complete_checkout` | Full checkout flow | Primary business value |

Example smoke test implementation:

```python
import pytest
from framework.pages.login_page import LoginPage
from framework.pages.locators import ProductsLocators
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD
from framework.utils.markers import component, test_type, priority, domain


@pytest.mark.smoke
@component("authentication")
@test_type("smoke")
@priority("critical")
@domain("login")
def check_T001_login_valid_credentials(driver):
    """Verify successful login with standard_user credentials.

    Preconditions:
    - App is launched and Login screen is displayed
    - standard_user account is active

    Steps:
    1. Enter 'standard_user' in the username field
    2. Enter 'secret_sauce' in the password field
    3. Tap the Login button

    Expected Results:
    - Products screen is displayed
    - Products title is visible
    """
    login_page = LoginPage(driver)
    products_page = login_page.login(TEST_USER_STANDARD, TEST_PASSWORD)
    assert products_page.is_displayed(ProductsLocators.TITLE), \
        "Products screen should be displayed after successful login"
```

### Step 4: Implement Regression Tests

Regression tests cover the broader feature set. They verify that existing functionality continues to work as changes are made.

**Criteria for regression tests:**
- Covers all features in scope
- Includes negative scenarios (invalid inputs, error handling)
- Tests boundary conditions
- Verifies sorting, filtering, and data display

Example regression test:

```python
import pytest
from framework.pages.login_page import LoginPage
from framework.pages.locators import LoginLocators
from framework.utils.constants import TEST_USER_LOCKED, TEST_PASSWORD
from framework.utils.markers import component, test_type, priority, domain


@pytest.mark.regression
@component("authentication")
@test_type("negative")
@priority("high")
@domain("login")
def check_T002_login_invalid_credentials(driver):
    """Verify error message for locked_out_user login attempt.

    Preconditions:
    - App is launched and Login screen is displayed
    - locked_out_user account exists

    Steps:
    1. Enter 'locked_out_user' in the username field
    2. Enter 'secret_sauce' in the password field
    3. Tap the Login button

    Expected Results:
    - Error message is displayed
    - User remains on Login screen
    - Error text contains 'locked out'
    """
    login_page = LoginPage(driver)
    login_page.type_text(LoginLocators.USERNAME_FIELD, TEST_USER_LOCKED)
    login_page.type_text(LoginLocators.PASSWORD_FIELD, TEST_PASSWORD)
    login_page.tap(LoginLocators.LOGIN_BUTTON)

    assert login_page.is_displayed(LoginLocators.ERROR_MESSAGE), \
        "Error message should be displayed for locked_out_user"
    error_text = login_page.get_text(LoginLocators.ERROR_MESSAGE)
    assert "locked out" in error_text.lower(), \
        f"Error should mention 'locked out', got: {error_text}"
```

### Step 5: Implement Reusable Test Flows

Flows encapsulate multi-step operations that are used across multiple tests. They reduce code duplication and make tests more readable.

**Flow design principles:**
1. Each flow uses page objects internally
2. Each flow returns the resulting page object for chaining
3. All string parameters are validated (no None, empty, or whitespace-only)
4. Failed page transitions raise `PageNotLoadedError`

**Available flows:**

| Flow | Signature | Returns |
|------|-----------|---------|
| `login_flow` | `(driver, username, password)` | `ProductsPage` |
| `add_product_to_cart_flow` | `(driver, product_name)` | `CartPage` |
| `complete_checkout_flow` | `(driver, first_name, last_name, zip_code)` | `CheckoutCompletePage` |

Implementation pattern:

```python
# tests/flows/login_flow.py
from framework.pages.login_page import LoginPage
from framework.pages.base_page import PageNotLoadedError


def login_flow(driver, username: str, password: str):
    """Execute login and return ProductsPage.

    Args:
        driver: Appium WebDriver instance.
        username: Login username (non-empty string).
        password: Login password (non-empty string).

    Returns:
        ProductsPage instance after successful login.

    Raises:
        ValueError: If username or password is None, empty, or whitespace-only.
        PageNotLoadedError: If ProductsPage doesn't load after login.
    """
    if not username or not username.strip():
        raise ValueError("username must not be None, empty, or whitespace-only")
    if not password or not password.strip():
        raise ValueError("password must not be None, empty, or whitespace-only")

    login_page = LoginPage(driver)
    products_page = login_page.login(username, password)
    return products_page
```

### Step 6: Compose Flows in Tests

The real power of flows emerges when you chain them together. A complex end-to-end test becomes a sequence of readable flow calls:

```python
@pytest.mark.smoke
@component("checkout")
@test_type("functional")
@priority("critical")
@domain("e-commerce")
def check_T010_complete_checkout(driver):
    """Verify complete purchase flow from login to order confirmation.

    Preconditions:
    - App is launched and Login screen is displayed
    - standard_user account is active
    - At least one product is available in catalog

    Steps:
    1. Login with valid credentials
    2. Add 'Sauce Labs Backpack' to cart
    3. Complete checkout with valid shipping info

    Expected Results:
    - Checkout Complete screen is displayed
    - Confirmation message is visible
    """
    from tests.flows import login_flow, add_product_to_cart_flow, complete_checkout_flow

    # Chain flows together
    products_page = login_flow(driver, "standard_user", "secret_sauce")
    cart_page = add_product_to_cart_flow(driver, "Sauce Labs Backpack")
    complete_page = complete_checkout_flow(driver, "John", "Doe", "12345")

    assert complete_page.is_displayed(CheckoutCompleteLocators.COMPLETE_HEADER), \
        "Checkout Complete screen should be displayed"
```

### Step 7: Apply Markers Correctly

Every test must have the correct markers for classification and reporting:

| Marker | Required? | Purpose | Valid Values |
|--------|-----------|---------|--------------|
| `smoke` / `regression` | At least one | Execution scope | — |
| `component` | Yes | Jira component traceability | Any string |
| `priority` | Yes | Execution priority | critical, high, medium, low |
| `test_type` | Recommended | Test classification | functional, smoke, negative, boundary, integration |
| `domain` | Recommended | Organizational grouping | Any string |

**Running tests by marker:**

```bash
# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression

# Run tests for a specific component
pytest -m "component('authentication')"

# Run critical priority tests
pytest -m "priority('critical')"

# Combine markers
pytest -m "smoke and priority('critical')"
```

---

## Worked Example: Building the Cart Test Suite

This example walks through creating the complete cart test suite, from identifying test cases to implementing check scripts with flows.

### 1. Identify Test Cases to Automate

From `test_library/cart/`:

| Test Case ID | Title | Priority | Automation |
|-------------|-------|----------|------------|
| TC_CART_001 | Add single product to cart | High | Automated |
| TC_CART_002 | Remove product from cart | High | Automated |
| TC_CART_003 | Cart badge updates on add | Normal | Automated |
| TC_CART_004 | Continue shopping from cart | Normal | Automated |
| TC_CART_005 | Proceed to checkout from cart | High | Automated |

### 2. Create the Flow

```python
# tests/flows/cart_flow.py
from framework.pages.products_page import ProductsPage
from framework.pages.locators import ProductsLocators


def add_product_to_cart_flow(driver, product_name: str):
    """Add a product by name and navigate to cart.

    Args:
        driver: Appium WebDriver instance.
        product_name: Name of the product to add (non-empty string).

    Returns:
        CartPage instance after navigating to cart.

    Raises:
        ValueError: If product_name is None, empty, or whitespace-only.
        PageNotLoadedError: If expected page transition fails.
    """
    if not product_name or not product_name.strip():
        raise ValueError("product_name must not be None, empty, or whitespace-only")

    products_page = ProductsPage(driver)
    product_detail = products_page.open_product(product_name)
    product_detail.add_to_cart()
    product_detail.go_back()

    products_page = ProductsPage(driver)
    cart_page = products_page.open_cart()
    return cart_page
```

### 3. Write the Check Scripts

```python
# tests/check_scripts/check_T005_add_product_to_cart.py
import pytest
from tests.flows import login_flow, add_product_to_cart_flow
from framework.pages.locators import CartLocators
from framework.utils.markers import component, test_type, priority, domain


@pytest.mark.smoke
@component("cart")
@test_type("functional")
@priority("critical")
@domain("shopping")
def check_T005_add_product_to_cart(driver):
    """Verify adding a product to cart shows it in cart screen.

    Preconditions:
    - App launched, Login screen displayed
    - standard_user account active
    - 'Sauce Labs Backpack' available in catalog

    Steps:
    1. Login with valid credentials
    2. Open 'Sauce Labs Backpack' product
    3. Tap 'Add to Cart'
    4. Navigate to Cart

    Expected Results:
    - Cart screen displays the added product
    - Product name matches 'Sauce Labs Backpack'
    """
    login_flow(driver, "standard_user", "secret_sauce")
    cart_page = add_product_to_cart_flow(driver, "Sauce Labs Backpack")

    assert cart_page.is_displayed(CartLocators.CART_ITEM), \
        "Cart should contain at least one item"
```

```python
# tests/check_scripts/check_T007_remove_from_cart.py
import pytest
from tests.flows import login_flow, add_product_to_cart_flow
from framework.pages.locators import CartLocators
from framework.utils.markers import component, test_type, priority, domain


@pytest.mark.regression
@component("cart")
@test_type("functional")
@priority("high")
@domain("shopping")
def check_T007_remove_from_cart(driver):
    """Verify removing a product from cart removes it from the list.

    Preconditions:
    - App launched, user logged in
    - At least one product in cart

    Steps:
    1. Login with valid credentials
    2. Add 'Sauce Labs Backpack' to cart
    3. On Cart screen, tap Remove for the item
    4. Verify cart is empty

    Expected Results:
    - Product is removed from cart
    - Cart shows no items
    """
    login_flow(driver, "standard_user", "secret_sauce")
    cart_page = add_product_to_cart_flow(driver, "Sauce Labs Backpack")

    cart_page.remove_item("Sauce Labs Backpack")

    assert not cart_page.is_displayed(CartLocators.CART_ITEM), \
        "Cart should be empty after removing the only item"
```

### 4. Verify Marker Coverage

After writing all cart tests, verify each has the required markers:

| Test | smoke/regression | component | priority | test_type |
|------|-----------------|-----------|----------|-----------|
| check_T005 | ✓ smoke | ✓ cart | ✓ critical | ✓ functional |
| check_T007 | ✓ regression | ✓ cart | ✓ high | ✓ functional |
| check_T012 | ✓ regression | ✓ cart | ✓ medium | ✓ functional |

---

## Deliverables Checklist

- [ ] At least 3 smoke check scripts implemented (`check_T001_*`, `check_T005_*`, `check_T010_*`)
- [ ] At least 10 regression check scripts implemented
- [ ] All check scripts follow `check_T{number}_{description}` naming convention
- [ ] All check scripts include docstrings with preconditions, steps, expected results
- [ ] All check scripts use page objects only (no direct driver calls)
- [ ] All check scripts have at least one explicit assertion
- [ ] All check scripts decorated with `component` and `priority` markers
- [ ] All check scripts decorated with either `smoke` or `regression` marker
- [ ] Reusable flows implemented: `login_flow`, `add_product_to_cart_flow`, `complete_checkout_flow`
- [ ] All flow functions validate string parameters (reject None, empty, whitespace)
- [ ] All flow functions return page object instances for chaining
- [ ] At least 2 tests demonstrate flow composition (chaining 2+ flows)
- [ ] Each test is independently executable (no order dependency)

---

## Tips and Common Pitfalls

- **Don't put assertions in page objects:** Page objects describe what the page can do, not what should be true. Assertions belong in test functions.
- **Don't chain too many flows in one test:** If a test chains 5+ flows, it's testing too much. Split into focused tests.
- **Use descriptive assertion messages:** `assert condition, "Expected X but got Y"` makes failures self-explanatory.
- **Keep tests independent:** Never rely on another test having run first. Use fixtures for setup.
- **Match test case IDs exactly:** The `T{number}` in your check script must correspond to a real test case in the library.
- **Validate flow parameters early:** Catching None/empty at the flow entry point gives clearer errors than a cryptic Appium exception later.
- **Don't over-use ensure_logged_in:** For login tests themselves, you need to start from the login screen — don't use the fixture that skips login.
