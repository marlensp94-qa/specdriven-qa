# Configuration Directory

This directory contains all YAML configuration files for the Demo_QA framework.

## Files

| File | Purpose | Required |
|------|---------|----------|
| `apps.yaml` | Target application settings (APK path, package, activity) | Yes |
| `emulators.yaml` | Android emulator/device settings (AVD name, platform, Appium URL) | Yes |
| `integrations.yaml` | Jira/Zephyr Scale integration (disabled by default) | No |

## Configuration Parameters

### apps.yaml

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `app.apk_path` | string | Path to APK relative to project root | `"apps/my-demo-app-android.apk"` |
| `app.package_name` | string | Android package name | `"com.saucelabs.mydemoapp.android"` |
| `app.activity_name` | string | Main activity to launch | `"...SplashActivity"` |
| `app.app_version` | string | Version for reporting | `"1.0.0"` |
| `app.app_name` | string | Display name for reports | `"Swag Labs Mobile"` |

### emulators.yaml

| Parameter | Type | Valid Values | Description |
|-----------|------|-------------|-------------|
| `emulator.name` | string | Any AVD name | Android Virtual Device name |
| `emulator.platform_version` | string | `"10.0"` – `"15.0"` | Android version (min API 29) |
| `emulator.appium_url` | string | Valid URL | Appium server endpoint |
| `emulator.port` | integer | 1024–65535 | Appium server port |
| `emulator.automation_name` | string | `"UiAutomator2"` | Appium automation driver |
| `emulator.device_profile` | string | Any device name | For reporting only |
| `emulator.system_image` | string | `"Google APIs"`, `"Google Play"`, `"default"` | AVD system image type |

### integrations.yaml

| Parameter | Type | Description |
|-----------|------|-------------|
| `jira.base_url` | string | Jira instance URL |
| `jira.project_key` | string | Project key (e.g., "DEMO") |
| `jira.api_token` | string | Authentication token |
| `jira.username` | string | Email associated with token |
| `zephyr.test_cycle_key` | string | Zephyr cycle key (e.g., "DEMO-C1") |
| `zephyr.api_token` | string | Zephyr API token |
| `zephyr.test_plan_key` | string | Test plan key (e.g., "DEMO-P1") |
| `zephyr.test_folder` | string | Folder path in Zephyr |
| `enabled` | boolean | Master switch for integrations |

## Environment Variable Overrides

Any configuration value can be overridden via environment variables using the naming convention:

```
DEMO_QA_<SECTION>_<KEY>
```

Examples:
```bash
export DEMO_QA_APP_APK_PATH="/custom/path/to/app.apk"
export DEMO_QA_EMULATOR_PLATFORM_VERSION="13.0"
export DEMO_QA_EMULATOR_APPIUM_URL="http://192.168.1.100:4723"
export DEMO_QA_JIRA_API_TOKEN="real-token-here"
```

Environment variables **always take precedence** over YAML file values.

## Configuration Priority

```
Environment Variables (highest priority)
    ↓
YAML config files
    ↓
Framework constants/defaults (lowest priority)
```

## Adding a New Configuration

1. Add the key to the appropriate YAML file with a descriptive comment
2. Update this README with the parameter documentation
3. If the key is required, add it to the validation list in `framework/core/config_loader.py`
4. If it should support env var override, follow the `DEMO_QA_<SECTION>_<KEY>` convention

## Troubleshooting

**Error: ConfigurationError — file not found**
- Ensure you're running tests from the `Demo_QA/` root directory
- Check that config files haven't been accidentally deleted

**Error: ConfigurationError — missing key**
- Check the YAML file for the missing key name shown in the error
- Ensure the value is not null or empty

**Error: ConfigurationError — malformed YAML**
- Validate YAML syntax (check for tab characters — use spaces only)
- Online validator: https://www.yamllint.com/
