---
name: restassured-transformer-xray
description: Legacy Rest Assured-specific alias for Xray case export. Prefer the standalone `test-artifact-export-skill` skill for transforming approved test cases into Xray-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
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

# Transform Cases For Xray


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Collect Inputs

1. Read the approved cases.
2. Preserve stable IDs, tags, and requirement links.

## 2. Transform

1. Convert BDD scenarios into Xray-compatible feature content when BDD is used.
2. Convert structured cases into JSON or CSV when BDD is not used.

## 3. Troubleshooting

1. Problem: The source content mixes multiple scenarios in one file.
   Fix: Split them before export.
