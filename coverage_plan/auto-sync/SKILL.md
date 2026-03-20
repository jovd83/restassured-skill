---
name: restassured-coverage-plan-auto-sync
description: Use when Codex needs to keep Rest Assured API coverage plans, requirements mappings, and test-case documentation synchronized as scenarios are added, removed, or renamed.
metadata:
  author: jovd83
  version: "1.0"
---

# Auto-Sync Coverage

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
