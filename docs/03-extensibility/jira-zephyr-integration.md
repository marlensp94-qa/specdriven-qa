# Jira and Zephyr Scale Integration

## Overview

The Mini_Framework includes placeholder modules for integrating with Jira (issue tracking) and Zephyr Scale (test management). These modules demonstrate the integration pattern without requiring live credentials, allowing QA engineers to understand the data flow and enable real connectivity when a Jira instance becomes available.

**Current status:** Placeholder mode (all API calls are logged but not executed).

---

## Integration Flow

The integration follows a sequential flow from test execution through result reporting:

### Test Execution → Result Reporting Sequence

1. **Test execution completes** — pytest runs a check script (e.g., `check_T001_login_valid_credentials.py`)
2. **Result collection** — The conftest.py pytest hook collects the test result (pass/fail/skip), duration, and any failure traceback
3. **Jira issue lookup** (optional) — `JiraConnector.search_issues()` queries for related issues using JQL (e.g., finding open bugs linked to the tested feature)
4. **Zephyr execution reporting** — `ZephyrReporter.report_execution()` sends the test result to Zephyr Scale, associating it with the correct test case key and test cycle
5. **Issue creation on failure** (optional) — If a test fails and no existing bug is found, `JiraConnector.create_issue()` creates a new Bug issue in the project
6. **Report generation** — The HTML report is generated locally with all results, independent of the Jira/Zephyr reporting

### Step-by-Step Sequence

| Step | Component | Action | API Endpoint |
|------|-----------|--------|--------------|
| 1 | pytest | Execute check script | — |
| 2 | conftest.py | Collect result + metadata | — |
| 3 | JiraConnector | Search for related issues | `POST /rest/api/2/search` |
| 4 | ZephyrReporter | Report execution result | `POST /rest/atm/1.0/testresult` |
| 5 | JiraConnector | Create bug (on failure) | `POST /rest/api/2/issue` |
| 6 | ReportGenerator | Generate HTML report | — |

---

## Authentication Mechanism

### Jira Cloud Authentication

Jira Cloud uses **API token + email** authentication via HTTP Basic Auth:

- **Username:** The email address associated with your Atlassian account
- **API Token:** Generated at https://id.atlassian.com/manage-profile/security/api-tokens
- **Auth method:** HTTP Basic Authentication (`email:api_token` base64-encoded in the `Authorization` header)

### Zephyr Scale Authentication

Zephyr Scale Cloud uses a **Bearer token** in the `Authorization` header:

- **API Token:** Generated in Zephyr Scale settings (Apps → Zephyr Scale → API Access Tokens)
- **Auth method:** Bearer token (`Authorization: Bearer <token>`)

For Zephyr Scale Server (on-premise), the Jira API token is reused with Basic Auth.

### Configuration Location

All credentials are stored in `config/integrations.yaml`:

```yaml
jira:
  base_url: "https://your-jira-instance.atlassian.net"
  project_key: "DEMO"
  api_token: "your-jira-api-token-here"
  username: "your.email@company.com"

zephyr:
  test_cycle_key: "DEMO-C1"
  api_token: "your-zephyr-api-token-here"
  test_plan_key: "DEMO-P1"
  test_folder: "/Automated/Demo_QA/"
```

### Environment Variable Overrides

Credentials can be overridden via environment variables (recommended for CI/CD):

| Variable | Overrides |
|----------|-----------|
| `DEMO_QA_JIRA_BASE_URL` | `jira.base_url` |
| `DEMO_QA_JIRA_API_TOKEN` | `jira.api_token` |
| `DEMO_QA_JIRA_USERNAME` | `jira.username` |
| `DEMO_QA_JIRA_PROJECT_KEY` | `jira.project_key` |
| `DEMO_QA_ZEPHYR_API_TOKEN` | `zephyr.api_token` |
| `DEMO_QA_ZEPHYR_TEST_CYCLE_KEY` | `zephyr.test_cycle_key` |

