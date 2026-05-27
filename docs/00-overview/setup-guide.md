# Setup Guide

This guide walks you through installing and configuring all prerequisites for the Demo_QA project. Follow each section in order. By the end, you will have a working environment capable of running automated mobile tests against the Swag Labs Android application on an emulator.

## Supported Operating Systems

| OS | Version | Notes |
|----|---------|-------|
| macOS | 12 (Monterey) or later | Recommended for development |
| Windows | 10/11 (64-bit) | Use PowerShell or Git Bash for commands |
| Linux | Ubuntu 20.04+ / Fedora 36+ | Any distro with glibc 2.31+ |

---

## 1. Install Python 3.8+

Python 3.8 or higher is required. Python 3.10+ is recommended.

### macOS

```bash
# Using Homebrew
brew install python@3.10

# Verify
python3 --version
```

### Windows

1. Download the installer from https://www.python.org/downloads/
2. Run the installer — check **"Add Python to PATH"** during installation
3. Open a new terminal and verify:

```powershell
python --version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Verify
python3 --version
```

### Create a Virtual Environment

```bash
cd Demo_QA
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Install Android Studio and Android SDK

Android Studio provides the SDK, emulator, and AVD Manager needed to run tests.

### Installation

1. Download Android Studio from https://developer.android.com/studio
2. Run the installer and follow the setup wizard
3. During setup, ensure the following SDK components are selected:
   - **Android SDK Platform** (API 29 or higher)
   - **Android SDK Build-Tools**
   - **Android SDK Platform-Tools**
   - **Android Emulator**
   - **Google APIs System Image** for your target API level

### Configure Environment Variables

Add the following to your shell profile (`~/.zshrc`, `~/.bashrc`, or Windows System Environment Variables):

**macOS/Linux:**

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk   # macOS
# export ANDROID_HOME=$HOME/Android/Sdk         # Linux

export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

**Windows (PowerShell profile or System Variables):**

```powershell
$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"
$env:PATH += ";$env:ANDROID_HOME\emulator;$env:ANDROID_HOME\platform-tools"
```

### Verify SDK Installation

```bash
adb --version
emulator -list-avds
```

---

## 3. Create and Configure an Android Emulator

The project targets **Android API 29** (Android 10) or higher with a **Google APIs** system image.

### Step-by-Step (AVD Manager)

1. Open Android Studio → **Tools** → **Device Manager** (or **AVD Manager**)
2. Click **Create Virtual Device**
3. Select a device profile:
   - Recommended: **Pixel 4** or **Pixel 5** (standard screen size, well-tested)
4. Select a system image:
   - Tab: **Recommended** or **x86 Images**
   - Target: **API Level 29** or higher (API 30, 31, 33 all work)
   - Type: **Google APIs** (not Google Play — Google APIs is sufficient and avoids Play Store sign-in)
   - ABI: **x86_64** (best performance with hardware acceleration)
5. Click **Download** if the image is not yet installed
6. Name the AVD (e.g., `Pixel_4_API_30`) — this name goes in `config/emulators.yaml`
7. In **Advanced Settings**:
   - RAM: 2048 MB minimum (4096 MB recommended)
   - Internal Storage: 2048 MB minimum
   - Enable **Hardware - GLES 2.0** for GPU acceleration
8. Click **Finish**

### Verify Emulator

```bash
# List available AVDs
emulator -list-avds

# Start the emulator (headless or with GUI)
emulator -avd Pixel_4_API_30

# In another terminal, verify device is connected
adb devices
# Expected output:
# List of devices attached
# emulator-5554   device
```

### Hardware Acceleration

- **macOS**: Hardware acceleration via Hypervisor.framework (enabled by default)
- **Windows**: Enable Intel HAXM or Windows Hypervisor Platform (WHPx) in BIOS
- **Linux**: Enable KVM (`sudo apt install qemu-kvm` and add user to `kvm` group)

---

## 4. Install Appium 2.x

Appium 2.x is the test automation server that communicates with the Android emulator.

### Prerequisites

- **Node.js 16+** is required for Appium. Install from https://nodejs.org/ or via a version manager (nvm, fnm).

### Install Appium

```bash
# Install Appium globally
npm install -g appium@latest

