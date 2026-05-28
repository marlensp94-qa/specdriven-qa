"""
Emulator Manager — Demo_QA
=============================
Creates and manages Appium driver sessions for Android emulators.
Handles session lifecycle, capability building, and connection verification.

Usage:
    from framework.core.emulator_manager import EmulatorManager
    from framework.core.config_loader import ConfigLoader

    config = ConfigLoader()
    manager = EmulatorManager(config)
    driver = manager.create_session()
    # ... run tests ...
    manager.quit_session()
"""

import os
import time
from typing import Optional

import urllib3
from appium import webdriver
from appium.options.android import UiAutomator2Options

from framework.core.config_loader import ConfigLoader, ConfigurationError
from framework.utils.constants import (
    APPIUM_CONNECTION_TIMEOUT,
    AUTOMATION_NAME,
    PLATFORM_NAME,
    IMPLICIT_WAIT,
)
from framework.utils.logger_factory import get_logger

log = get_logger(__name__)


class EmulatorManager:
    """Manages Appium driver sessions for Android emulators.

    Provides session creation with UiAutomator2 capabilities, connection
    verification, and clean teardown. Designed for single-emulator execution
    (no device pool or parallel workers).

    Args:
        config_loader: ConfigLoader instance for reading device and app configuration.

    Example:
        config = ConfigLoader()
        manager = EmulatorManager(config)
        driver = manager.create_session()
        # Use driver for testing...
        manager.quit_session()
    """

    def __init__(self, config_loader: ConfigLoader):
        self._config = config_loader
        self._driver: Optional[webdriver.Remote] = None
        self._appium_url: Optional[str] = None

    @property
    def driver(self) -> Optional[webdriver.Remote]:
        """Return the current Appium WebDriver instance, or None if no session."""
        return self._driver

    def create_session(self) -> webdriver.Remote:
        """Create an Appium driver session configured for Android/UiAutomator2.

        Loads configuration from apps.yaml and emulators.yaml, verifies Appium
        server connectivity, builds capabilities, and creates the session.

        Returns:
            Appium WebDriver (Remote) instance ready for test interaction.

        Raises:
            ConnectionError: If Appium server is not reachable within timeout.
            ConfigurationError: If required configuration is missing or invalid.
        """
        # Load configurations
        app_config = self._config.load_app_config()
        emulator_config = self._config.load_emulator_config()

        # Resolve Appium URL
        self._appium_url = self._config.get(
            "emulator", "appium_url"
        ) or emulator_config.get("appium_url", "http://localhost:4723")

        # Verify Appium server is reachable
        self._check_appium_connection(self._appium_url)

        # Build capabilities and create session
        capabilities = self._build_capabilities(app_config, emulator_config)

        log.info("Creating Appium session at %s", self._appium_url)
        log.info("Platform: %s | Automation: %s", PLATFORM_NAME, AUTOMATION_NAME)
        log.info("App: %s (%s)", app_config.get("app_name", "Unknown"), app_config.get("package_name"))
        log.info(
            "NOTE: Real-device support is available through configuration changes. "
            "See docs/03-extensibility/real-devices.md"
        )

        try:
            self._driver = webdriver.Remote(
                command_executor=self._appium_url,
                options=capabilities,
            )
            self._driver.implicitly_wait(IMPLICIT_WAIT)
            log.info("Session created successfully. Session ID: %s", self._driver.session_id)
        except Exception as e:
            log.error("Failed to create Appium session: %s", e)
            raise ConnectionError(
                f"Failed to create session at '{self._appium_url}': {e}. "
                f"Verify the emulator is running and the APK path is correct."
            ) from e

        return self._driver

    def quit_session(self):
        """Quit the current Appium session and clean up resources.

        Safe to call even if no session exists (no-op in that case).
        """
        if self._driver is not None:
            try:
                self._driver.quit()
                log.info("Appium session terminated successfully.")
            except Exception as e:
                log.warning("Error during session quit: %s", e.__class__.__name__)
            finally:
                self._driver = None

    def _build_capabilities(self, app_config: dict, emulator_config: dict) -> UiAutomator2Options:
        """Build UiAutomator2 desired capabilities from configuration.

        Args:
            app_config: App configuration dictionary (from apps.yaml).
            emulator_config: Emulator configuration dictionary (from emulators.yaml).

        Returns:
            UiAutomator2Options instance with all capabilities set.
        """
        options = UiAutomator2Options()

        # Platform capabilities
        options.platform_name = PLATFORM_NAME
        options.automation_name = AUTOMATION_NAME
        options.platform_version = emulator_config.get("platform_version", "12.0")
        options.device_name = emulator_config.get("name", "emulator-5554")

        # App capabilities
        app_path = app_config.get("apk_path", "")
        if app_path and not os.path.isabs(app_path):
            # Resolve relative to project root
            app_path = os.path.join(self._config.project_root, app_path)

        if app_path and os.path.exists(app_path):
            options.app = app_path
            log.info("Using APK: %s", app_path)
        else:
            # If APK not found, use package/activity (app must be pre-installed)
            log.warning(
                "APK not found at '%s'. Using package/activity (app must be pre-installed).",
                app_path,
            )

        options.app_package = app_config.get("package_name")
        options.app_activity = app_config.get("activity_name")

        # Session behavior
        options.no_reset = False  # Fresh app state for each session
        options.full_reset = False  # Don't uninstall between sessions
        options.auto_grant_permissions = True  # Auto-accept permission dialogs

        # Performance settings
        options.new_command_timeout = 300  # 5 min timeout for idle sessions
        options.adb_exec_timeout = 30000  # 30s for ADB commands

        return options

    def _check_appium_connection(self, url: str, timeout: int = None):
        """Verify Appium server is reachable.

        Attempts to connect to the Appium server's /status endpoint within
        the configured timeout period.

        Args:
            url: Appium server URL (e.g., "http://localhost:4723").
            timeout: Maximum seconds to wait. Defaults to APPIUM_CONNECTION_TIMEOUT.

        Raises:
            ConnectionError: If server is not reachable within timeout.
        """
        if timeout is None:
            timeout = APPIUM_CONNECTION_TIMEOUT

        status_url = f"{url.rstrip('/')}/status"
        log.info("Checking Appium server at %s (timeout: %ds)...", status_url, timeout)

        start_time = time.time()
        last_error = None

        while (time.time() - start_time) < timeout:
            try:
                http = urllib3.PoolManager(timeout=3.0)
                response = http.request("GET", status_url)
                if response.status == 200:
                    log.info("Appium server is reachable.")
                    return
            except (urllib3.exceptions.HTTPError, OSError, ConnectionRefusedError) as e:
                last_error = e
                time.sleep(1)

        raise ConnectionError(
            f"Appium server not reachable at '{url}' after {timeout} seconds. "
            f"Last error: {last_error}. "
            f"Please verify:\n"
            f"  1. Appium is running: appium --port {url.split(':')[-1].rstrip('/')}\n"
            f"  2. The URL in config/emulators.yaml is correct\n"
            f"  3. No firewall is blocking the connection"
        )
