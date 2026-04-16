---
name: restassured-transformer-zephyr
description: Legacy Rest Assured-specific alias for Zephyr case export. Prefer the standalone `test-artifact-export-skill` skill for transforming approved test cases into Zephyr-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: test-artifact-formatting, api-legacy-export-transform
  dispatcher-accepted-intents: render_test_artifact, export_test_cases
  dispatcher-input-artifacts: approved_test_cases, normalized_test_case_model, destination_constraints
  dispatcher-output-artifacts: transformed_test_artifact, export_bundle
  dispatcher-stack-tags: restassured, transform, legacy-alias
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Transform Cases For Zephyr


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Collect Inputs

1. Read approved source cases.
2. Preserve stable titles and traceability references.

## 2. Transform

1. Map scenario metadata into the Zephyr import structure.
2. Preserve execution labels when the target format supports them.

## 3. Troubleshooting

1. Problem: The source cases are missing expected results.
   Fix: Fill the gap before export.