# Verify installation
appium --version
# Expected: 2.x.x (e.g., 2.4.1)
```

### Install UiAutomator2 Driver

```bash
# Install the Android automation driver
appium driver install uiautomator2

# Verify driver is installed
appium driver list --installed
# Expected output includes:
# - uiautomator2@x.x.x [installed (npm)]
```

### Start Appium Server

```bash
# Start on default port (4723)
appium

# Or specify a port
appium --port 4723

# Expected output:
# [Appium] Welcome to Appium v2.x.x
# [Appium] Appium REST http interface listener started on http://0.0.0.0:4723
```

> **Note:** Keep the Appium server running in a separate terminal while executing tests.

---

## 5. Download the Swag Labs APK

The Swag Labs Mobile app is a public demo application provided by Sauce Labs.

### Download Instructions

1. Navigate to the Sauce Labs sample apps GitHub repository:
   https://github.com/saucelabs/sample-app-mobile/releases
2. Download the Android APK from the latest release:
   - Expected filename: `Android-MyDemoAppReset.apk` (or `swag-labs.apk` depending on release)
   - Look for the `.apk` file under the release assets
3. Place the downloaded APK in the project's `apps/` directory:

```bash
# From the Demo_QA project root
mv ~/Downloads/Android-MyDemoAppReset.apk apps/

# Verify
ls apps/
# Expected: Android-MyDemoAppReset.apk
```

4. Update `config/apps.yaml` if the filename differs from the default:

```yaml
app:
  apk_path: "apps/Android-MyDemoAppReset.apk"
  package_name: "com.swaglabsmobileapp"
  activity_name: "com.swaglabsmobileapp.MainActivity"
  app_version: "1.0"
```

### Target Directory Structure

```
Demo_QA/
└── apps/
    └── Android-MyDemoAppReset.apk   ← Place APK here
```

> **Important:** The `apps/` directory is included in `.gitignore`. The APK must be downloaded manually by each developer.

---

## 6. Verification Procedure

After completing all setup steps, verify your environment by running a single smoke test.

### Pre-flight Checklist

Before running the verification test, confirm:

- [ ] Python virtual environment is activated
- [ ] Android emulator is running (`adb devices` shows a connected device)
- [ ] Appium server is running (`http://localhost:4723`)
- [ ] Swag Labs APK is in the `apps/` directory
- [ ] `config/emulators.yaml` has the correct AVD name and Appium URL

### Run the Smoke Test

```bash
# From the Demo_QA project root, with venv activated
pytest tests/check_scripts/check_T001_login_valid_credentials.py -v --tb=short
```

### Expected Output — Success

```
========================= test session starts ==========================
platform darwin -- Python 3.10.x, pytest-7.4.x
collected 1 item

tests/check_scripts/check_T001_login_valid_credentials.py::check_T001_login_valid_credentials PASSED

========================= 1 passed in 15.23s ===========================
```

Key indicators of success:
- Test status is **PASSED**
- No connection errors or timeouts
- An HTML report is generated in `reports/`

### Expected Output — Failure Scenarios

**Appium server not running:**

```
FAILED tests/check_scripts/check_T001_login_valid_credentials.py::check_T001_login_valid_credentials
E   ConnectionError: Could not connect to Appium server at http://localhost:4723.
E   Verify that Appium is running: appium --port 4723
```

**Emulator not running:**

```
FAILED tests/check_scripts/check_T001_login_valid_credentials.py::check_T001_login_valid_credentials
E   WebDriverException: An unknown server-side error occurred while processing the command.
E   Original error: Could not find a connected Android device
```

**APK not found:**

```
FAILED tests/check_scripts/check_T001_login_valid_credentials.py::check_T001_login_valid_credentials
E   ConfigurationError: Configuration error in 'config/apps.yaml': APK file not found at 'apps/Android-MyDemoAppReset.apk'
```

---

## 7. Troubleshooting

### Tool Not Found in PATH

