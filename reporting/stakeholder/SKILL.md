---
name: restassured-reporting-stakeholder
description: Use when Codex needs to summarize Rest Assured API test execution for non-technical stakeholders in clear business terms instead of raw test runner output.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: stakeholder-reporting, api-stakeholder-reporting
  dispatcher-accepted-intents: summarize_api_test_results
  dispatcher-input-artifacts: execution_results, tested_scope, release_context
  dispatcher-output-artifacts: stakeholder_summary, release_health_report
  dispatcher-stack-tags: restassured, reporting, stakeholder
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Stakeholder Reporting


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Summarize Business Impact

1. State what feature area was tested.
2. State the overall result.
3. State the user or business impact of failures.

## 2. Avoid Low-Signal Detail

1. Do not dump stack traces.
2. Do not list raw JSON payloads unless necessary.
3. Translate technical failures into business-readable risk.

## 3. Include Next Actions

1. State whether release scope is blocked, degraded, or acceptable.
2. State the next owner and next action when known.
