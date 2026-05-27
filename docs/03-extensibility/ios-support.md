# Extending the Framework for iOS

## Overview

The Demo_QA framework's Page Object Model and configuration-driven architecture are designed to support multiple platforms. While the current implementation targets Android emulators, extending to iOS requires setting up the Apple toolchain, building WebDriverAgent, and adding iOS-specific capabilities to the configuration.

This guide covers the complete process of adding iOS device support to the framework.

---

## Prerequisites

- A Mac running macOS 12 (Monterey) or later
- An Apple Developer account (free account works for personal devices)
- An iOS device running iOS 15.0 or later, or the Xcode iOS Simulator
- Xcode 14.0 or later installed from the Mac App Store
- Appium 2.x with the XCUITest driver installed
- A USB cable (Lightning or USB-C depending on device)

---

## Step 1: Install Xcode and Command-Line Tools

### Install Xcode

1. Open the **Mac App Store**.
2. Search for **Xcode** and install it (requires 12+ GB of disk space).
3. Launch Xcode once to accept the license agreement.
4. Wait for additional components to download and install.

### Install Command-Line Tools

```bash
xcode-select --install
```

### Verify Installation

```bash
# Check Xcode version
xcodebuild -version
# Expected: Xcode 14.x or higher

# Check command-line tools path
xcode-select -p
# Expected: /Applications/Xcode.app/Contents/Developer
```

### Set the Active Developer Directory

If you have multiple Xcode versions installed:

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

---

## Step 2: Install the Appium XCUITest Driver

The XCUITest driver is the iOS equivalent of UiAutomator2 for Android.

```bash
appium driver install xcuitest
```

### Verify Installation

```bash
appium driver list --installed
```

Expected output should include:

```
- xcuitest@x.x.x [installed (npm)]
```

---

## Step 3: Build and Configure WebDriverAgent

WebDriverAgent (WDA) is a WebDriver server for iOS that Appium uses to communicate with the device. It must be built and signed with a valid Apple Developer certificate.

### Locate WebDriverAgent

After installing the XCUITest driver, WDA is located at:

```bash
~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent
```

### Open in Xcode

```bash
open ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent/WebDriverAgent.xcodeproj
```

### Configure Signing

1. In Xcode, select the **WebDriverAgentRunner** target.
2. Go to **Signing & Capabilities** tab.
3. Check **Automatically manage signing**.
4. Select your **Team** (your Apple Developer account).
5. If you see a bundle identifier conflict, change it to something unique:
   - Example: `com.yourname.WebDriverAgentRunner`
6. Repeat for the **WebDriverAgentLib** target.
7. Repeat for the **IntegrationApp** target (if present).

### Build WebDriverAgent

Build from the command line to verify everything compiles:

```bash
cd ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent

xcodebuild build-for-testing \
  -project WebDriverAgent.xcodeproj \
  -scheme WebDriverAgentRunner \
  -destination 'id=<DEVICE_UDID>' \
  IPHONEOS_DEPLOYMENT_TARGET=15.0 \
  CODE_SIGN_IDENTITY="Apple Development" \
  DEVELOPMENT_TEAM="<YOUR_TEAM_ID>"
```

Replace `<DEVICE_UDID>` with your device UDID and `<YOUR_TEAM_ID>` with your Apple Developer Team ID.

### Trust the Developer Certificate on Device

After the first build to a physical device:

1. On the iOS device, go to **Settings** → **General** → **VPN & Device Management**.
2. Find your developer certificate under **Developer App**.
3. Tap **Trust** to allow apps signed with this certificate.

---

## Step 4: Discover iOS Device UDID

### Method 1: Using Xcode

1. Connect the device via USB.
2. Open **Xcode** → **Window** → **Devices and Simulators**.
3. Select your device — the **Identifier** field shows the UDID.

### Method 2: Using the Command Line

```bash
# List connected iOS devices
xcrun xctrace list devices
```

Output example:

```
== Devices ==
iPhone 14 Pro (16.1) (00008110-XXXXXXXXXXXX)

== Simulators ==
iPhone 14 Simulator (16.1) (XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)
```

The value in parentheses after the iOS version is the UDID.

### Method 3: Using idevice_id (libimobiledevice)

```bash
brew install libimobiledevice
idevice_id -l
```

---

## Step 5: iOS Desired Capabilities

iOS requires a different set of Appium capabilities compared to Android.

### Key iOS Capabilities

