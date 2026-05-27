# SDD Training Guide — Table of Contents

## Overview

This guide documents the complete Spec-Driven Development (SDD) process applied to QA, using the Swag Labs Mobile application as a worked example. Follow the phases sequentially from Phase 0 through Phase 7 to learn the full methodology.

## Phases

| Phase | Title | Document Location | Description |
|-------|-------|-------------------|-------------|
| 0 | App Analysis | `docs/01-sdd-guide/phase-0-app-analysis.md` | Analyze the target application, identify features, screens, and flows |
| 1 | Test Planning | `docs/01-sdd-guide/phase-1-test-planning.md` | Define scope, approach, entry/exit criteria, and risk assessment |
| 2 | Test Case Design | `docs/01-sdd-guide/phase-2-test-case-design.md` | Design test cases using methodology and decision matrix |
| 3 | Test Library Management | `docs/01-sdd-guide/phase-3-test-library-management.md` | Organize, maintain, and review the test case library |
| 4 | Automation Framework Setup | `docs/01-sdd-guide/phase-4-automation-framework.md` | Set up the framework, POM pattern, and configuration |
| 5 | Test Automation | `docs/01-sdd-guide/phase-5-test-automation.md` | Write check scripts, flows, and apply markers |
| 6 | Execution and Reporting | `docs/01-sdd-guide/phase-6-execution-reporting.md` | Run tests, generate HTML reports, analyze failures |
| 7 | Maintenance and CI/CD | `docs/01-sdd-guide/phase-7-maintenance-cicd.md` | Maintain tests, integrate with CI/CD pipelines |

## How to Use This Guide

1. Start at Phase 0 and work through each phase in order
2. Each phase document includes prerequisites — verify them before starting
3. Complete the deliverables checklist at the end of each phase before moving on
4. Use the worked examples as templates for your own projects
5. Reference the Process Journal (`docs/02-process-journal/`) for real prompts and decisions made during this project's creation

## Prerequisites for the Entire Guide

- Python 3.8+ installed
- Android Studio with Android SDK
- Appium 2.x with UiAutomator2 driver
- Basic familiarity with pytest and Python
- Access to the Swag Labs Mobile APK (Sauce Labs GitHub)

## Related Documents

- Setup Guide: `docs/00-overview/setup-guide.md`
- Quality Standards: `docs/standards/quality-checklist.md`
- Field Requirements: `docs/standards/field-requirements.md`
- Process Journal: `docs/02-process-journal/process-journal.md`
- Extensibility Docs: `docs/03-extensibility/`
