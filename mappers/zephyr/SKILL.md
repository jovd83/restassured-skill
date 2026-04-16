---
name: restassured-mapper-zephyr
description: Use when Codex needs to map Zephyr case IDs or execution references back to local Rest Assured API documentation or automation files.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: test-management-mapping, api-test-management-mapping
  dispatcher-accepted-intents: map_api_test_management_ids
  dispatcher-input-artifacts: test_management_ids, local_artifacts, repo_context
  dispatcher-output-artifacts: mapped_traceability_artifacts, mapping_report
  dispatcher-stack-tags: restassured, mapping, test-management
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Map Zephyr IDs


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Gather Inputs

1. Collect Zephyr IDs.
2. Read local case and automation metadata.

## 2. Map

1. Prefer stable IDs over title-only matching.
2. Mark collisions explicitly.
