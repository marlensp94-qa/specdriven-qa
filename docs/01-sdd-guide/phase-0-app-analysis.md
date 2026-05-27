# Phase 0: Application Analysis

## Objectives

- Understand the target application's purpose, architecture, and user base
- Identify all features, screens, and user flows
- Define the testing scope (what is in scope vs. out of scope)
- Produce a structured analysis document that serves as the foundation for all subsequent phases

## Prerequisites

- Access to the target application (installed on device/emulator or available as APK)
- Basic understanding of the application's domain (e-commerce in this case)
- A device or emulator to explore the application manually

## Inputs

- Application binary (APK/IPA) or access to the running application
- Any available product documentation, user stories, or feature specs
- Stakeholder input on priority areas (if available)

## Outputs

- Feature inventory with descriptions
- Screen catalog with navigation relationships
- End-to-end user flow diagrams
- Scope definition document (in/out of scope)
- Initial risk areas identified

---

## Step-by-Step Instructions

### Step 1: Install and Launch the Application

1. Obtain the application binary (for Swag Labs: download from Sauce Labs GitHub)
2. Install on your test device or emulator
3. Launch the application and observe the initial state
4. Note the entry point (login screen, onboarding, etc.)

### Step 2: Explore All Screens

Navigate through every reachable screen in the application. For each screen, document:

- Screen name (descriptive, consistent naming)
- Purpose (what the user accomplishes here)
- Key UI elements (buttons, inputs, lists, labels)
- Navigation paths (how to reach this screen, where it leads)

### Step 3: Identify Features

Group related functionality into features. A feature is a cohesive set of capabilities that delivers value to the user. For each feature, document:

- Feature name
- Description (1-2 sentences)
- Related screens
- User value proposition

### Step 4: Map User Flows

Identify end-to-end paths a user takes to accomplish goals. For each flow:

- Flow name
- Starting point
- Steps (screen-by-screen)
- End state
- Variations (happy path, error paths)

### Step 5: Define Scope

Determine what will and will not be tested. Consider:

