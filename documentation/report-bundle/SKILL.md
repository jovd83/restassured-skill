---
name: restassured-documentation-report-bundle
description: Use when Codex needs to generate or refresh a bundled Rest Assured reporting set, including traceability, contract mismatches, coverage gaps, OpenAPI change impact, assertion strength, and the human-friendly HTML portal, with support for BDD, TDD, plain-text, mixed, or absent narrative documentation.
---

# Build Report Bundle

## 1. Gather Inputs

1. Require `docs/testing/test-mapping-report.md`.
2. Require `docs/testing/contract-mismatches.md`.
3. Require the Java test root used by the Rest Assured suite.
4. Require the HTML output directory, or default to `docs/testing/html/`.
5. Require baseline and current OpenAPI sources only when change-impact reporting is needed.
6. Treat narrative documentation as optional. Accept BDD, TDD, plain text, mixed documentation, or no narrative documentation at all.

## 2. Choose The Outputs

1. Generate or refresh these markdown artifacts when their inputs exist:
   1. `docs/testing/coverage-gap-report.md`
   2. `docs/testing/assertion-strength-report.md`
   3. `docs/testing/openapi-change-impact-report.md` when both contract sources are available
2. Generate or refresh these HTML artifacts:
   1. `docs/testing/html/index.html`
   2. `docs/testing/html/test-mapping-report.html`
   3. `docs/testing/html/contract-mismatches.html`
   4. `docs/testing/html/coverage-gap-report.html`
   5. `docs/testing/html/assertion-strength-report.html`
   6. `docs/testing/html/openapi-change-impact-report.html` when both contract sources are available
3. Prefer `docs/testing/report-bundle-manifest.md` for the bundle manifest.

## 3. Run The Bundle

1. Run `python scripts/generate_report_bundle.py --mapping <mapping-md> --mismatches <mismatch-md> --tests-root <tests-root> --html-dir <html-dir>`.
2. Add `--baseline <baseline-openapi>` and `--current <current-openapi>` when change-impact output is required.
3. Add `--output-manifest <manifest-md>` when the caller wants an explicit bundle manifest.
4. Keep the traceability markdown and mismatch markdown canonical. Treat the generated HTML and auxiliary markdown reports as deterministic projections.

## 4. Keep The Bundle Format-Agnostic

1. Use `documentation references` as the generic reporting concept.
2. Accept BDD feature files, TDD case documents, plain-text cases, mixed sets, or no narrative docs.
3. Do not force Gherkin sections or BDD labels into reports that can be documentation-neutral.
4. When the traceability markdown still uses legacy BDD headings or columns, preserve compatibility and regenerate the bundle without rewriting history unless the user asked for normalization.

## 5. Keep It Actionable

1. Regenerate the HTML landing portal after refreshing any sibling report.
2. Surface sibling reports automatically from the landing portal when they exist.
3. Update the session-state artifact after running the bundle.
4. Use the coverage-gap report to drive next-slice planning.
5. Use the assertion-strength report to drive test-hardening work.
6. Use the change-impact report to drive contract-diff regression work.

## 6. Examples

1. Input: `Refresh the full API reporting bundle for this module.`
   Output: Regenerate traceability HTML, mismatch HTML, coverage-gap, assertion-strength, and the landing portal.
2. Input: `Rebuild all reports after the OpenAPI changed.`
   Output: Regenerate the full bundle and include `openapi-change-impact-report`.
3. Input: `Update the human-readable reports, but this repo uses TDD case docs, not BDD.`
   Output: Regenerate the bundle using generic documentation references without forcing BDD-specific labels.

## 7. Troubleshooting

1. Problem: The bundle fails because the change-impact sources are missing.
   Fix: Skip `openapi-change-impact-report` unless both `--baseline` and `--current` are available.
2. Problem: The traceability markdown uses legacy `BDD References`.
   Fix: Keep the legacy markdown as input and let the bundle regenerate compatible outputs.
3. Problem: The HTML portal does not show a sibling report.
   Fix: Verify the markdown artifact exists in `docs/testing/` and the matching HTML artifact exists in `docs/testing/html/`, then rerun the bundle.
