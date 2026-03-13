---
name: restassured-reporting-stakeholder
description: Use when Codex needs to summarize Rest Assured API test execution for non-technical stakeholders in clear business terms instead of raw test runner output.
---

# Stakeholder Reporting

## 1. Summarize Business Impact

1. State what feature area was tested.
2. State the overall result.
3. State the user or business impact of failures.

## 2. Avoid Low-Signal Detail

1. Do not dump stack traces.
2. Do not list raw JSON payloads unless necessary.
3. Translate technical failures into business-readable risk.

## 3. Include Next Actions

1. State whether release scope is blocked, degraded, or acceptable.
2. State the next owner and next action when known.
