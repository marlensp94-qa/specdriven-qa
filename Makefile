# =============================================================================
# Demo_QA — Makefile
# =============================================================================
# Convenience commands for common development tasks.
# Usage: make <target>
# =============================================================================

.PHONY: help install test unit smoke regression lint format clean report check-env

# Default target
help: ## Show this help message
	@echo "Demo_QA — Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Setup
# =============================================================================

install: ## Install all Python dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-hooks: ## Install pre-commit hooks
	pre-commit install

# =============================================================================
# Testing
# =============================================================================

test: ## Run all unit and property-based tests
	pytest tests/unit/ -v

unit: ## Run unit tests only (alias for test)
	pytest tests/unit/ -v

smoke: ## Run smoke tests (requires emulator + Appium)
	pytest tests/check_scripts/ -m smoke -v

regression: ## Run regression tests (requires emulator + Appium)
	pytest tests/check_scripts/ -m regression -v

all-tests: ## Run all check scripts (requires emulator + Appium)
	pytest tests/check_scripts/ -v

coverage: ## Run tests with coverage report
	pytest tests/unit/ --cov=framework --cov-report=html --cov-report=term-missing

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run linter (ruff)
	ruff check framework/ tests/

format: ## Auto-format code (ruff)
	ruff format framework/ tests/

format-check: ## Check formatting without modifying files
	ruff format --check framework/ tests/

typecheck: ## Run type checking (mypy)
	mypy framework/ --ignore-missing-imports

# =============================================================================
# Environment Verification
# =============================================================================

check-env: ## Verify all prerequisites are installed
	@echo "Checking prerequisites..."
	@echo -n "  Python: " && python3 --version
	@echo -n "  pip: " && pip --version | head -c 30 && echo ""
	@echo -n "  pytest: " && pytest --version 2>/dev/null || echo "NOT INSTALLED"
	@echo -n "  Appium: " && appium --version 2>/dev/null || echo "NOT INSTALLED"
	@echo -n "  ADB: " && adb --version 2>/dev/null | head -1 || echo "NOT INSTALLED"
	@echo -n "  Node: " && node --version 2>/dev/null || echo "NOT INSTALLED"
	@echo ""
	@echo "Checking emulator..."
	@adb devices 2>/dev/null | grep -q "device$$" && echo "  ✓ Emulator/device connected" || echo "  ✗ No device connected"
	@echo ""
	@echo "Checking Appium server..."
	@curl -s http://localhost:4723/status > /dev/null 2>&1 && echo "  ✓ Appium server running" || echo "  ✗ Appium server not running"

# =============================================================================
# Reports and Cleanup
# =============================================================================

report: ## Open the latest HTML report
	@latest=$$(ls -t reports/report_*.html 2>/dev/null | head -1); \
	if [ -n "$$latest" ]; then \
		open "$$latest"; \
	else \
		echo "No reports found. Run tests first: make smoke"; \
	fi

clean: ## Remove generated files (reports, logs, caches)
	rm -rf reports/*.html reports/*.png
	rm -rf logs/*.log
	rm -rf .pytest_cache
	rm -rf framework/__pycache__ tests/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned generated files."

clean-all: clean ## Remove everything including .hypothesis database
	rm -rf .hypothesis
	@echo "Cleaned all generated files including Hypothesis database."
