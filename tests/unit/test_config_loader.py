"""
Property-Based Tests for ConfigLoader — Demo_QA
=================================================
Validates correctness properties of the configuration loading system
using Hypothesis for property-based testing.

Properties tested:
- Property 1: Configuration Round-Trip (serialize → load → equivalent)
- Property 2: Configuration Error Handling (missing/malformed/empty → ConfigurationError)
- Property 3: Configuration Environment Variable Override (env var > YAML)

Run with:
    pytest tests/unit/test_config_loader.py -v
"""

import os
import tempfile
import shutil
from pathlib import Path

import pytest
import yaml
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st

from framework.core.config_loader import ConfigLoader, ConfigurationError


# =============================================================================
# Strategies (data generators)
# =============================================================================

# Valid app config values
valid_app_config = st.fixed_dictionaries({
    "app": st.fixed_dictionaries({
        "apk_path": st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=("L", "N", "P"),
            whitelist_characters="/_-."
        )).filter(lambda s: s.strip() != ""),
        "package_name": st.from_regex(r"com\.[a-z]{3,10}\.[a-z]{3,10}", fullmatch=True),
        "activity_name": st.from_regex(r"com\.[a-z]{3,10}\.[a-z]{3,10}\.MainActivity", fullmatch=True),
        "app_version": st.from_regex(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", fullmatch=True),
    })
})

# Valid emulator config values
valid_emulator_config = st.fixed_dictionaries({
    "emulator": st.fixed_dictionaries({
        "name": st.text(min_size=1, max_size=50, alphabet=st.characters(
            whitelist_categories=("L", "N"),
            whitelist_characters="_-"
        )).filter(lambda s: s.strip() != ""),
        "platform_version": st.from_regex(r"1[0-5]\.[0-9]", fullmatch=True),
        "appium_url": st.just("http://localhost:4723"),
        "port": st.integers(min_value=1024, max_value=65535),
    })
})

# Invalid port values (outside valid range)
invalid_ports = st.one_of(
    st.integers(max_value=1023),
    st.integers(min_value=65536),
)

# Non-empty strings for env var overrides
non_empty_strings = st.text(min_size=1, max_size=50, alphabet=st.characters(
    whitelist_categories=("L", "N"),
    whitelist_characters="_-."
)).filter(lambda s: s.strip() != "")

# Section and key names for env var testing
section_names = st.sampled_from(["app", "emulator", "jira", "zephyr"])
key_names = st.sampled_from([
    "apk_path", "package_name", "platform_version", "appium_url", "port", "name"
])


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_config_dir():
    """Create a temporary config directory for testing."""
    temp_dir = tempfile.mkdtemp()
    config_dir = os.path.join(temp_dir, "config")
    os.makedirs(config_dir)
    yield temp_dir, config_dir
    shutil.rmtree(temp_dir)


