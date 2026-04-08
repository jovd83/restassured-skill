---
name: restassured-documentation-traceability-report
description: Use when Codex needs to produce a traceability report that maps API endpoints, methods, operations, coverage rows, Rest Assured tests, and narrative documentation references so humans and later agents can see exactly what is covered across BDD, TDD, plain-text, mixed, or absent documentation.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: traceability-reporting, api-traceability-reporting
  dispatcher-accepted-intents: generate_api_traceability_report
  dispatcher-input-artifacts: coverage_plan, test_suite, narrative_docs
  dispatcher-output-artifacts: traceability_report, coverage_map
  dispatcher-stack-tags: restassured, documentation, traceability
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Build Traceability Report

## 1. Gather Inputs

1. Require the relevant contract or endpoint list.
2. Require the current coverage matrix or matrices when they exist.
3. Require the executable Rest Assured test files.
4. Require the narrative documentation files when they exist. Accept BDD, TDD, plain-text, mixed documentation, or no narrative docs.
5. Treat scenario-level narrative artifacts as canonical when they exist. Treat aggregate index files under `docs/testing/` as secondary context.

## 2. Choose The File

1. Prefer `docs/testing/test-mapping-report.md` in the target repository.
2. Use an existing traceability or mapping report when one already exists.
3. Keep one canonical mapping report per service or test module unless the repo already splits by domain.
4. When the user wants a human-friendly report site, also generate HTML into `docs/testing/html/`.

## 3. Build The Mapping

1. Create one row per endpoint and method combination.
2. Include the operation ID when available.
3. Link each row to the coverage scenario IDs.
4. Link each row to the executable test class and test method names.
5. Link each row to the canonical narrative documentation artifact and scenario or case reference when documentation exists.
6. Prefer scenario-level docs such as `docs/tests/<feature>/<scenario>-mss.md` or `.feature` scenario anchors over aggregate index files.
7. Use aggregate index files only when the repo has no per-scenario narrative artifacts or when the index adds necessary summary context.
8. Mark the execution status as covered, partially covered, contract drift, or not covered.
9. When the report will be used by humans in an IDE, add reverse sections by test class and by documentation artifact.
10. Keep the exact section headings `## Summary`, `## Endpoint Mapping`, `## Reverse Mapping By Test Class`, `## Reverse Mapping By Documentation Artifact`, and `## Gaps` for new reports. Accept legacy `## Reverse Mapping By BDD Feature` when maintaining older artifacts.
11. Keep the endpoint-mapping columns exactly `Method | Path | Operation ID | Coverage Rows | Test References | Documentation References | Status | Notes` for new reports. Accept legacy `BDD References` when maintaining older artifacts.
12. When a row has multiple coverage rows, test references, or documentation references, keep their order intentional because the HTML portal projects them into one executable coverage row per test reference.

## 4. Keep The Report Actionable

1. Add a summary with total endpoints, covered endpoints, drift-only endpoints, and uncovered endpoints.
2. Add a short gaps section listing anything still missing or only covered through drift assertions.
3. Update the session-state artifact after creating or changing the report.
4. Prefer clickable file-and-line references when the environment supports them.
5. If `contract-mismatches.md` also exists, generate the paired HTML report with `scripts/generate_html_reports.py`.
6. For HTML output, generate a report portal, not a flat table dump.
7. In HTML, group operations by resource, add search and status filters, preserve reverse mapping by test class and documentation artifact, and keep links back to the canonical markdown files.
8. In HTML, render executable coverage as one visible row per test reference instead of a comma-separated blob.
9. When sibling reports such as `coverage-gap-report`, `openapi-change-impact-report`, or `assertion-strength-report` exist in the same `docs/testing/` folder, surface them in the HTML landing portal and link their canonical markdown sources.
10. When the caller wants all report surfaces refreshed together, route to `../report-bundle/SKILL.md`.

## 5. Output Shape

1. Start from [traceability-report-template.md](assets/traceability-report-template.md).
2. Keep the columns stable so later sync work can update the report deterministically.
3. Use exact endpoint paths and method names from the contract.
4. For HTML output, run `python scripts/generate_html_reports.py --mapping <mapping-md> --mismatches <mismatch-md> --outdir <html-dir>`.
5. Treat the markdown report as canonical and the HTML report as a deterministic projection of that markdown.
6. When both per-scenario docs and an aggregate index exist, put the per-scenario doc in `Documentation References` and mention the index only in `Notes` when it adds value.

## 6. Examples

1. Input: `Map the Orders API coverage to tests and TDD case files.`
   Output: Create `docs/testing/test-mapping-report.md` with one row per contract operation and links to the relevant code and docs.
2. Input: `Show which Rest Assured tests cover each Petstore endpoint.`
   Output: Produce a mapping report that connects OpenAPI operations to coverage rows, test methods, and documentation references.

## 7. Troubleshooting

1. Problem: Several tests touch the same endpoint for different purposes.
   Fix: Keep one row per endpoint and method, then list all relevant test methods in that row.
2. Problem: The endpoint is only covered through a mismatch or negative test.
   Fix: Mark the row as `Contract drift` or `Partial` instead of `Covered`.
3. Problem: The coverage matrix and tests disagree.
   Fix: Use the executable tests as the source of truth and list the matrix discrepancy under `Gaps`.
4. Problem: The HTML report loses columns or collapses into one column.
   Fix: Restore the exact section headings and exact endpoint-mapping columns from the template before regenerating the HTML portal.
5. Problem: The report links only to a TDD index file or a documentation summary page.
   Fix: Replace the mapping references with the canonical scenario-level documents and keep the index only as optional supporting context.
