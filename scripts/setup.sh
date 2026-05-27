#!/usr/bin/env bash
# =============================================================================
# Demo_QA — Setup Script
# =============================================================================
# This script creates a Python virtual environment, installs all dependencies,
# and verifies that the environment is ready for test execution.
#
# Usage:
#   chmod +x scripts/setup.sh
#   ./scripts/setup.sh
#
# What it does:
#   1. Checks Python 3.8+ is available
#   2. Creates a virtual environment (.venv/)
#   3. Installs production + dev dependencies
#   4. Verifies key packages are installed
#   5. Checks for external tools (Appium, ADB, Node)
#   6. Prints a summary of what's ready and what's missing
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the project root (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Demo_QA — Environment Setup                        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

cd "$PROJECT_ROOT"

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Check Python version
# ─────────────────────────────────────────────────────────────────────────────
echo -e "${BLUE}[1/5]${NC} Checking Python installation..."

PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &> /dev/null; then
        version=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}  ✗ Python 3.8+ not found.${NC}"
    echo "    Please install Python 3.8 or higher:"
    echo "    - macOS: brew install python@3.10"
    echo "    - Ubuntu: sudo apt install python3 python3-venv python3-pip"
    echo "    - Windows: https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}  ✓ Found: $($PYTHON_CMD --version)${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Create virtual environment
# ─────────────────────────────────────────────────────────────────────────────
echo -e "${BLUE}[2/5]${NC} Setting up virtual environment..."

VENV_DIR="$PROJECT_ROOT/.venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}  → Virtual environment already exists at .venv/${NC}"
    echo "    Reusing existing environment."
else
    echo "  Creating .venv/ ..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "${GREEN}  ✓ Virtual environment created${NC}"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}  ✓ Virtual environment activated${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Install dependencies
# ─────────────────────────────────────────────────────────────────────────────
echo -e "${BLUE}[3/5]${NC} Installing dependencies..."

echo "  Installing production dependencies (requirements.txt)..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "  Installing development dependencies (requirements-dev.txt)..."
pip install -r requirements-dev.txt --quiet

echo -e "${GREEN}  ✓ All Python dependencies installed${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Verify Python packages
# ─────────────────────────────────────────────────────────────────────────────
echo -e "${BLUE}[4/5]${NC} Verifying installed packages..."

PACKAGES_OK=true
for pkg in pytest hypothesis yaml appium jinja2 ruff; do
    if python -c "import $pkg" 2>/dev/null || python -c "import ${pkg//-/_}" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $pkg"
    else
        echo -e "  ${RED}✗${NC} $pkg — NOT FOUND"
        PACKAGES_OK=false
    fi
done

# Special check for appium (it's Appium-Python-Client)
if python -c "from appium import webdriver" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} appium-python-client"
else
    echo -e "  ${RED}✗${NC} appium-python-client — NOT FOUND"
    PACKAGES_OK=false
fi

if [ "$PACKAGES_OK" = true ]; then
    echo -e "${GREEN}  ✓ All Python packages verified${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Check external tools
# ─────────────────────────────────────────────────────────────────────────────
echo -e "${BLUE}[5/5]${NC} Checking external tools..."

TOOLS_MISSING=0

# Node.js
if command -v node &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Node.js: $(node --version)"
else
    echo -e "  ${YELLOW}⚠${NC} Node.js: NOT FOUND (required for Appium)"
    echo "    Install: brew install node (macOS) or https://nodejs.org/"
    TOOLS_MISSING=$((TOOLS_MISSING + 1))
fi

# Appium
if command -v appium &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Appium: $(appium --version 2>/dev/null)"
else
    echo -e "  ${YELLOW}⚠${NC} Appium: NOT FOUND"
    echo "    Install: npm install -g appium"
    TOOLS_MISSING=$((TOOLS_MISSING + 1))
fi

# ADB (Android SDK)
if command -v adb &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} ADB: $(adb --version 2>/dev/null | head -1)"
else
    echo -e "  ${YELLOW}⚠${NC} ADB: NOT FOUND (Android SDK Platform-Tools)"
    echo "    Install Android Studio: https://developer.android.com/studio"
    TOOLS_MISSING=$((TOOLS_MISSING + 1))
fi

# Emulator
if command -v emulator &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Android Emulator: available"
else
    echo -e "  ${YELLOW}⚠${NC} Android Emulator: NOT IN PATH"
    echo "    Add to PATH: export PATH=\$PATH:\$ANDROID_HOME/emulator"
    TOOLS_MISSING=$((TOOLS_MISSING + 1))
fi

# APK file
if [ -f "$PROJECT_ROOT/apps/mda-2.2.0-25.apk" ]; then
    echo -e "  ${GREEN}✓${NC} APK: apps/mda-2.2.0-25.apk ($(du -h apps/mda-2.2.0-25.apk | cut -f1))"
else
    echo -e "  ${YELLOW}⚠${NC} APK: NOT FOUND in apps/"
    echo "    Download from: https://github.com/saucelabs/my-demo-app-android/releases"
    TOOLS_MISSING=$((TOOLS_MISSING + 1))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Setup Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Python environment: ${GREEN}Ready${NC}"
echo -e "  Virtual env path:   ${PROJECT_ROOT}/.venv/"
echo ""

if [ $TOOLS_MISSING -eq 0 ]; then
    echo -e "  External tools:     ${GREEN}All present${NC}"
    echo ""
    echo -e "${GREEN}  ✓ Environment is fully configured!${NC}"
    echo ""
    echo "  Next steps:"
    echo "    1. Activate the venv:  source .venv/bin/activate"
    echo "    2. Run unit tests:     make test"
    echo "    3. Run smoke tests:    ./scripts/run_tests.sh"
else
    echo -e "  External tools:     ${YELLOW}$TOOLS_MISSING missing (see above)${NC}"
    echo ""
    echo -e "${YELLOW}  ⚠ Python environment is ready, but some external tools are missing.${NC}"
    echo "    Unit tests will work:  make test"
    echo "    Smoke/regression tests require the missing tools above."
fi

echo ""
echo "  To activate the virtual environment in future sessions:"
echo "    source .venv/bin/activate"
echo ""
