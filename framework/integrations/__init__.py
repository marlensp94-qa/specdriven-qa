"""
Framework Integrations — Demo_QA
==================================
Placeholder modules for Jira and Zephyr Scale integration.

These modules demonstrate the integration pattern without requiring
real credentials. All methods log their intended behavior.

Modules:
    jira_connector: Jira REST API connector for issue management
    zephyr_reporter: Zephyr Scale reporter for test execution results

Usage:
    from framework.integrations.jira_connector import JiraConnector
    from framework.integrations.zephyr_reporter import ZephyrReporter
"""

from framework.integrations.jira_connector import JiraConnector
from framework.integrations.zephyr_reporter import ZephyrReporter

__all__ = ["JiraConnector", "ZephyrReporter"]
