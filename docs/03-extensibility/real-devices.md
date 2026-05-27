# Extending the Framework for Real Android Devices

## Overview

The Demo_QA framework is designed with a configuration-driven architecture that separates driver creation from test logic. This means you can run your existing test suite on a real Android device by updating configuration only — no changes to test files or page objects are required.

This guide covers the complete process of connecting a physical Android device and running your tests against it.

---

## Prerequisites

- A physical Android device (Android 10.0 / API 29 or higher)
- A USB cable (preferably the one that came with the device)
- Android SDK Platform-Tools installed (includes `adb`)
- Appium 2.x running with the UiAutomator2 driver installed
- The Swag Labs APK file available in the `apps/` directory

---

## Step 1: Enable USB Debugging on the Device

USB debugging allows your computer to communicate with the device via ADB (Android Debug Bridge).

### Instructions

1. Open **Settings** on your Android device.
2. Navigate to **About Phone** (or **About Device**).
3. Tap **Build Number** 7 times until you see "You are now a developer!"
4. Go back to **Settings** → **Developer Options**.
5. Enable **USB Debugging**.
6. (Optional) Enable **Stay Awake** to prevent the screen from turning off during tests.

### Verification

Connect the device via USB and run:

```bash
adb devices
```

Expected output:

```
List of devices attached
XXXXXXXXXXXXXXX    device
```

If you see `unauthorized` instead of `device`, check the device screen for a USB debugging authorization prompt and tap **Allow**.

---

## Step 2: Discover the Device UDID

The UDID (Unique Device Identifier) is required to target a specific device when multiple devices or emulators are connected.

### Method 1: Using ADB

```bash
adb devices -l
```

Output example:

```
List of devices attached
R5CR30XXXXX        device usb:1-1 product:starqltesq model:SM_G960U transport_id:1
```

The UDID is the alphanumeric string in the first column (e.g., `R5CR30XXXXX`).

### Method 2: Using ADB Shell

```bash
adb shell getprop ro.serialno
```

This returns the device serial number directly.

### Method 3: From Device Settings

Navigate to **Settings** → **About Phone** → **Status** → **Serial Number**.

---

## Step 3: Update the Configuration

Add a new entry to `config/emulators.yaml` for your real device. You can keep the existing emulator entry and add the device alongside it, or replace it entirely.

### Example: Adding a Real Device Entry

```yaml
# =============================================================================
# Device Configuration — Real Android Device
# =============================================================================

emulator:
  # Device name (descriptive, used in reports)
  name: "Samsung_Galaxy_S21"

  # Android platform version on the device
  # Check via: adb shell getprop ro.build.version.release
  platform_version: "13.0"

  # Appium server URL (same as emulator setup)
  appium_url: "http://localhost:4723"

  # Appium server port
  port: 4723

  # Automation engine
  automation_name: "UiAutomator2"

  # Device UDID — REQUIRED for real devices
  # Discovered via: adb devices
  udid: "R5CR30XXXXX"

  # Device profile (informational)
  device_profile: "Samsung Galaxy S21"

  # System image type (not applicable for real devices, kept for compatibility)
  system_image: "N/A"
```

### Key Differences from Emulator Configuration

| Parameter | Emulator | Real Device |
|-----------|----------|-------------|
| `name` | AVD name (e.g., `Pixel_6_API_31`) | Descriptive name |
| `udid` | Not required (optional) | **Required** — device serial number |
| `platform_version` | Matches system image | Matches device OS version |
| `system_image` | `Google APIs` / `Google Play` | Not applicable |

---

## Step 4: Capabilities Changes

When targeting a real device, the Appium desired capabilities differ slightly from emulator sessions.

### Required Capability Changes

| Capability | Emulator Value | Real Device Value |
|------------|---------------|-------------------|
| `appium:udid` | (omitted or AVD name) | Device serial from `adb devices` |
| `appium:noReset` | `false` (typical) | `true` (recommended to preserve app state between runs) |
| `appium:autoGrantPermissions` | `true` | `true` (avoids permission dialogs) |

