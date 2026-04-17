---
name: restassured-documentation-root-cause
description: Use when Codex needs to analyze failing Rest Assured API tests, identify the most likely root cause, and produce a developer-focused failure diagnosis.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: failure-analysis, api-root-cause
  dispatcher-accepted-intents: analyze_api_test_failure
  dispatcher-input-artifacts: failure_output, repo_context, test_artifacts
  dispatcher-output-artifacts: root_cause_report, failure_summary
  dispatcher-stack-tags: restassured, diagnostics, failure-analysis
  dispatcher-risk: low
  dispatcher-writes-files: false
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Root Cause Analysis

## 1. Gather Evidence

1. Capture the failing request and response.
2. Capture the exact assertion failure.
3. Capture environment details, auth details, and dependency behavior.
4. Capture container or stub logs when relevant.

## 2. Identify The Failure Class

1. Classify the failure as environment, auth, contract drift, test data, dependency outage, assertion bug, or application defect.
2. State the most likely root cause first.
3. State competing hypotheses only when evidence is incomplete.

## 3. Produce The Diagnosis

1. State what failed.
2. State why it most likely failed.
3. State how to confirm it.
4. State the recommended fix.

## 4. Troubleshooting

1. Problem: The evidence is incomplete.
   Fix: State the gap and request the missing artifact explicitly.