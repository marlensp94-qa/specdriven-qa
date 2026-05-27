# Phase 4: Automation Framework Setup

## Objectives

By the end of this phase you will:

- Understand the architecture of the Mini_Framework and how its components interact
- Set up the Page Object Model (POM) pattern with a reusable BasePage class
- Implement configuration management using YAML files and environment variable overrides
- Create the Emulator Manager for Appium session lifecycle
- Establish the logging and constants infrastructure

## Prerequisites

Before starting Phase 4, ensure you have completed:

- [ ] Phase 0 — App Analysis (identified screens, features, and flows)
- [ ] Phase 1 — Test Planning (scope, approach, entry/exit criteria defined)
- [ ] Phase 2 — Test Case Design (manual test cases written)
- [ ] Phase 3 — Test Library Management (test cases organized and reviewed)
- [ ] Python 3.8+ installed and virtual environment created
- [ ] Appium 2.x installed with UiAutomator2 driver
- [ ] Android Studio with emulator configured (API 29+)

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| App analysis document | Phase 0 | Identifies screens needing page objects |
| Test plan | Phase 1 | Defines scope of automation |
| Swag Labs APK | Sauce Labs GitHub | Target application |
| Emulator configuration | Android Studio | Device capabilities |

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| BasePage class | `framework/pages/base_page.py` | Abstract base with common methods |
| ConfigLoader | `framework/core/config_loader.py` | YAML config management |
| EmulatorManager | `framework/core/emulator_manager.py` | Appium session factory |
| Logger Factory | `framework/utils/logger_factory.py` | Structured logging |
| Constants module | `framework/utils/constants.py` | Centralized values |
| YAML config files | `config/` | App, emulator, integration settings |

---

## Step-by-Step Instructions

### Step 1: Create the Project Directory Structure

Organize the framework into logical packages:

```
Demo_QA/
├── framework/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   └── emulator_manager.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   └── locators.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── logger_factory.py
│   │   └── markers.py
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── html_report.py
│   └── integrations/
│       ├── __init__.py
│       ├── jira_connector.py
│       └── zephyr_reporter.py
├── config/
│   ├── apps.yaml
│   ├── emulators.yaml
│   ├── integrations.yaml
│   └── README.md
├── tests/
│   ├── conftest.py
│   ├── check_scripts/
│   ├── flows/
│   └── unit/
├── pytest.ini
└── requirements.txt
```

Each directory with Python code must contain an `__init__.py` file to be recognized as a package.

### Step 2: Define Constants and Configuration Values

Create `framework/utils/constants.py` to centralize all magic numbers and application-specific strings:

```python
"""Centralized constants for the Demo_QA framework."""

# Timeouts (seconds)
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
PAGE_LOAD_TIMEOUT = 15
IMPLICIT_WAIT = 5

# Scroll settings
SCROLL_PAUSE = 0.5
MAX_SCROLL_ATTEMPTS = 5
UI_ANIMATION_DELAY = 0.3

# Application identifiers
APP_PACKAGE = "com.swaglabsmobileapp"
APP_ACTIVITY = "com.swaglabsmobileapp.MainActivity"

# Test credentials
TEST_USER_STANDARD = "standard_user"
TEST_USER_LOCKED = "locked_out_user"
TEST_PASSWORD = "secret_sauce"

# Paths
CONFIG_DIR = "config"
REPORTS_DIR = "reports"
LOGS_DIR = "logs"
APPS_CONFIG_FILE = "apps.yaml"
EMULATORS_CONFIG_FILE = "emulators.yaml"
INTEGRATIONS_CONFIG_FILE = "integrations.yaml"

# Logging
LOG_LEVEL = "INFO"
```

**Key principle:** No test file should contain hardcoded timeout values, credentials, or package names. Always reference constants.

### Step 3: Implement Configuration Management

Create `config/apps.yaml`:

```yaml
# Application configuration for Swag Labs Mobile
apk_path: "apps/swag-labs.apk"
package_name: "com.swaglabsmobileapp"
activity_name: "com.swaglabsmobileapp.MainActivity"
app_version: "1.0"
```

Create `config/emulators.yaml`:

```yaml
# Emulator configuration
emulator_name: "Pixel_4_API_30"
platform_version: "11.0"
appium_url: "http://localhost:4723"
port: 4723
```

Implement the `ConfigLoader` class with these responsibilities:

1. **Load YAML files** — Parse configuration from `config/` directory
2. **Validate required keys** — Raise `ConfigurationError` for missing or empty values
3. **Environment variable overrides** — Allow `DEMO_QA_<SECTION>_<KEY>` to override YAML values