| Capability | Description | Example Value |
|------------|-------------|---------------|
| `platformName` | Target platform | `iOS` |
| `appium:automationName` | Automation driver | `XCUITest` |
| `appium:deviceName` | Device name | `iPhone 14 Pro` |
| `appium:platformVersion` | iOS version | `16.1` |
| `appium:udid` | Device UDID | `00008110-XXXXXXXXXXXX` |
| `appium:app` | Path to .app or .ipa | `apps/SwagLabs.ipa` |
| `appium:bundleId` | App bundle identifier | `com.saucelabs.SwagLabsMobileApp` |
| `appium:xcodeOrgId` | Apple Team ID | `XXXXXXXXXX` |
| `appium:xcodeSigningId` | Signing identity | `iPhone Developer` |
| `appium:wdaLocalPort` | WDA communication port | `8100` |
| `appium:noReset` | Preserve app state | `true` |
| `appium:autoAcceptAlerts` | Dismiss iOS alerts | `true` |

### Comparison: Android vs iOS Capabilities

| Aspect | Android | iOS |
|--------|---------|-----|
| Automation name | `UiAutomator2` | `XCUITest` |
| App format | `.apk` | `.ipa` or `.app` |
| App identifier | `appPackage` + `appActivity` | `bundleId` |
| Signing | Not required | Apple Developer certificate |
| Device targeting | `udid` (serial number) | `udid` (Xcode identifier) |

---

## Step 6: Add iOS Configuration

Create a new configuration section or file for iOS devices. The framework's `ConfigLoader` supports environment variable overrides, so you can switch between platforms without modifying files.

### Option A: Separate iOS Config File

Create `config/ios_device.yaml`:

```yaml
# =============================================================================
# Device Configuration — iOS Real Device
# =============================================================================

device:
  # Device name (as shown in Xcode)
  name: "iPhone_14_Pro"

  # iOS version
  platform_version: "16.1"

  # Platform
  platform_name: "iOS"

  # Appium server URL
  appium_url: "http://localhost:4723"

  # Appium server port
  port: 4723

  # Automation engine for iOS
  automation_name: "XCUITest"

  # Device UDID (from Xcode or xcrun xctrace list devices)
  udid: "00008110-XXXXXXXXXXXX"

  # App bundle identifier
  bundle_id: "com.saucelabs.SwagLabsMobileApp"

  # Path to IPA file
  app_path: "apps/SwagLabs.ipa"

  # Apple Developer Team ID (from developer.apple.com)
  xcode_org_id: "XXXXXXXXXX"

  # Signing identity
  xcode_signing_id: "iPhone Developer"

  # WebDriverAgent local port
  wda_local_port: 8100
```

### Option B: Environment Variable Override

Switch to iOS without changing any files:

```bash
export DEMO_QA_EMULATOR_PLATFORM_NAME="iOS"
export DEMO_QA_EMULATOR_AUTOMATION_NAME="XCUITest"
export DEMO_QA_EMULATOR_UDID="00008110-XXXXXXXXXXXX"
export DEMO_QA_EMULATOR_PLATFORM_VERSION="16.1"
export DEMO_QA_EMULATOR_NAME="iPhone_14_Pro"
```

---

## Step-by-Step Example: Running Tests on an iOS Device

This walkthrough takes you from a fresh setup to running a test on a physical iPhone.

### 1. Verify Xcode and tools

```bash
xcodebuild -version
# Xcode 14.3.1
# Build version 14E300c

appium driver list --installed
# - xcuitest@5.x.x [installed (npm)]
```

### 2. Connect and identify the device

```bash
xcrun xctrace list devices
# iPhone 14 Pro (16.1) (00008110-XXXXXXXXXXXX)
```

### 3. Build WebDriverAgent for the device

```bash
cd ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent

xcodebuild build-for-testing \
  -project WebDriverAgent.xcodeproj \
  -scheme WebDriverAgentRunner \
  -destination 'id=00008110-XXXXXXXXXXXX' \
  CODE_SIGN_IDENTITY="Apple Development" \
  DEVELOPMENT_TEAM="XXXXXXXXXX"
```

### 4. Trust the certificate on the device

- **Settings** → **General** → **VPN & Device Management** → Trust your developer certificate.

### 5. Create the iOS configuration

Create `config/ios_device.yaml` with the content from Step 6 above, filling in your actual UDID and Team ID.

### 6. Start Appium server

```bash
appium --port 4723
```

### 7. Run a smoke test

