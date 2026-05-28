"""
Framework Constants — Demo_QA
==============================
Centralized configuration values for the mini automation framework.
All timing values, credentials, identifiers, and configurable parameters
are defined here to eliminate magic numbers and hardcoded strings.

Usage:
    from framework.utils.constants import DEFAULT_TIMEOUT, TEST_USER_STANDARD
"""

import os

# =============================================================================
# TIMEOUTS (seconds)
# =============================================================================

# Default explicit wait timeout for element visibility
DEFAULT_TIMEOUT = 10

# Implicit wait timeout (applied globally to driver)
IMPLICIT_WAIT = 5

# Page load timeout — maximum time to wait for a page to validate
PAGE_LOAD_TIMEOUT = 15

# Short timeout for optional elements or quick checks
SHORT_TIMEOUT = 3

# Connection timeout for Appium server reachability check
APPIUM_CONNECTION_TIMEOUT = 15

# =============================================================================
# APPIUM / DRIVER CONFIGURATION
# =============================================================================

# Default Appium server URL
APPIUM_BASE_URL = "http://localhost:4723"

# Automation engine
AUTOMATION_NAME = "UiAutomator2"

# Platform
PLATFORM_NAME = "Android"

# =============================================================================
# APPLICATION IDENTIFIERS
# =============================================================================

# Swag Labs Mobile (Sauce Labs demo app)
APP_PACKAGE = "com.saucelabs.mydemoapp.android"
APP_ACTIVITY = "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"
APP_NAME = "Swag Labs Mobile"

# =============================================================================
# TEST USER CREDENTIALS
# =============================================================================
# Swag Labs provides several test users with different behaviors.
# See: https://github.com/saucelabs/my-demo-app-android

# Standard user — full access, no restrictions
TEST_USER_STANDARD = "bod@example.com"
TEST_PASSWORD_STANDARD = "10203040"

# Locked out user — login will be rejected
TEST_USER_LOCKED = "alice@example.com"
TEST_PASSWORD_LOCKED = "10203040"

# Problem user — experiences UI glitches
TEST_USER_PROBLEM = "bob@example.com"
TEST_PASSWORD_PROBLEM = "10203040"

# =============================================================================
# UI INTERACTION TIMING (seconds)
# =============================================================================

# Delay after UI animations (transitions, modals)
UI_ANIMATION_DELAY = 0.5

# Delay between rapid interactions (typing, tapping sequences)
INTERACTION_DELAY = 0.3

# Scroll pause duration (wait for content to settle)
SCROLL_PAUSE = 0.8

# Maximum scroll attempts before giving up
MAX_SCROLL_ATTEMPTS = 5

# =============================================================================
# REPORTING
# =============================================================================

# Directory for generated reports (relative to project root)
REPORTS_DIR = "reports"

# Directory for log files (relative to project root)
LOGS_DIR = "logs"

# Screenshot filename format (used in f-strings)
SCREENSHOT_FORMAT = "{test_name}_{timestamp}.png"

# Report filename format
REPORT_FORMAT = "report_{timestamp}.html"

# =============================================================================
# LOGGING
# =============================================================================

# Default log level (can be overridden via DEMO_QA_LOG_LEVEL env var)
LOG_LEVEL = os.environ.get("DEMO_QA_LOG_LEVEL", "INFO")

# Log format — ISO 8601 with milliseconds
LOG_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)-8s %(filename)s:%(lineno)d %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

# =============================================================================
# CONFIGURATION PATHS
# =============================================================================

# Configuration directory (relative to project root)
CONFIG_DIR = "config"

# Config file names
APPS_CONFIG_FILE = "apps.yaml"
EMULATORS_CONFIG_FILE = "emulators.yaml"
INTEGRATIONS_CONFIG_FILE = "integrations.yaml"