- Core functionality vs. edge cases
- Platform constraints (Android only, emulator only)
- Integration boundaries (what's mocked vs. real)
- Time and resource constraints

---

## Worked Example: Swag Labs Mobile

### Application Overview

**App Name:** Swag Labs Mobile  
**Platform:** Android  
**Package:** `com.swaglabsmobileapp`  
**Source:** Sauce Labs public demo APK (GitHub)  
**Domain:** E-commerce (product catalog, cart, checkout)  
**Test Users:** `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`  
**Password:** `secret_sauce` (all users)

### Feature Inventory

| # | Feature | Description | Screens Involved | Priority |
|---|---------|-------------|------------------|----------|
| 1 | Authentication | User login/logout with credential validation | Login, Products (logout menu) | High |
| 2 | Product Catalog | Browse, sort, and view product details | Products, Product Detail | High |
| 3 | Shopping Cart | Add/remove items, view cart contents | Products, Product Detail, Cart | High |
| 4 | Checkout | Complete purchase with shipping info | Cart, Checkout Info, Checkout Overview, Checkout Complete | High |
| 5 | Product Sorting | Sort products by name (A-Z, Z-A) and price (low-high, high-low) | Products | Medium |

### Screen Catalog

#### Screen 1: Login Screen
- **Purpose:** Authenticate users before accessing the store
- **Key Elements:** Username field, Password field, Login button, Error message area
- **Navigation:** Entry point → Products (on success), stays on Login (on failure)
- **Accessibility IDs:** `test-Username`, `test-Password`, `test-LOGIN`

#### Screen 2: Products Screen
- **Purpose:** Display product catalog with sorting options
- **Key Elements:** Product list, Sort dropdown, Cart icon with badge, Hamburger menu
- **Navigation:** Login → Products; Products → Product Detail, Cart, Menu
- **Accessibility IDs:** `test-PRODUCTS`, `test-Modal Selector Button`, `test-Cart`

#### Screen 3: Product Detail Screen
- **Purpose:** Show detailed information about a single product
- **Key Elements:** Product image, Title, Description, Price, Add/Remove Cart button, Back button
- **Navigation:** Products → Product Detail → Products (back)
- **Accessibility IDs:** `test-Description`, `test-Price`, `test-ADD TO CART`

#### Screen 4: Cart Screen
- **Purpose:** Review items before checkout
- **Key Elements:** Cart items list, Remove buttons, Continue Shopping button, Checkout button
- **Navigation:** Products/Product Detail → Cart → Checkout Info, Products
- **Accessibility IDs:** `test-CHECKOUT`, `test-CONTINUE SHOPPING`

#### Screen 5: Checkout Information Screen
- **Purpose:** Collect shipping/billing information
- **Key Elements:** First Name field, Last Name field, Zip Code field, Continue button, Cancel button
- **Navigation:** Cart → Checkout Info → Checkout Overview, Cart (cancel)
- **Accessibility IDs:** `test-First Name`, `test-Last Name`, `test-Zip/Postal Code`, `test-CONTINUE`

#### Screen 6: Checkout Overview Screen
- **Purpose:** Review order summary before confirming
- **Key Elements:** Item list, Item total, Tax, Total price, Finish button, Cancel button
- **Navigation:** Checkout Info → Checkout Overview → Checkout Complete, Products (cancel)
- **Accessibility IDs:** `test-FINISH`, `test-CANCEL`

#### Screen 7: Checkout Complete Screen
- **Purpose:** Confirm successful order placement
- **Key Elements:** Confirmation message, Pony Express image, Back Home button
- **Navigation:** Checkout Overview → Checkout Complete → Products
- **Accessibility IDs:** `test-BACK HOME`, `test-CHECKOUT: COMPLETE!`

### End-to-End User Flows

#### Flow 1: Complete Purchase (Happy Path)

```
Login → Products → Product Detail → Add to Cart → Cart → 
Checkout Info → Checkout Overview → Checkout Complete → Products
```

**Steps:**
1. Enter valid credentials on Login screen
2. Tap a product from the catalog
3. Tap "Add to Cart" on Product Detail
4. Navigate to Cart
5. Tap "Checkout"
6. Fill in First Name, Last Name, Zip Code
7. Tap "Continue"
8. Review order on Overview screen
9. Tap "Finish"
10. Verify confirmation message on Complete screen

**Variations:**
- Add multiple products before checkout
- Add from Products screen directly (without going to detail)

#### Flow 2: Cart Management

```
Login → Products → Add Item(s) → Cart → Remove Item → Continue Shopping → Products
```

**Steps:**
1. Login with valid credentials
2. Add one or more products to cart
3. Navigate to Cart
4. Remove an item
5. Tap "Continue Shopping"
6. Verify return to Products screen

**Variations:**
- Remove all items (empty cart)
- Add same item multiple times (if supported)

#### Flow 3: Authentication Failure

```
Login (invalid credentials) → Error Message → Login (retry)
```

**Steps:**
1. Enter invalid username or password
2. Tap Login button
3. Observe error message
4. Verify user remains on Login screen

**Variations:**
- Empty username
- Empty password
- Both fields empty
- Locked out user (`locked_out_user`)

### Scope Definition

#### In Scope

| Area | Justification |
|------|---------------|
| Login with all test users | Core entry point, multiple user types available |
| Product catalog browsing | Primary feature, high user interaction |
| Product sorting (all options) | Verifiable UI behavior, data-driven |
| Add/remove cart items | Core e-commerce flow |
| Complete checkout flow | Critical business path |
| Error handling (invalid login, missing checkout info) | Negative testing for robustness |
| UI element presence and text verification | Basic functional validation |

#### Out of Scope

| Area | Justification |
|------|---------------|
| Performance testing | Requires specialized tools, not in training scope |
| Network failure simulation | Requires proxy setup, adds complexity |
| Multi-device parallel execution | Single emulator focus for simplicity |
| iOS platform | Android-only for this training project |
| Real payment processing | Demo app has no real backend |
| Accessibility compliance testing | Requires specialized tools (TalkBack audit) |
| Localization/i18n | App is English-only |

### Scope Criteria

The following criteria were used to determine scope boundaries:

1. **Testability:** Can the behavior be verified through the UI with assertions?
2. **Stability:** Is the feature stable enough to automate reliably?
3. **Value:** Does testing this feature provide meaningful coverage?
4. **Feasibility:** Can it be tested with our tools (Appium + emulator)?
5. **Independence:** Can the test run without external dependencies?

---

## Deliverables Checklist

- [ ] Feature inventory with at least 3 features identified and described
- [ ] Screen catalog with at least 5 screens documented (name, purpose, elements, navigation)
- [ ] At least 2 end-to-end user flows mapped with steps and variations
- [ ] Scope definition with in-scope and out-of-scope items justified
- [ ] Scope criteria documented (what rules determined the boundaries)
- [ ] Application overview (name, platform, package, domain, test users)

---

## Tips and Common Pitfalls

- **Don't skip exploration:** Spend real time clicking through the app before documenting
- **Be specific with locators:** Note accessibility IDs during exploration — you'll need them later
- **Document navigation relationships:** Knowing which screens connect saves time in flow design
- **Keep scope realistic:** It's better to thoroughly test 5 features than superficially test 15
- **Identify test users early:** Different user types often reveal different behaviors
