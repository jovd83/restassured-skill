---
name: restassured-mapper-testlink
description: Use when Codex needs to map TestLink case IDs or execution references back to local Rest Assured API documentation or automation files.
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

# Map TestLink IDs

## 1. Gather Inputs

1. Collect the external TestLink IDs.
2. Read the local docs and automation metadata.

## 2. Map

1. Match by stable scenario ID first.
2. Match by title only when IDs are missing.
3. Record ambiguous matches explicitly.

## 3. Troubleshooting

1. Problem: Multiple local cases match the same title.
   Fix: Use requirement IDs or endpoint paths to disambiguate.
