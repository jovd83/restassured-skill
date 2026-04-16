---
name: restassured-documentation-coverage-gap-report
description: Use when Codex needs to highlight uncovered, partial, drift-only, or weakly covered API areas so humans can prioritize the next Rest Assured work instead of reading the full traceability report.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: coverage-gap-analysis, api-coverage-gap-reporting
  dispatcher-accepted-intents: report_api_coverage_gaps
  dispatcher-input-artifacts: coverage_plan, test_suite, traceability_artifacts
  dispatcher-output-artifacts: coverage_gap_report, risk_summary
  dispatcher-stack-tags: restassured, documentation, coverage
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Build Coverage Gap Report


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Gather Inputs

1. Require the current `docs/testing/test-mapping-report.md`.
2. Require `docs/testing/contract-mismatches.md` when it exists.
3. Require the active coverage matrices when they contain gaps not yet reflected in traceability.

## 2. Choose The Files

1. Prefer `docs/testing/coverage-gap-report.md`.
2. When the user wants human-friendly navigation, also generate `docs/testing/html/coverage-gap-report.html`.

## 3. Build The Report

1. Treat `Not covered`, `Partial`, and `Contract drift` operations as primary gaps.
2. Include explicit gap bullets from the traceability report.
3. Separate the report into summary, operation gaps, and planning recommendations.
4. Keep one operation row per endpoint and method in markdown.
5. In HTML, group the operation gaps by resource and make the next action obvious.

## 4. Output Shape

1. Start from [coverage-gap-report-template.md](assets/coverage-gap-report-template.md).
2. Keep the exact section headings so the generator can update the file deterministically.
3. Run `python scripts/generate_coverage_gap_report.py --mapping <mapping-md> --output-md <gap-md> --output-html <gap-html>`.

## 5. Keep It Actionable

1. Explain why each gap matters.
2. Recommend the next slice to implement.
3. Update the session-state artifact after generating or changing the report.

## 6. Examples

1. Input: `Show me the biggest API coverage gaps.`
   Output: Create `docs/testing/coverage-gap-report.md` and the paired HTML report.
2. Input: `Which endpoints are only covered through drift assertions?`
   Output: Produce a gap report that isolates `Contract drift` operations and suggests next actions.

## 7. Troubleshooting

1. Problem: The traceability report says everything is covered.
   Fix: Still surface `Contract drift` rows and explicit gap bullets because those are planning gaps.
2. Problem: The markdown and HTML disagree.
   Fix: Regenerate the HTML from the canonical markdown inputs and do not hand-edit the HTML.