```python
class ConfigLoader:
    """Loads and validates YAML configuration with environment variable overrides."""

    def __init__(self, config_dir: str = "config"):
        self._config_dir = config_dir
        self._cache = {}

    def load_app_config(self) -> dict:
        """Load config/apps.yaml. Raises ConfigurationError if missing/invalid."""
        required_keys = ["apk_path", "package_name", "activity_name", "app_version"]
        return self._load_and_validate("apps.yaml", required_keys)

    def load_emulator_config(self) -> dict:
        """Load config/emulators.yaml. Raises ConfigurationError if missing/invalid."""
        required_keys = ["emulator_name", "platform_version", "appium_url", "port"]
        return self._load_and_validate("emulators.yaml", required_keys)

    def get(self, section: str, key: str, default=None):
        """Get config value with env var override (DEMO_QA_<SECTION>_<KEY>)."""
        env_var = f"DEMO_QA_{section.upper()}_{key.upper()}"
        env_value = os.environ.get(env_var)
        if env_value is not None:
            return env_value
        # Fall back to YAML value
        ...
```

**Environment variable override pattern:**
- YAML key `platform_version` in section `emulator` → env var `DEMO_QA_EMULATOR_PLATFORM_VERSION`
- Environment variables always take precedence over file values

### Step 4: Implement the Page Object Model (POM) Pattern

The POM pattern separates test logic from page interaction logic. Each screen in the app gets a corresponding class.

**Architecture:**

```
BasePage (abstract)
├── LoginPage
├── ProductsPage
├── ProductDetailPage
├── CartPage
├── CheckoutInfoPage
├── CheckoutOverviewPage
└── CheckoutCompletePage
```

**BasePage responsibilities:**

| Method | Purpose |
|--------|---------|
| `tap(locator)` | Click an element |
| `type_text(locator, text)` | Clear and type into a field |
| `wait_for_element(locator, timeout)` | Explicit wait for visibility |
| `is_displayed(locator, timeout)` | Check element presence (no exception) |
| `scroll(direction, distance)` | Swipe the screen |
| `get_text(locator)` | Read element text |
| `validate_page()` | Verify page loaded via `key_element` |

**Key design decisions:**

1. **Locator tuples** — All methods accept `(strategy, value)` tuples, e.g., `(AppiumBy.ACCESSIBILITY_ID, "Login")`
2. **Page validation** — Every page object defines a `key_element` attribute. On instantiation, `validate_page()` checks this element is visible within `PAGE_LOAD_TIMEOUT`
3. **Lazy-loading** — Element properties locate elements only on first access, then cache the result
4. **Navigation returns** — Action methods that navigate to a new screen return the destination page object instance

```python
class BasePage(ABC):
    key_element: tuple = None  # Subclasses MUST override

    def __init__(self, driver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.validate_page()  # Fail fast if page didn't load

    def validate_page(self):
        """Check key_element is visible. Raises PageNotLoadedError on timeout."""
        try:
            WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
                EC.visibility_of_element_located(self.key_element)
            )
        except TimeoutException:
            raise PageNotLoadedError(
                page_name=self.__class__.__name__,
                key_element=self.key_element,
            )
```

**Lazy-loading pattern:**

```python
class _LazyElement:
    """Descriptor that locates an element only on first access."""

    def __init__(self, locator: tuple):
        self._locator = locator

    def __set_name__(self, owner, name):
        self._attr_name = f"_lazy_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        cached = getattr(obj, self._attr_name, None)
        if cached is not None:
            return cached
        element = obj.wait_for_element(self._locator)
        setattr(obj, self._attr_name, element)
        return element
```

### Step 5: Implement the Emulator Manager

The `EmulatorManager` handles Appium session creation and teardown:

```python
class EmulatorManager:
    """Manages Appium driver sessions for Android emulators."""

    def __init__(self, config_loader: ConfigLoader):
        self._config = config_loader
        self._driver = None

    def create_session(self) -> webdriver.Remote:
        """Create Appium session with UiAutomator2 capabilities."""
        emulator_config = self._config.load_emulator_config()
        app_config = self._config.load_app_config()

        self._check_appium_connection(emulator_config["appium_url"])

        capabilities = self._build_capabilities(app_config, emulator_config)
        self._driver = webdriver.Remote(
            command_executor=emulator_config["appium_url"],
            desired_capabilities=capabilities,
        )
        log.info("Real-device support available through configuration changes")
        return self._driver

    def quit_session(self):
        """Quit current session and clean up."""
        if self._driver:
            self._driver.quit()
            self._driver = None

    def _build_capabilities(self, app_config, emulator_config) -> dict:
        return {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": emulator_config["emulator_name"],
            "appium:platformVersion": emulator_config["platform_version"],
            "appium:app": app_config["apk_path"],
            "appium:appPackage": app_config["package_name"],
            "appium:appActivity": app_config["activity_name"],
        }

    def _check_appium_connection(self, url: str, timeout: int = 15):
        """Verify Appium server is reachable within timeout."""
        # Raises ConnectionError if unreachable
        ...
```