Environment variables take precedence over YAML values when set.

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEMO_QA MINI_FRAMEWORK                             │
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────────┐  │
│  │ pytest       │    │ conftest.py  │    │ ReportGenerator              │  │
│  │ (check_T*)   │───▶│ (hooks)      │───▶│ (HTML report)               │  │
│  └──────────────┘    └──────┬───────┘    └──────────────────────────────┘  │
│                             │                                               │
│                             │ test result + metadata                        │
│                             ▼                                               │
│                    ┌────────────────────┐                                   │
│                    │ Integration Layer  │                                   │
│                    │                    │                                   │
│                    │ ┌────────────────┐ │                                   │
│                    │ │ JiraConnector  │ │                                   │
│                    │ └───────┬────────┘ │                                   │
│                    │         │          │                                   │
│                    │ ┌───────┴────────┐ │                                   │
│                    │ │ ZephyrReporter │ │                                   │
│                    │ └───────┬────────┘ │                                   │
│                    └─────────┼──────────┘                                   │
└─────────────────────────────┼───────────────────────────────────────────────┘
                              │
                              │ HTTPS (REST API)
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         JIRA CLOUD INSTANCE                                 │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Jira REST API (/rest/api/2/)                                         │  │
│  │                                                                      │  │
│  │  • POST /search         — Find related issues (JQL)                  │  │
│  │  • POST /issue          — Create bug on test failure                 │  │
│  │  • PUT  /issue/{key}    — Update issue status/fields                 │  │
│  │  • GET  /myself         — Verify connection/credentials              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Zephyr Scale REST API (/rest/atm/1.0/)                               │  │
│  │                                                                      │  │
│  │  • POST /testresult             — Report execution result            │  │
│  │  • GET  /testcase/{key}         — Retrieve test case definition      │  │
│  │  • GET  /testcase/search        — Search test cases by project       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Zephyr Scale Dashboard                                               │  │
│  │                                                                      │  │
│  │  • Test Cycle: DEMO-C1 (aggregated pass/fail per test case)          │  │
│  │  • Test Plan:  DEMO-P1 (overall coverage and execution status)       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Simplified Flow

```
Mini_Framework ──▶ Jira (issue tracking) ──▶ Zephyr Scale (test management)
     │                    │                         │
     │  1. Run tests      │  3. Create/link bugs    │  4. Record execution
     │  2. Collect results │                         │     in test cycle
     ▼                    ▼                         ▼
 HTML Report         Bug Tickets              Test Cycle Dashboard
 (local file)        (DEMO-123)               (pass/fail metrics)
```

---

## Enabling Real Integration

To switch from placeholder mode to live API calls:

1. **Configure credentials** — Replace placeholder values in `config/integrations.yaml` with real credentials
2. **Install dependencies** — Run `pip install requests` (or `pip install jira` for the Jira library)
3. **Enable the integration flag** — Set `enabled: true` in `config/integrations.yaml`
4. **Uncomment API calls** — In both `jira_connector.py` and `zephyr_reporter.py`, uncomment the real implementation blocks below each placeholder log statement
5. **Verify connectivity** — Call `JiraConnector.test_connection()` to confirm credentials work

### Verification Checklist

- [ ] `config/integrations.yaml` has real credentials
- [ ] `enabled: true` is set in the config
- [ ] `requests` package is installed
- [ ] `JiraConnector.test_connection()` returns `True`
- [ ] `ZephyrReporter.report_execution()` successfully posts to a test cycle

---

## Module Reference

| Module | Location | Purpose |
|--------|----------|---------|
| JiraConnector | `framework/integrations/jira_connector.py` | Issue search, creation, and updates |
| ZephyrReporter | `framework/integrations/zephyr_reporter.py` | Test case retrieval and execution reporting |
| Configuration | `config/integrations.yaml` | Credentials and connection settings |

---

## Security Considerations

- Never commit real API tokens to version control
- Use environment variable overrides (`DEMO_QA_JIRA_API_TOKEN`, etc.) in CI/CD pipelines
- The `config/integrations.yaml` file ships with placeholder values only
- Consider using a secrets manager for production deployments
