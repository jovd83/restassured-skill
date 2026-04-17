---
name: restassured-reporter-zephyr
description: Use when Codex needs to report Rest Assured API test execution results back to Zephyr through its API using local case mappings and execution evidence.
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

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Report Results To Zephyr

## 1. Gather Inputs

1. Collect Zephyr credentials securely.
2. Collect execution results and mappings.

## 2. Report

1. Map each result to the correct Zephyr case.
2. Attach concise evidence for failures.

## 3. Troubleshooting

1. Problem: The execution status mapping is wrong.
   Fix: Normalize local statuses before sending them.