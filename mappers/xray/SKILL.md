---
name: restassured-mapper-xray
description: Use when Codex needs to map Xray issue keys or execution references back to local Rest Assured API documentation or automation files.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: test-management-mapping, api-test-management-mapping
  dispatcher-accepted-intents: map_api_test_management_ids
  dispatcher-input-artifacts: test_management_ids, local_artifacts, repo_context
  dispatcher-output-artifacts: mapped_traceability_artifacts, mapping_report
  dispatcher-stack-tags: restassured, mapping, test-management
  dispatcher-risk: low
  dispatcher-writes-files: true
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Map Xray IDs

## 1. Gather Inputs

1. Collect Xray issue keys.
2. Read local case IDs, tags, and docs.

## 2. Map

1. Match by stable scenario ID or requirement link.
2. Preserve unresolved gaps for manual triage.