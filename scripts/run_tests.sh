#!/usr/bin/env bash
# =============================================================================
# Demo_QA — Interactive Test Runner
# =============================================================================
# This script provides an interactive menu to:
#   1. Select an Android emulator device
#   2. Start the emulator and Appium server
#   3. Choose which tests to run (by category, marker, component, etc.)
#   4. Execute the selected tests and show results
#
# Usage:
#   chmod +x scripts/run_tests.sh
#   ./scripts/run_tests.sh
#
# Requirements:
#   - Virtual environment activated (run scripts/setup.sh first)
#   - Android SDK installed with at least one AVD configured
#   - Appium installed (npm install -g appium)
#   - UiAutomator2 driver installed (appium driver install uiautomator2)
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Track background processes for cleanup
APPIUM_PID=""
EMULATOR_PID=""

# ─────────────────────────────────────────────────────────────────────────────
# Cleanup function — kills background processes on exit
# ─────────────────────────────────────────────────────────────────────────────
cleanup() {
    echo ""
    echo -e "${BLUE}Cleaning up...${NC}"
    if [ -n "$APPIUM_PID" ] && kill -0 "$APPIUM_PID" 2>/dev/null; then
        echo "  Stopping Appium server (PID: $APPIUM_PID)..."
        kill "$APPIUM_PID" 2>/dev/null || true
    fi
    # Note: We don't kill the emulator by default — user may want it running
    echo -e "${GREEN}  Done.${NC}"
}
trap cleanup EXIT

# ─────────────────────────────────────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────────────────────────────────────

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          Demo_QA — Interactive Test Runner                   ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${CYAN}── $1 ──${NC}"
    echo ""
}

prompt_choice() {
    local prompt="$1"
    local default="$2"
    echo -ne "${BOLD}$prompt${NC}"
    if [ -n "$default" ]; then
        echo -ne " [${default}]: "
    else
        echo -ne ": "
    fi
    read -r choice
    if [ -z "$choice" ] && [ -n "$default" ]; then
        choice="$default"
    fi
    echo "$choice"
}

wait_for_device() {
    local timeout=120
    local elapsed=0
    echo -n "  Waiting for emulator to boot"
    while [ $elapsed -lt $timeout ]; do
        if adb shell getprop sys.boot_completed 2>/dev/null | grep -q "1"; then
            echo ""
            echo -e "  ${GREEN}✓ Emulator is ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 3
        elapsed=$((elapsed + 3))
    done
    echo ""
    echo -e "  ${RED}✗ Emulator did not boot within ${timeout}s${NC}"
    return 1
}