### How the Framework Handles This

The `EmulatorManager._build_capabilities()` method reads from `config/emulators.yaml`. When a `udid` field is present, Appium automatically targets the physical device instead of launching an emulator. No code changes are needed — the configuration drives the behavior.

### Environment Variable Override

You can also target a real device without modifying the YAML file by setting environment variables:

```bash
export DEMO_QA_EMULATOR_UDID="R5CR30XXXXX"
export DEMO_QA_EMULATOR_PLATFORM_VERSION="13.0"
export DEMO_QA_EMULATOR_NAME="Samsung_Galaxy_S21"
```

---

## Step 5: Install the APK on the Device

Before running tests, ensure the Swag Labs APK is available on the device:

```bash
adb -s R5CR30XXXXX install apps/my-demo-app-android.apk
```

Alternatively, set `appium:app` in capabilities to the APK path and Appium will install it automatically on session creation.

---

## Step-by-Step Example: Running Tests on a Real Device

This complete walkthrough takes you from a connected device to a passing test.

### 1. Connect and verify the device

```bash
# Verify device is connected and authorized
adb devices
# Expected: R5CR30XXXXX    device
```

### 2. Get the device details

```bash
# Get Android version
adb -s R5CR30XXXXX shell getprop ro.build.version.release
# Output: 13

# Get device model
adb -s R5CR30XXXXX shell getprop ro.product.model
# Output: SM-G991B
```

### 3. Update `config/emulators.yaml`

```yaml
emulator:
  name: "Samsung_Galaxy_S21"
  platform_version: "13.0"
  appium_url: "http://localhost:4723"
  port: 4723
  automation_name: "UiAutomator2"
  udid: "R5CR30XXXXX"
  device_profile: "Samsung Galaxy S21"
  system_image: "N/A"
```

### 4. Start Appium server

```bash
appium --port 4723
```

### 5. Run a smoke test

```bash
pytest tests/check_scripts/check_T001_login_valid_credentials.py -v --tb=short
```

### 6. Verify results

The test should execute on the physical device. You will see the Swag Labs app launch on the device screen. The HTML report will be generated in `reports/` as usual.

---

## Troubleshooting

### Device not detected by ADB

- Try a different USB cable (use the original manufacturer cable if possible).
- Ensure USB debugging is enabled in Developer Options.
- On the device, revoke USB debugging authorizations and re-authorize.
- Restart the ADB server: `adb kill-server && adb start-server`.

### "Could not find a connected Android device"

- Verify with `adb devices` that the device shows as `device` (not `offline` or `unauthorized`).
- Ensure only one device/emulator is connected, or specify the UDID explicitly.

### App crashes on launch

- Verify the APK is compatible with the device's Android version.
- Check available storage: `adb -s <UDID> shell df`.
- Try a clean install: `adb -s <UDID> uninstall com.saucelabs.mydemoapp.android && adb -s <UDID> install apps/my-demo-app-android.apk`.

### Permission dialogs interrupting tests

- Add `appium:autoGrantPermissions: true` to capabilities.
- Alternatively, grant permissions manually before running tests.

### Slow test execution on device

- Disable animations: **Settings** → **Developer Options** → Set all animation scales to **0x**.
- Ensure the device is not in power-saving mode.
- Use a USB 3.0 port for faster communication.

---

## Summary

| Step | Action | Command/File |
|------|--------|--------------|
| 1 | Enable USB debugging | Device Settings → Developer Options |
| 2 | Discover UDID | `adb devices` |
| 3 | Update configuration | `config/emulators.yaml` — add `udid` field |
| 4 | Install APK | `adb install apps/my-demo-app-android.apk` |
| 5 | Start Appium | `appium --port 4723` |
| 6 | Run tests | `pytest tests/check_scripts/ -v` |

No test code or page object modifications are required. The framework's configuration-driven design ensures that switching between emulator and real device is purely a configuration change.