```bash
# Using environment variables to target iOS
export DEMO_QA_EMULATOR_PLATFORM_NAME="iOS"
export DEMO_QA_EMULATOR_AUTOMATION_NAME="XCUITest"
export DEMO_QA_EMULATOR_UDID="00008110-XXXXXXXXXXXX"
export DEMO_QA_EMULATOR_PLATFORM_VERSION="16.1"

pytest tests/check_scripts/check_T001_login_valid_credentials.py -v --tb=short
```

### 8. Verify results

The test executes on the iPhone. The Swag Labs app launches on the device, and the HTML report is generated in `reports/` as usual.

---

## Locator Strategy Considerations for iOS

The framework uses accessibility IDs as the primary locator strategy (80%+ of locators). This is intentional — accessibility IDs work identically on both Android and iOS, making cross-platform support straightforward.

### What works across platforms

| Strategy | Android | iOS | Cross-Platform |
|----------|---------|-----|----------------|
| Accessibility ID | `content-desc` attribute | `accessibilityIdentifier` | Yes |
| XPath | Works but slow | Works but slow | Syntax differs |
| Resource ID | `resource-id` attribute | Not available | No |
| iOS Predicate | Not available | Native iOS queries | No |
| iOS Class Chain | Not available | Native iOS queries | No |

### Locator adjustments needed

If the Swag Labs iOS app uses the same accessibility identifiers as the Android version (which is common for cross-platform apps), no locator changes are needed. If identifiers differ, you would:

1. Create an iOS-specific locator set in `framework/pages/locators.py`.
2. Use a platform-aware locator selection pattern based on the active configuration.

---

## Using the iOS Simulator

For development and testing without a physical device, you can use the Xcode iOS Simulator.

### List Available Simulators

```bash
xcrun simctl list devices available
```

### Boot a Simulator

```bash
xcrun simctl boot "iPhone 14 Pro"
```

### Configuration for Simulator

The configuration is similar to a real device, but without signing requirements:

```yaml
device:
  name: "iPhone 14 Pro"
  platform_version: "16.1"
  platform_name: "iOS"
  appium_url: "http://localhost:4723"
  port: 4723
  automation_name: "XCUITest"
  # For simulators, use the simulator UDID from: xcrun simctl list devices
  udid: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
  bundle_id: "com.saucelabs.SwagLabsMobileApp"
  app_path: "apps/SwagLabs.app"  # Use .app for simulator, .ipa for device
```

Note: Simulators use `.app` bundles while real devices require `.ipa` files.

---

## Troubleshooting

### "Unable to launch WebDriverAgent"

- Rebuild WDA in Xcode with the correct signing profile.
- Ensure the developer certificate is trusted on the device.
- Check that the bundle identifier is unique and not conflicting.

### "Could not determine your device UDID"

- Verify the device is connected: `xcrun xctrace list devices`.
- Ensure the device is unlocked and trusted (tap "Trust" on the device when prompted).
- Try unplugging and reconnecting the USB cable.

### "Xcode build failed"

- Run `xcode-select --install` to ensure command-line tools are current.
- Open Xcode and check for pending updates or license agreements.
- Clean the build: `xcodebuild clean` before rebuilding.

### "App installation failed on device"

- Verify the IPA is signed with a provisioning profile that includes the device UDID.
- For free developer accounts, you can only install on up to 3 devices.
- Check device storage: **Settings** → **General** → **iPhone Storage**.

### "Session creation timed out"

- Increase the WDA startup timeout: add `appium:wdaStartupRetries: 4` to capabilities.
- Ensure no other Appium sessions are active on the same device.
- Restart the device and try again.

### Tests pass on Android but fail on iOS

- Check for platform-specific UI differences (e.g., different element hierarchy).
- Verify accessibility IDs match between platforms.
- iOS may have additional system alerts (notifications, tracking) — use `appium:autoAcceptAlerts: true`.

---

## Summary

| Step | Action | Tool/File |
|------|--------|-----------|
| 1 | Install Xcode + CLI tools | Mac App Store + `xcode-select --install` |
| 2 | Install XCUITest driver | `appium driver install xcuitest` |
| 3 | Build & sign WebDriverAgent | Xcode → WebDriverAgent.xcodeproj |
| 4 | Discover device UDID | `xcrun xctrace list devices` |
| 5 | Add iOS configuration | `config/ios_device.yaml` or env vars |
| 6 | Start Appium | `appium --port 4723` |
| 7 | Run tests | `pytest tests/check_scripts/ -v` |

The framework's use of accessibility IDs and configuration-driven driver creation means that most tests can run on iOS without modification. Only platform-specific locator fallbacks (XPath, resource-id) would need iOS equivalents.