def write_yaml(path: str, data: dict):
    """Helper to write a YAML file."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)


# =============================================================================
# Property 1: Configuration Round-Trip
# =============================================================================
# For any valid configuration dictionary, serializing it to YAML and loading
# it back through ConfigLoader should produce an equivalent dictionary.

class TestConfigRoundTrip:
    """Property 1: Configuration Round-Trip."""

    # Feature: qa-demo-training, Property 1: Configuration Round-Trip

    @given(config_data=valid_app_config)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_app_config_round_trip(self, config_data, temp_config_dir):
        """App config survives YAML serialize → load cycle."""
        project_root, config_dir = temp_config_dir

        # Write config to YAML
        write_yaml(os.path.join(config_dir, "apps.yaml"), config_data)

        # Also need emulators.yaml for ConfigLoader to work
        write_yaml(os.path.join(config_dir, "emulators.yaml"), {
            "emulator": {"name": "test", "platform_version": "12.0",
                         "appium_url": "http://localhost:4723", "port": 4723}
        })

        # Load through ConfigLoader
        loader = ConfigLoader(config_dir="config", project_root=project_root)
        loaded = loader.load_app_config()

        # Verify all values preserved
        original = config_data["app"]
        assert loaded["apk_path"] == original["apk_path"]
        assert loaded["package_name"] == original["package_name"]
        assert loaded["activity_name"] == original["activity_name"]
        assert loaded["app_version"] == original["app_version"]

    @given(config_data=valid_emulator_config)
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_emulator_config_round_trip(self, config_data, temp_config_dir):
        """Emulator config survives YAML serialize → load cycle."""
        project_root, config_dir = temp_config_dir

        # Write config to YAML
        write_yaml(os.path.join(config_dir, "emulators.yaml"), config_data)

        # Load through ConfigLoader
        loader = ConfigLoader(config_dir="config", project_root=project_root)
        loaded = loader.load_emulator_config()

        # Verify all values preserved
        original = config_data["emulator"]
        assert loaded["name"] == original["name"]
        assert loaded["platform_version"] == original["platform_version"]
        assert loaded["appium_url"] == original["appium_url"]
        assert loaded["port"] == original["port"]


# =============================================================================
# Property 2: Configuration Error Handling
# =============================================================================
# For any configuration file path that does not exist, or any file containing
# invalid YAML syntax, or any valid YAML file missing a required key,
# ConfigLoader SHALL raise ConfigurationError with file path and issue description.

class TestConfigErrorHandling:
    """Property 2: Configuration Error Handling."""

    # Feature: qa-demo-training, Property 2: Configuration Error Handling

    def test_missing_file_raises_error_with_path(self, temp_config_dir):
        """Missing config file raises ConfigurationError containing the file path."""
        project_root, config_dir = temp_config_dir

        loader = ConfigLoader(config_dir="config", project_root=project_root)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load_app_config()

        assert "apps.yaml" in str(exc_info.value.file_path)
        assert "not found" in exc_info.value.issue.lower() or "File not found" in exc_info.value.issue

    def test_malformed_yaml_raises_error(self, temp_config_dir):
        """Invalid YAML syntax raises ConfigurationError mentioning 'malformed'."""
        project_root, config_dir = temp_config_dir

        # Write invalid YAML
        file_path = os.path.join(config_dir, "apps.yaml")
        with open(file_path, "w") as f:
            f.write("invalid: yaml: content: [unclosed bracket\n  bad indent")

        loader = ConfigLoader(config_dir="config", project_root=project_root)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load_app_config()

        assert "apps.yaml" in str(exc_info.value.file_path)
        assert "malformed" in exc_info.value.issue.lower() or "YAML" in exc_info.value.issue

    @given(missing_key=st.sampled_from(["apk_path", "package_name", "activity_name", "app_version"]))
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_missing_required_key_raises_error(self, missing_key, temp_config_dir):
        """Missing required key raises ConfigurationError naming the key."""
        project_root, config_dir = temp_config_dir

        # Create config with one key missing
        config_data = {
            "app": {
                "apk_path": "apps/test.apk",
                "package_name": "com.test.app",
                "activity_name": "com.test.app.Main",
                "app_version": "1.0.0",
            }
        }
        del config_data["app"][missing_key]

        write_yaml(os.path.join(config_dir, "apps.yaml"), config_data)

        loader = ConfigLoader(config_dir="config", project_root=project_root)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load_app_config()

        # Error should mention the missing key
        assert missing_key in exc_info.value.issue

    @given(empty_key=st.sampled_from(["apk_path", "package_name", "activity_name", "app_version"]))
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_empty_value_raises_error(self, empty_key, temp_config_dir):
        """Empty/null value for required key raises ConfigurationError."""
        project_root, config_dir = temp_config_dir

        config_data = {
            "app": {
                "apk_path": "apps/test.apk",
                "package_name": "com.test.app",
                "activity_name": "com.test.app.Main",
                "app_version": "1.0.0",
            }
        }
        config_data["app"][empty_key] = ""  # Empty string

        write_yaml(os.path.join(config_dir, "apps.yaml"), config_data)

        loader = ConfigLoader(config_dir="config", project_root=project_root)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load_app_config()

        assert empty_key in exc_info.value.issue

    @given(port=invalid_ports)
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_invalid_port_raises_error(self, port, temp_config_dir):
        """Port outside 1024-65535 raises ConfigurationError."""
        project_root, config_dir = temp_config_dir

        config_data = {
            "emulator": {
                "name": "TestDevice",
                "platform_version": "12.0",
                "appium_url": "http://localhost:4723",
                "port": port,
            }
        }

        write_yaml(os.path.join(config_dir, "emulators.yaml"), config_data)

        loader = ConfigLoader(config_dir="config", project_root=project_root)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load_emulator_config()

        assert "port" in exc_info.value.issue.lower()

    def test_empty_file_raises_error(self, temp_config_dir):
        """Empty YAML file raises ConfigurationError."""
        project_root, config_dir = temp_config_dir

        file_path = os.path.join(config_dir, "apps.yaml")
        with open(file_path, "w") as f:
            f.write("")  # Empty file

        loader = ConfigLoader(config_dir="config", project_root=project_root)

        with pytest.raises(ConfigurationError) as exc_info:
            loader.load_app_config()

        assert "empty" in exc_info.value.issue.lower() or "File is empty" in exc_info.value.issue


# =============================================================================
# Property 3: Configuration Environment Variable Override
# =============================================================================
# For any configuration section and key with a value defined in YAML, setting
# DEMO_QA_{SECTION}_{KEY} should cause get() to return the env var value.

class TestConfigEnvOverride:
    """Property 3: Configuration Environment Variable Override."""

    # Feature: qa-demo-training, Property 3: Configuration Environment Variable Override

    @given(
        section=section_names,
        key=key_names,
        override_value=non_empty_strings,
    )
    @settings(max_examples=25, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_env_var_overrides_yaml_value(self, section, key, override_value, temp_config_dir):
        """Environment variable takes precedence over YAML value."""
        project_root, config_dir = temp_config_dir

        # Write a config with a YAML value
        yaml_value = "original_yaml_value"
        config_data = {section: {key: yaml_value}}
        write_yaml(os.path.join(config_dir, "apps.yaml"), {"app": {"apk_path": "x", "package_name": "x", "activity_name": "x", "app_version": "x"}})

        loader = ConfigLoader(config_dir="config", project_root=project_root)
        loader._cache[section] = {key: yaml_value}

        # Set environment variable
        env_var = f"DEMO_QA_{section.upper()}_{key.upper()}"
        os.environ[env_var] = override_value

        try:
            result = loader.get(section, key)
            assert result == override_value, (
                f"Expected env var override '{override_value}', got '{result}'"
            )
        finally:
            # Clean up env var
            del os.environ[env_var]

    @given(
        section=section_names,
        key=key_names,
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_yaml_value_used_when_no_env_var(self, section, key, temp_config_dir):
        """YAML value is returned when no environment variable is set."""
        project_root, config_dir = temp_config_dir

        yaml_value = "from_yaml_file"

        # Ensure env var is NOT set
        env_var = f"DEMO_QA_{section.upper()}_{key.upper()}"
        os.environ.pop(env_var, None)

        loader = ConfigLoader(config_dir="config", project_root=project_root)
        loader._cache[section] = {key: yaml_value}

        result = loader.get(section, key)
        assert result == yaml_value

    @given(
        section=section_names,
        key=key_names,
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_default_used_when_no_env_and_no_yaml(self, section, key, temp_config_dir):
        """Default value is returned when neither env var nor YAML value exists."""
        project_root, config_dir = temp_config_dir

        # Ensure env var is NOT set
        env_var = f"DEMO_QA_{section.upper()}_{key.upper()}"
        os.environ.pop(env_var, None)

        loader = ConfigLoader(config_dir="config", project_root=project_root)
        # Empty cache — no YAML value loaded

        default_value = "my_default"
        result = loader.get(section, key, default=default_value)
        assert result == default_value