| Symptom | Cause | Solution |
|---------|-------|----------|
| `python3: command not found` | Python not in PATH | Re-run installer with "Add to PATH" checked, or add manually to shell profile |
| `adb: command not found` | Android SDK platform-tools not in PATH | Add `$ANDROID_HOME/platform-tools` to PATH (see Section 2) |
| `emulator: command not found` | Android emulator not in PATH | Add `$ANDROID_HOME/emulator` to PATH |
| `appium: command not found` | Appium not installed globally or npm bin not in PATH | Run `npm install -g appium` or add `$(npm bin -g)` to PATH |
| `node: command not found` | Node.js not installed | Install Node.js 16+ from https://nodejs.org/ |

**General fix:** After modifying PATH, restart your terminal or run `source ~/.zshrc` (macOS/Linux).

### Version Mismatch

| Symptom | Cause | Solution |
|---------|-------|----------|
| `SyntaxError` on import | Python version < 3.8 | Upgrade Python: `brew upgrade python` or download newer installer |
| Appium driver errors | Appium 1.x installed instead of 2.x | Uninstall and reinstall: `npm uninstall -g appium && npm install -g appium@latest` |
| `UiAutomator2 not found` | Driver not installed for Appium 2.x | Run `appium driver install uiautomator2` |
| pytest collection errors | pytest version < 7.0 | Upgrade: `pip install --upgrade pytest` |
| `InvalidArgumentException` in capabilities | Appium 2.x requires `appium:` prefix | Ensure capabilities use `appium:automationName`, `appium:platformVersion`, etc. |

**Check all versions at once:**

```bash
python3 --version          # Expected: 3.8+
node --version             # Expected: 16+
appium --version           # Expected: 2.x.x
adb --version              # Expected: any recent version
pytest --version           # Expected: 7.0+
appium driver list --installed  # Expected: uiautomator2 listed
```

### Appium-Emulator Connection Failure

| Symptom | Cause | Solution |
|---------|-------|----------|
| `Could not connect to Appium server` | Appium not running | Start Appium: `appium --port 4723` |
| `Could not find a connected Android device` | Emulator not running or ADB not detecting it | Start emulator and run `adb devices` to confirm |
| `Session not created: ... system image` | Wrong system image (non-Google APIs) | Recreate AVD with Google APIs system image |
| `ECONNREFUSED 127.0.0.1:4723` | Port mismatch between config and Appium | Ensure `config/emulators.yaml` port matches Appium startup port |
| Timeout waiting for device | Emulator still booting | Wait for emulator to fully boot (home screen visible), then retry |
| `adb server version doesn't match` | Multiple ADB versions on system | Kill ADB server (`adb kill-server`) and restart; ensure only one SDK installation |

**Connection diagnostic steps:**

```bash
# 1. Verify emulator is running and detected
adb devices
# Should show: emulator-5554   device

# 2. Verify Appium is listening
curl http://localhost:4723/status
# Should return JSON with "ready": true

# 3. Verify UiAutomator2 driver is available
appium driver list --installed
# Should list uiautomator2

# 4. Try a manual session creation (optional)
# Use Appium Inspector or curl to create a test session
```

**If all else fails:**

1. Kill all ADB and emulator processes:
   ```bash
   adb kill-server
   killall qemu-system-x86_64  # macOS/Linux
   ```
2. Restart the emulator from AVD Manager
3. Wait for the home screen to appear
4. Restart Appium server
5. Run `adb devices` to confirm connection
6. Retry the smoke test

---

## Quick Reference

| Component | Minimum Version | Install Command |
|-----------|----------------|-----------------|
| Python | 3.8+ | `brew install python@3.10` / python.org installer |
| Node.js | 16+ | `brew install node` / nodejs.org installer |
| Appium | 2.0+ | `npm install -g appium@latest` |
| UiAutomator2 | latest | `appium driver install uiautomator2` |
| Android SDK | API 29+ | Via Android Studio SDK Manager |
| Android Studio | latest | https://developer.android.com/studio |
| pytest | 7.0+ | `pip install pytest` (via requirements.txt) |

---

## Next Steps

Once verification passes:

1. Explore the project structure in the [README](../../README.md)
2. Read the [SDD Training Guide](../01-sdd-guide/00-table-of-contents.md) to understand the methodology
3. Run the full smoke suite: `pytest tests/check_scripts/ -m smoke -v`
4. Review the generated HTML report in `reports/`
