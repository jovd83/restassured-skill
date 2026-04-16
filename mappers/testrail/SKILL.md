---
name: restassured-mapper-testrail
description: Use when Codex needs to map TestRail case IDs or execution references back to local Rest Assured API documentation or automation files.
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

# Map TestRail IDs


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Gather Inputs

1. Collect the external TestRail IDs.
2. Read the local case metadata.

## 2. Map

1. Prefer stable local IDs and requirement links.
2. Record unmatched cases explicitly.
