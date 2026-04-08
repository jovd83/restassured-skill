---
name: restassured-reporter-testlink
description: Use when Codex needs to report Rest Assured API test execution results back to TestLink through its API using local case mappings and execution evidence.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: test-management-reporting, api-test-management-reporting
  dispatcher-accepted-intents: report_api_test_results
  dispatcher-input-artifacts: execution_results, test_management_config, mappings
  dispatcher-output-artifacts: published_results, reporting_summary
  dispatcher-stack-tags: restassured, reporting, test-management
  dispatcher-risk: medium
  dispatcher-writes-files: true
---

# Report Results To TestLink

## 1. Gather Inputs

1. Collect the TestLink URL and API key securely.
2. Collect the latest execution result set.
3. Collect the local-to-external case mapping.

## 2. Report

1. Map each test result to the target external ID.
2. Send passed, failed, blocked, or skipped status as supported.
3. Attach concise failure evidence when useful.

## 3. Troubleshooting

1. Problem: The result cannot be mapped.
   Fix: Run the mapper skill before reporting.