wait_for_appium() {
    local timeout=30
    local elapsed=0
    echo -n "  Waiting for Appium server"
    while [ $elapsed -lt $timeout ]; do
        if curl -s http://localhost:4723/status 2>/dev/null | grep -q "ready"; then
            echo ""
            echo -e "  ${GREEN}✓ Appium server is ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        elapsed=$((elapsed + 2))
    done
    echo ""
    echo -e "  ${RED}✗ Appium server did not start within ${timeout}s${NC}"
    return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# Step 0: Pre-flight checks
# ─────────────────────────────────────────────────────────────────────────────

print_header

echo -e "${BLUE}Pre-flight checks...${NC}"

# Check virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
        echo -e "  ${YELLOW}⚠ Virtual environment not active. Activating...${NC}"
        source "$PROJECT_ROOT/.venv/bin/activate"
    else
        echo -e "  ${RED}✗ No virtual environment found. Run scripts/setup.sh first.${NC}"
        exit 1
    fi
fi
echo -e "  ${GREEN}✓${NC} Python venv active: $VIRTUAL_ENV"

# Check pytest
if ! command -v pytest &> /dev/null; then
    echo -e "  ${RED}✗ pytest not found. Run: pip install -r requirements.txt${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} pytest available"

# Check Appium
if ! command -v appium &> /dev/null; then
    echo -e "  ${RED}✗ Appium not found. Run: npm install -g appium${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Appium available"

# Check ADB
if ! command -v adb &> /dev/null; then
    echo -e "  ${RED}✗ ADB not found. Install Android SDK Platform-Tools.${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} ADB available"

# Check emulator command
if ! command -v emulator &> /dev/null; then
    echo -e "  ${RED}✗ emulator command not found. Add \$ANDROID_HOME/emulator to PATH.${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Android emulator available"

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Select emulator device
# ─────────────────────────────────────────────────────────────────────────────

print_section "Step 1: Select Android Emulator"

# Get list of available AVDs
AVDS=($(emulator -list-avds 2>/dev/null))

if [ ${#AVDS[@]} -eq 0 ]; then
    echo -e "${RED}  No AVDs found. Create one in Android Studio → Device Manager.${NC}"
    echo "  Recommended: Pixel 4, API 30, Google APIs, x86_64"
    exit 1
fi

echo "  Available emulators:"
echo ""
for i in "${!AVDS[@]}"; do
    echo -e "    ${BOLD}$((i + 1))${NC}) ${AVDS[$i]}"
done
echo ""

# Check if an emulator is already running
DEVICE_RUNNING=$(adb devices 2>/dev/null | grep -c "emulator-" || true)
if [ "$DEVICE_RUNNING" -gt 0 ]; then
    RUNNING_DEVICE=$(adb devices 2>/dev/null | grep "emulator-" | head -1 | awk '{print $1}')
    echo -e "  ${GREEN}→ Emulator already running: $RUNNING_DEVICE${NC}"
    echo ""
    USE_RUNNING=$(prompt_choice "  Use the running emulator? (y/n)" "y")
    if [[ "$USE_RUNNING" =~ ^[Yy] ]]; then
        SELECTED_AVD="(already running)"
        SKIP_EMULATOR_START=true
    fi
fi

if [ -z "$SKIP_EMULATOR_START" ]; then
    if [ ${#AVDS[@]} -eq 1 ]; then
        SELECTED_AVD="${AVDS[0]}"
        echo -e "  Auto-selecting: ${GREEN}$SELECTED_AVD${NC} (only one available)"
    else
        AVD_CHOICE=$(prompt_choice "  Select emulator (1-${#AVDS[@]})" "1")
        AVD_INDEX=$((AVD_CHOICE - 1))
        if [ $AVD_INDEX -lt 0 ] || [ $AVD_INDEX -ge ${#AVDS[@]} ]; then
            echo -e "${RED}  Invalid selection. Exiting.${NC}"
            exit 1
        fi
        SELECTED_AVD="${AVDS[$AVD_INDEX]}"
    fi
    echo -e "  Selected: ${GREEN}$SELECTED_AVD${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Start emulator (if needed)
# ─────────────────────────────────────────────────────────────────────────────

if [ -z "$SKIP_EMULATOR_START" ]; then
    print_section "Step 2: Starting Emulator"

    echo "  Launching: $SELECTED_AVD"
    emulator -avd "$SELECTED_AVD" -no-snapshot-load -no-audio &>/dev/null &
    EMULATOR_PID=$!
    echo "  Emulator PID: $EMULATOR_PID"

    if ! wait_for_device; then
        echo -e "${RED}  Failed to start emulator. Check Android Studio.${NC}"
        exit 1
    fi
else
    print_section "Step 2: Emulator (skipped — already running)"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Start Appium server
# ─────────────────────────────────────────────────────────────────────────────

print_section "Step 3: Starting Appium Server"

# Check if Appium is already running
if curl -s http://localhost:4723/status 2>/dev/null | grep -q "ready"; then
    echo -e "  ${GREEN}→ Appium server already running on port 4723${NC}"
else
    echo "  Starting Appium on port 4723..."
    appium --port 4723 --log-level error &>/dev/null &
    APPIUM_PID=$!
    echo "  Appium PID: $APPIUM_PID"

    if ! wait_for_appium; then
        echo -e "${RED}  Failed to start Appium. Check: appium --version${NC}"
        exit 1
    fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Select tests to run
# ─────────────────────────────────────────────────────────────────────────────

print_section "Step 4: Select Tests to Run"

echo "  Choose a test selection mode:"
echo ""
echo -e "    ${BOLD}1${NC}) Smoke tests only (critical path — 3 tests)"
echo -e "    ${BOLD}2${NC}) Regression tests only (full coverage — 10 tests)"
echo -e "    ${BOLD}3${NC}) All tests (smoke + regression — 13 tests)"
echo -e "    ${BOLD}4${NC}) By component (authentication, cart, catalog, checkout)"
echo -e "    ${BOLD}5${NC}) By priority (critical, high, medium, low)"
echo -e "    ${BOLD}6${NC}) By test type (functional, smoke, negative, boundary)"
echo -e "    ${BOLD}7${NC}) By specific test case ID (e.g., T001, T005)"
echo -e "    ${BOLD}8${NC}) Unit/property tests only (no emulator needed)"
echo -e "    ${BOLD}9${NC}) Custom pytest expression"
echo ""

MODE=$(prompt_choice "  Select mode (1-9)" "1")

PYTEST_ARGS="tests/check_scripts/ -v --tb=short"

case "$MODE" in
    1)
        PYTEST_ARGS="tests/check_scripts/ -m smoke -v --tb=short"
        echo -e "  → Running: ${GREEN}Smoke tests${NC}"
        ;;
    2)
        PYTEST_ARGS="tests/check_scripts/ -m regression -v --tb=short"
        echo -e "  → Running: ${GREEN}Regression tests${NC}"
        ;;
    3)
        PYTEST_ARGS="tests/check_scripts/ -v --tb=short"
        echo -e "  → Running: ${GREEN}All tests${NC}"
        ;;
    4)
        echo ""
        echo "  Available components:"
        echo -e "    ${BOLD}a${NC}) authentication"
        echo -e "    ${BOLD}b${NC}) cart"
        echo -e "    ${BOLD}c${NC}) catalog"
        echo -e "    ${BOLD}d${NC}) checkout"
        echo ""
        COMP_CHOICE=$(prompt_choice "  Select component (a/b/c/d)" "a")
        case "$COMP_CHOICE" in
            a) COMPONENT="authentication" ;;
            b) COMPONENT="cart" ;;
            c) COMPONENT="catalog" ;;
            d) COMPONENT="checkout" ;;
            *) COMPONENT="$COMP_CHOICE" ;;
        esac
        PYTEST_ARGS="tests/check_scripts/ -k '$COMPONENT' -v --tb=short"
        echo -e "  → Running: ${GREEN}Component: $COMPONENT${NC}"
        ;;
    5)
        echo ""
        echo "  Available priorities:"
        echo -e "    ${BOLD}1${NC}) critical"
        echo -e "    ${BOLD}2${NC}) high"
        echo -e "    ${BOLD}3${NC}) medium"
        echo -e "    ${BOLD}4${NC}) low"
        echo ""
        PRIO_CHOICE=$(prompt_choice "  Select priority (1-4)" "1")
        case "$PRIO_CHOICE" in
            1) PRIORITY="critical" ;;
            2) PRIORITY="high" ;;
            3) PRIORITY="medium" ;;
            4) PRIORITY="low" ;;
            *) PRIORITY="$PRIO_CHOICE" ;;
        esac
        PYTEST_ARGS="tests/check_scripts/ -m \"priority('$PRIORITY')\" -v --tb=short"
        echo -e "  → Running: ${GREEN}Priority: $PRIORITY${NC}"
        ;;
    6)
        echo ""
        echo "  Available test types:"
        echo -e "    ${BOLD}1${NC}) functional"
        echo -e "    ${BOLD}2${NC}) smoke"
        echo -e "    ${BOLD}3${NC}) negative"
        echo -e "    ${BOLD}4${NC}) boundary"
        echo ""
        TYPE_CHOICE=$(prompt_choice "  Select test type (1-4)" "1")
        case "$TYPE_CHOICE" in
            1) TEST_TYPE="functional" ;;
            2) TEST_TYPE="smoke" ;;
            3) TEST_TYPE="negative" ;;
            4) TEST_TYPE="boundary" ;;
            *) TEST_TYPE="$TYPE_CHOICE" ;;
        esac
        PYTEST_ARGS="tests/check_scripts/ -m \"test_type('$TEST_TYPE')\" -v --tb=short"
        echo -e "  → Running: ${GREEN}Test type: $TEST_TYPE${NC}"
        ;;
    7)
        echo ""
        echo "  Available test case IDs: T001-T013"
        echo "  (Enter comma-separated IDs, e.g.: T001,T005,T010)"
        echo ""
        TC_IDS=$(prompt_choice "  Enter test case IDs" "T001")
        # Build -k expression from IDs
        K_EXPR=""
        IFS=',' read -ra IDS <<< "$TC_IDS"
        for id in "${IDS[@]}"; do
            id=$(echo "$id" | xargs) # trim whitespace
            if [ -n "$K_EXPR" ]; then
                K_EXPR="$K_EXPR or $id"
            else
                K_EXPR="$id"
            fi
        done
        PYTEST_ARGS="tests/check_scripts/ -k '$K_EXPR' -v --tb=short"
        echo -e "  → Running: ${GREEN}Test cases: $TC_IDS${NC}"
        ;;
    8)
        PYTEST_ARGS="tests/unit/ -v --tb=short"
        echo -e "  → Running: ${GREEN}Unit/property tests (no emulator needed)${NC}"
        ;;
    9)
        echo ""
        CUSTOM_EXPR=$(prompt_choice "  Enter custom pytest expression (e.g., '-m smoke -k login')" "")
        PYTEST_ARGS="tests/check_scripts/ $CUSTOM_EXPR -v --tb=short"
        echo -e "  → Running: ${GREEN}Custom: pytest $PYTEST_ARGS${NC}"
        ;;
    *)
        echo -e "${RED}  Invalid selection. Running smoke tests.${NC}"
        PYTEST_ARGS="tests/check_scripts/ -m smoke -v --tb=short"
        ;;
