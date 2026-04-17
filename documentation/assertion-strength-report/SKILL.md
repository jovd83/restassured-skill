---
name: restassured-documentation-assertion-strength-report
description: Use when Codex needs to assess whether Rest Assured tests are weak, moderate, or strong based on the assertions they make, the amount of API behavior they verify, and whether they go beyond status-code checks.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: assertion-review, api-assertion-strength-review
  dispatcher-accepted-intents: assess_api_assertion_strength
  dispatcher-input-artifacts: api_test_suite, repo_context
  dispatcher-output-artifacts: assertion_strength_report, review_findings
  dispatcher-stack-tags: restassured, documentation, review
  dispatcher-risk: low
  dispatcher-writes-files: false
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Build Assertion Strength Report

## 1. Gather Inputs

1. Require the Rest Assured test sources.
2. Require `docs/testing/test-mapping-report.md` when endpoint context is needed.

## 2. Choose The Files

1. Prefer `docs/testing/assertion-strength-report.md`.
2. When the user wants a human-friendly report, also generate `docs/testing/html/assertion-strength-report.html`.

## 3. Build The Assessment

1. Score each test method from the code, not from assumptions.
2. Detect status, header, content-type, body, schema, and workflow-style assertions.
3. Classify each test method as `Weak`, `Moderate`, or `Strong`.
4. Call out tests that only assert status codes or only transport-level behavior.
5. Recommend where semantic assertions should be added next.

## 4. Output Shape

1. Start from [assertion-strength-report-template.md](assets/assertion-strength-report-template.md).
2. Keep the exact section headings stable.
3. Run `python scripts/generate_assertion_strength_report.py --tests-root <tests-root> --mapping <mapping-md> --output-md <report-md> --output-html <report-html>`.

## 5. Keep It Actionable

1. Highlight the weakest tests first.
2. Explain why a test is weak or strong.
3. Update the session-state artifact after generating or changing the report.

## 6. Examples

1. Input: `Which tests only assert status codes?`
   Output: Create an assertion-strength report that classifies tests and isolates weak ones.
2. Input: `Assess the quality of these Rest Assured assertions.`
   Output: Produce a markdown and HTML report with strengths, weaknesses, and recommended next assertions.

## 7. Troubleshooting

1. Problem: The same test method mixes several requests.
   Fix: Score the whole method and label it as workflow-oriented when multiple HTTP calls are present.
2. Problem: The repo uses helper methods for assertions.
   Fix: Mark the result as approximate and recommend manual review for the affected tests.