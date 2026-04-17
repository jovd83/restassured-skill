---
name: restassured-coverage-plan-auto-sync
description: Use when Codex needs to keep Rest Assured API coverage plans, requirements mappings, and test-case documentation synchronized as scenarios are added, removed, or renamed.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: coverage-maintenance, restassured-coverage-sync
  dispatcher-accepted-intents: sync_api_coverage_artifacts
  dispatcher-input-artifacts: coverage_plan, test_suite, traceability_artifacts
  dispatcher-output-artifacts: updated_coverage_artifacts, sync_report
  dispatcher-stack-tags: restassured, coverage, sync
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Auto-Sync Coverage


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Detect Drift

1. Compare the current scenario list against the approved coverage plan.
2. Compare the current documentation files against the approved coverage plan.
3. Identify added, removed, renamed, and unmatched scenarios.

## 2. Repair Traceability

1. Update requirement and contract mappings.
2. Preserve stable identifiers where possible.
3. Mark orphaned cases explicitly instead of deleting them silently.

## 3. Recalculate Coverage

1. Recount covered and uncovered requirements.
2. Recount covered and uncovered operations or faults.
3. Surface residual risk after the sync.

## 4. Troubleshooting

1. Problem: Scenario names changed but IDs did not.
   Fix: Prefer stable IDs and update display titles only.
