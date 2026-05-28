"""
Configuration Loader — Demo_QA
================================
Loads, validates, and provides access to YAML configuration files.
Supports environment variable overrides using DEMO_QA_<SECTION>_<KEY> convention.

Usage:
    from framework.core.config_loader import ConfigLoader, ConfigurationError

    config = ConfigLoader()
    app_config = config.load_app_config()
    emulator_config = config.load_emulator_config()

    # With env var override
    value = config.get("emulator", "platform_version")
"""

import os
from pathlib import Path
from typing import Any, Optional

import yaml

from framework.utils.constants import (
    CONFIG_DIR,
    APPS_CONFIG_FILE,
    EMULATORS_CONFIG_FILE,
    INTEGRATIONS_CONFIG_FILE,
)


class ConfigurationError(Exception):
    """Raised when configuration is missing, malformed, or invalid.

    Attributes:
        file_path: Path to the problematic configuration file.
        issue: Description of what went wrong.
    """

    def __init__(self, file_path: str, issue: str):
        self.file_path = file_path
        self.issue = issue
        super().__init__(f"Configuration error in '{file_path}': {issue}")


class ConfigLoader:
    """Loads and validates YAML configuration with environment variable overrides.

    The loader searches for config files relative to the project root directory.
    Environment variables override YAML values using the naming convention:
        DEMO_QA_<SECTION>_<KEY> (uppercase, underscores replacing dots)

    Args:
        config_dir: Path to configuration directory relative to project root.
                    Defaults to "config".
        project_root: Absolute path to project root. Auto-detected if None.
    """

    def __init__(self, config_dir: str = None, project_root: str = None):
        if project_root is None:
            # Auto-detect: go up from this file's location to find project root
            # framework/core/config_loader.py -> framework/core -> framework -> Demo_QA
            project_root = str(Path(__file__).resolve().parents[2])

        self._project_root = project_root
        self._config_dir = os.path.join(
            project_root, config_dir or CONFIG_DIR
        )
        self._cache: dict = {}

    @property
    def project_root(self) -> str:
        """Return the resolved project root path."""
        return self._project_root

    def load_app_config(self) -> dict:
        """Load config/apps.yaml and validate required keys.

        Returns:
            Dictionary with app configuration values.

        Raises:
            ConfigurationError: If file is missing, malformed, or missing required keys.
        """
        file_path = os.path.join(self._config_dir, APPS_CONFIG_FILE)
        data = self._load_yaml(file_path)

        required_keys = ["apk_path", "package_name", "activity_name", "app_version"]
        app_data = data.get("app", {})
        if not app_data:
            raise ConfigurationError(
                file_path, "Missing 'app' section"
            )

        self._validate_required_keys(app_data, required_keys, file_path)
        self._cache["app"] = app_data
        return app_data

    def load_emulator_config(self) -> dict:
        """Load config/emulators.yaml and validate required keys.

        Returns:
            Dictionary with emulator configuration values.

        Raises:
            ConfigurationError: If file is missing, malformed, or missing required keys.
        """
        file_path = os.path.join(self._config_dir, EMULATORS_CONFIG_FILE)
        data = self._load_yaml(file_path)

        required_keys = ["name", "platform_version", "appium_url", "port"]
        emulator_data = data.get("emulator", {})
        if not emulator_data:
            raise ConfigurationError(
                file_path, "Missing 'emulator' section"
            )

        self._validate_required_keys(emulator_data, required_keys, file_path)

        # Validate port range
        port = emulator_data.get("port")
        if isinstance(port, int) and not (1024 <= port <= 65535):
            raise ConfigurationError(
                file_path,
                f"Invalid port '{port}': must be between 1024 and 65535",
            )

        self._cache["emulator"] = emulator_data
        return emulator_data

    def load_integrations_config(self) -> dict:
        """Load config/integrations.yaml (optional — does not raise if disabled).

        Returns:
            Dictionary with integrations configuration values.

        Raises:
            ConfigurationError: If file exists but contains invalid YAML.
        """
        file_path = os.path.join(self._config_dir, INTEGRATIONS_CONFIG_FILE)

        # Integrations config is optional — return empty if not found
        if not os.path.exists(file_path):
            return {"enabled": False}

        data = self._load_yaml(file_path)
        self._cache["integrations"] = data
        return data

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value with environment variable override.

        Environment variable format: DEMO_QA_<SECTION>_<KEY> (uppercase).
        Environment variables always take precedence over YAML values.

        Args:
            section: Configuration section (e.g., "app", "emulator", "jira").
            key: Configuration key within the section.
            default: Default value if key not found anywhere.

        Returns:
            Configuration value (env var > YAML > default).
        """
        # Check environment variable first (highest priority)
        env_var = f"DEMO_QA_{section.upper()}_{key.upper()}"
        env_value = os.environ.get(env_var)
        if env_value is not None:
            return env_value

        # Check cached config
        section_data = self._cache.get(section, {})
        if isinstance(section_data, dict):
            value = section_data.get(key)
            if value is not None:
                return value

        return default

    def _validate_required_keys(
        self, data: dict, required_keys: list, file_path: str
    ):
        """Validate that all required keys are present and non-empty.

        Args:
            data: Dictionary to validate.
            required_keys: List of keys that must be present and non-empty.
            file_path: File path for error messages.

        Raises:
            ConfigurationError: If any required key is missing or empty.
        """
        for key in required_keys:
            value = data.get(key)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise ConfigurationError(
                    file_path,
                    f"Required key '{key}' is missing or empty",
                )

    def _load_yaml(self, file_path: str) -> dict:
        """Load and parse a YAML file.

        Args:
            file_path: Absolute path to the YAML file.

        Returns:
            Parsed YAML content as a dictionary.

        Raises:
            ConfigurationError: If file doesn't exist or contains invalid YAML.
        """
        if not os.path.exists(file_path):
            raise ConfigurationError(
                file_path, "File not found"
            )

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(
                file_path, f"Malformed YAML: {e}"
            )
        except (IOError, OSError) as e:
            raise ConfigurationError(
                file_path, f"Cannot read file: {e}"
            )

        if data is None:
            raise ConfigurationError(
                file_path, "File is empty"
            )

        if not isinstance(data, dict):
            raise ConfigurationError(
                file_path, "Root element must be a YAML mapping (dictionary)"
            )

        return data
