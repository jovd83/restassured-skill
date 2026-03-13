---
name: restassured-documentation-root-cause
description: Use when Codex needs to analyze failing Rest Assured API tests, identify the most likely root cause, and produce a developer-focused failure diagnosis.
---

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