### Step 6: Set Up Structured Logging

Create `framework/utils/logger_factory.py`:

```python
import logging
import os
from datetime import datetime

def get_logger(name: str, level: str = None) -> logging.Logger:
    """Create a named logger with ISO 8601 format.

    Format: {ISO_timestamp_ms} {level} {filename}:{lineno} {message}
    Output: Console + logs/session_{timestamp}.log
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        log_level = getattr(logging, (level or LOG_LEVEL).upper(), logging.INFO)
        logger.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(levelname)-8s %(filename)s:%(lineno)d %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )

        # Console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        # File handler
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(f"logs/session_{timestamp}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
```

---

## Worked Example: Building the LoginPage

Here is a complete worked example showing how all Phase 4 components come together for the Login screen:

**1. Define locators in the Locator Store (`framework/pages/locators.py`):**

```python
from appium.webdriver.common.appiumby import AppiumBy

class LoginLocators:
    USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    ERROR_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "test-Error message")
```

**2. Create the LoginPage class (`framework/pages/login_page.py`):**

```python
from framework.pages.base_page import BasePage
from framework.pages.locators import LoginLocators

class LoginPage(BasePage):
    key_element = LoginLocators.LOGIN_BUTTON

    def login(self, username: str, password: str):
        """Enter credentials and tap login. Returns ProductsPage."""
        self.type_text(LoginLocators.USERNAME_FIELD, username)
        self.type_text(LoginLocators.PASSWORD_FIELD, password)
        self.tap(LoginLocators.LOGIN_BUTTON)
        from framework.pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def clear_credentials(self):
        """Clear both input fields."""
        self.type_text(LoginLocators.USERNAME_FIELD, "")
        self.type_text(LoginLocators.PASSWORD_FIELD, "")
```

**3. Use in a test:**

```python
from framework.pages.login_page import LoginPage
from framework.utils.constants import TEST_USER_STANDARD, TEST_PASSWORD

def check_T001_login_valid_credentials(driver):
    """Verify successful login with standard_user credentials."""
    login_page = LoginPage(driver)
    products_page = login_page.login(TEST_USER_STANDARD, TEST_PASSWORD)
    assert products_page.is_displayed(ProductsLocators.TITLE)
```

---

## Deliverables Checklist

- [ ] `framework/utils/constants.py` — All timeouts, credentials, paths centralized
- [ ] `framework/utils/logger_factory.py` — Dual-output logger with ISO 8601 format
- [ ] `framework/core/config_loader.py` — YAML loading with validation and env var overrides
- [ ] `framework/core/emulator_manager.py` — Appium session creation and teardown
- [ ] `framework/pages/base_page.py` — Abstract base with tap, type, wait, scroll, validate
- [ ] `framework/pages/locators.py` — Centralized locator store organized by screen
- [ ] `config/apps.yaml` — APK path, package, activity, version
- [ ] `config/emulators.yaml` — Emulator name, platform version, Appium URL, port
- [ ] `config/integrations.yaml` — Placeholder Jira/Zephyr credentials
- [ ] `config/README.md` — Parameter documentation with valid values
- [ ] `requirements.txt` — Pinned dependencies (appium-python-client, pytest, PyYAML, hypothesis, Jinja2)
- [ ] All `__init__.py` files present in framework packages
- [ ] Property tests passing for ConfigLoader (round-trip, error handling, env override)
- [ ] Property tests passing for BasePage (page load validation, lazy-loading)

---

## Tips and Common Pitfalls

- **Don't skip page validation:** Every page object must define `key_element` and call `validate_page()` in `__init__`. This catches navigation errors immediately instead of producing cryptic element-not-found errors later.
- **Keep the Locator Store as the single source of truth:** Never put locator values directly in page objects or tests. When the app changes, you want one file to update.
- **Use accessibility IDs first:** They are the most stable locator strategy. Only fall back to XPath when no accessibility ID is available on the element.
- **Don't over-engineer the config:** Start with the minimum required keys. You can always add more configuration later.
- **Environment variables are for overrides, not defaults:** The YAML files should contain sensible defaults. Environment variables let you change values without editing files (useful in CI/CD).
- **Lazy-loading is an optimization, not a requirement:** If your tests are fast enough without it, simple `find_element` calls in methods are fine. Add lazy-loading when you notice performance issues from repeated lookups.
- **Test your framework components:** The ConfigLoader, BasePage, and markers are code too. Property-based tests catch edge cases you wouldn't think to test manually.