esac

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Execute tests
# ─────────────────────────────────────────────────────────────────────────────

print_section "Step 5: Executing Tests"

echo -e "  Command: ${CYAN}pytest $PYTEST_ARGS${NC}"
echo ""
echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"
echo ""

# Run pytest
eval "pytest $PYTEST_ARGS"
TEST_EXIT_CODE=$?

echo ""
echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# Step 6: Results summary
# ─────────────────────────────────────────────────────────────────────────────

print_section "Results"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "  ${GREEN}✓ All tests passed!${NC}"
else
    echo -e "  ${RED}✗ Some tests failed (exit code: $TEST_EXIT_CODE)${NC}"
fi

# Check for generated report
LATEST_REPORT=$(ls -t reports/report_*.html 2>/dev/null | head -1)
if [ -n "$LATEST_REPORT" ]; then
    echo ""
    echo -e "  HTML Report: ${CYAN}$LATEST_REPORT${NC}"
    echo ""
    OPEN_REPORT=$(prompt_choice "  Open report in browser? (y/n)" "y")
    if [[ "$OPEN_REPORT" =~ ^[Yy] ]]; then
        open "$LATEST_REPORT" 2>/dev/null || xdg-open "$LATEST_REPORT" 2>/dev/null || echo "  (Could not open browser automatically)"
    fi
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "  ${BOLD}Session complete.${NC}"
echo ""
echo "  Useful commands:"
echo "    make test          — Run unit tests"
echo "    make smoke         — Run smoke tests"
echo "    make report        — Open latest report"
echo "    make check-env     — Verify environment"
echo ""

exit $TEST_EXIT_CODE
