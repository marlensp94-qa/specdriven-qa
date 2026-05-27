# Demo_QA — QA Training Showroom

A comprehensive QA training and demonstration project that implements the Spec-Driven Development (SDD) process applied to mobile test automation. Built around the **Swag Labs Mobile** app (Sauce Labs public demo APK) running on Android emulators, this project packages a mini automation framework, a manual test case library, process documentation, and an SDD training guide into a self-contained learning environment.

## What's Inside

- **Mini Automation Framework** — Python + Appium + pytest using the Page Object Model pattern
- **Manual Test Case Library** — 20+ structured test cases organized by feature (login, catalog, cart, checkout)
- **Automated Test Suite** — Smoke and regression check scripts mapped to manual test cases
- **SDD Training Guide** — Phase-by-phase documentation of the entire QA lifecycle (Phase 0–7)
- **Process Journal** — Real prompts, decisions, and iterations that produced this project
- **HTML Reporting** — Self-contained test execution reports with pass/fail/skip metrics

## Directory Structure

```
Demo_QA/
├── apps/                       # APK files (Swag Labs Mobile)
├── config/                     # YAML configuration files
│   ├── apps.yaml               #   App package, activity, APK path
│   ├── emulators.yaml          #   Emulator name, platform version, Appium URL
│   ├── integrations.yaml       #   Jira/Zephyr placeholder credentials
│   └── README.md               #   Configuration parameter reference
├── docs/                       # Project documentation
│   ├── 00-overview/            #   Setup guide, automation plan
│   ├── 01-sdd-guide/           #   SDD training guide (Phase 0–7)
│   ├── 02-process-journal/     #   Prompts, decisions, iterations
│   ├── 03-extensibility/       #   Real devices, iOS, Jira/Zephyr
│   └── standards/              #   Quality checklist, field requirements
├── framework/                  # Mini automation framework
│   ├── core/                   #   ConfigLoader, EmulatorManager
│   ├── integrations/           #   Jira/Zephyr placeholder modules
│   ├── pages/                  #   Page objects (BasePage + 7 screens)
│   ├── reporting/              #   HTML report generator
│   └── utils/                  #   Logger, markers, constants, coverage analyzer
├── logs/                       # Session log files (auto-generated)
├── reports/                    # HTML reports and failure screenshots (auto-generated)
├── test_library/               # Manual test case library
│   ├── login/                  #   Login test cases (TC_LOGIN_001–005)
│   ├── catalog/                #   Catalog test cases (TC_CATALOG_001–005)
│   ├── cart/                   #   Cart test cases (TC_CART_001–005)
│   ├── checkout/               #   Checkout test cases (TC_CHECKOUT_001–005)
│   ├── template.md             #   Test case template
│   └── coverage_analysis.md    #   Manual-to-automated mapping
├── tests/                      # Automated tests
│   ├── check_scripts/          #   Smoke and regression check scripts
│   ├── flows/                  #   Reusable multi-step test flows
│   ├── unit/                   #   Property-based and unit tests
│   ├── integration/            #   End-to-end tests (require emulator)
│   └── conftest.py             #   Fixtures (driver, login, reporting)
├── scripts/                    # Automation scripts
│   ├── setup.sh                #   One-command environment setup
│   └── run_tests.sh            #   Interactive test runner
├── pytest.ini                  # pytest configuration
├── requirements.txt            # Pinned Python dependencies
└── README.md                   # This file
```

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.8+ | Runtime and test execution |
| Android Studio | Latest | Emulator management and SDK |
| Android SDK | API 29+ (Android 10+) | Platform tools and system images |
| Appium | 2.x | Mobile automation server |
| UiAutomator2 Driver | Latest | Android automation engine |
| Node.js | 16+ | Required by Appium |
| Java JDK | 11+ | Required by Android SDK |

## Setup Instructions

> **Quick option:** Run `./scripts/setup.sh` to automate steps 1-3 below.

Follow these steps to go from clone to running a test:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Demo_QA
   ```

2. **Create a Python virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   # .venv\Scripts\activate    # Windows
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Appium and UiAutomator2 driver**
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```

5. **Set up Android Studio and create an emulator**
   - Open Android Studio → Virtual Device Manager
   - Create a device with API 29+ and Google APIs system image
   - Start the emulator

6. **Download the Swag Labs APK**
   - Get the APK from the [Sauce Labs GitHub](https://github.com/saucelabs/my-demo-app-android/releases)
   - Download `mda-2.2.0-25.apk` (or latest version)
   - Place it in the `apps/` directory

7. **Update configuration** (if needed)
   - Edit `config/apps.yaml` to set the correct APK path
   - Edit `config/emulators.yaml` to match your emulator name and Appium URL

8. **Start the Appium server**
   ```bash
   appium
   ```

9. **Run the unit/property tests** (no emulator required)
   ```bash
   pytest tests/unit/ --run
   ```

10. **Run a smoke test** (requires running emulator + Appium)
    ```bash
    pytest tests/check_scripts/check_T001_login_valid_credentials.py --run
    ```

## Quick Start (Automated Scripts)

For a fully automated setup and test execution experience, use the provided scripts:

### 1. Environment Setup (one-time)

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
- Verify Python 3.8+ is installed
- Create a virtual environment (`.venv/`)
- Install all production and development dependencies
- Check for external tools (Appium, ADB, Android Emulator)
- Report what's ready and what's missing

### 2. Interactive Test Runner

```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

This script provides a fully interactive experience:
- **Device selection** — Lists available AVDs and lets you choose which emulator to launch
- **Auto-start infrastructure** — Starts the emulator and Appium server automatically
- **Test filtering** — Choose tests by:
  - Scope (smoke / regression / all)
  - Component (authentication, cart, catalog, checkout)
  - Priority (critical, high, medium, low)
  - Test type (functional, negative, boundary)
  - Specific test case IDs (T001, T005, T010...)
  - Custom pytest expression
- **Results** — Shows results and offers to open the HTML report

## Running Tests (Manual)

```bash
# Run all unit and property-based tests (no emulator needed)
pytest tests/unit/

# Run smoke tests only
pytest -m smoke

# Run regression tests only
pytest -m regression

# Run a specific check script
pytest tests/check_scripts/check_T001_login_valid_credentials.py

# Generate HTML report (automatic after any test run)
# Reports are saved to reports/report_YYYYMMDD_HHMMSS.html
```

## Makefile Commands

```bash
make help          # Show all available commands
make install       # Install all dependencies
make test          # Run unit/property tests
make smoke         # Run smoke tests (requires emulator)
make regression    # Run regression tests (requires emulator)
make lint          # Run linter (ruff)
make format        # Auto-format code
make check-env     # Verify all prerequisites
make clean         # Remove generated files
make report        # Open latest HTML report
```

## Further Reading

- **Setup Guide**: `docs/00-overview/setup-guide.md` — Detailed installation and troubleshooting
- **Project Spec**: `docs/00-overview/spec/` — Requirements, design, and implementation tasks
- **SDD Training Guide**: `docs/01-sdd-guide/` — Complete Phase 0–7 walkthrough
- **Process Journal**: `docs/02-process-journal/process-journal.md` — Prompts, decisions, lessons learned
- **Configuration Reference**: `config/README.md` — All configuration parameters explained
- **Quality Standards**: `docs/standards/` — Test case quality checklist and field requirements
