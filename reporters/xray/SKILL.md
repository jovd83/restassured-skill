---
name: restassured-reporter-xray
description: Use when Codex needs to report Rest Assured API test execution results back to Xray through its API using local case mappings and execution evidence.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: test-management-reporting, api-test-management-reporting
  dispatcher-accepted-intents: report_api_test_results
  dispatcher-input-artifacts: execution_results, test_management_config, mappings
  dispatcher-output-artifacts: published_results, reporting_summary
  dispatcher-stack-tags: restassured, reporting, test-management
  dispatcher-risk: medium
  dispatcher-writes-files: true
---

# Report Results To Xray


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Gather Inputs

1. Collect Xray or Jira credentials securely.
2. Collect execution results and mappings.

## 2. Report

1. Map results to test issue keys.
2. Send concise evidence for failures and blocked states.

## 3. Troubleshooting

1. Problem: The execution file format is rejected.
   Fix: Validate the payload shape against the selected Xray API.
