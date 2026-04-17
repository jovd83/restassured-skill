---
name: restassured-documentation-openapi-change-impact-report
description: Use when Codex needs to compare two OpenAPI or Swagger contracts, identify added, removed, or changed operations and schemas, and map the impact back to existing Rest Assured coverage.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: change-impact-analysis, openapi-change-impact
  dispatcher-accepted-intents: analyze_openapi_change_impact
  dispatcher-input-artifacts: old_contract, new_contract, coverage_artifacts
  dispatcher-output-artifacts: change_impact_report, impacted_tests
  dispatcher-stack-tags: restassured, documentation, contract
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Build OpenAPI Change Impact Report


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Gather Inputs

1. Require a baseline OpenAPI or Swagger source.
2. Require a current OpenAPI or Swagger source.
3. Require `docs/testing/test-mapping-report.md` when test-impact mapping is needed.

## 2. Choose The Files

1. Prefer `docs/testing/openapi-change-impact-report.md`.
2. When the user wants a human-friendly report, also generate `docs/testing/html/openapi-change-impact-report.html`.

## 3. Build The Comparison

1. Compare operation existence first.
2. Compare operation metadata second: tags, summary, security, parameters, request body, and response codes.
3. Classify each difference as `Added`, `Removed`, `Breaking change`, `Non-breaking change`, or `No change`.
4. When a traceability report exists, map changed operations back to affected tests and documentation references.
5. Keep the report useful even when there is no change.

## 4. Output Shape

1. Start from [openapi-change-impact-report-template.md](assets/openapi-change-impact-report-template.md).
2. Keep the exact section headings stable.
3. Run `python scripts/generate_openapi_change_impact_report.py --baseline <baseline> --current <current> --mapping <mapping-md> --output-md <impact-md> --output-html <impact-html>`.

## 5. Keep It Actionable

1. Explain which changed operations need test updates first.
2. Separate breaking changes from additive changes.
3. Update the session-state artifact after generating or changing the report.

## 6. Examples

1. Input: `Show what changed between these two OpenAPI files and which tests are affected.`
   Output: Create `docs/testing/openapi-change-impact-report.md` and the paired HTML report.
2. Input: `Compare the live contract to the repo contract.`
   Output: Produce a change-impact report, even if the final result is `No change`.

## 7. Troubleshooting

1. Problem: The two sources use different file formats.
   Fix: Normalize both sources before comparison; YAML vs JSON is not itself a change.
2. Problem: There are no contract changes.
   Fix: Still generate the report and state `No change` explicitly.
