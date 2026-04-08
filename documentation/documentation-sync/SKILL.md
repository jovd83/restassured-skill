---
name: restassured-documentation-sync
description: Use when Codex needs to keep Rest Assured narrative documentation synchronized with endpoint traceability, coverage rows, and executable tests across BDD, TDD, plain-text, mixed, or partially documented API suites.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: documentation-sync, api-documentation-sync
  dispatcher-accepted-intents: sync_api_test_docs
  dispatcher-input-artifacts: test_suite, narrative_docs, traceability_artifacts
  dispatcher-output-artifacts: documentation_sync_report, updated_docs
  dispatcher-stack-tags: restassured, documentation, sync
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Sync Narrative Documentation

## 1. Gather Inputs

1. Require `docs/testing/test-mapping-report.md`.
2. Require the narrative documentation roots when they are known.
3. Accept BDD feature files, TDD case files, plain-text case files, mixed sets, or partially documented suites.
4. Accept missing narrative docs and report them explicitly instead of inventing them.
5. Prefer `docs/tests/` as the default narrative-doc root for TDD, plain-text, and mixed per-scenario documentation.
6. Treat aggregate files under `docs/testing/` as secondary indexes or reports, not as the primary narrative-doc root.

## 2. Audit Before Editing

1. Run `python scripts/audit_documentation_sync.py --mapping <mapping-md> --output <sync-report-md>`.
2. Add `--docs-root <path>` for each narrative-documentation root when the repo stores multiple documentation sets.
3. When the repo follows the family convention and `docs/tests/` exists, allow the script to discover that root automatically.
4. Use the audit report to identify:
   1. Missing documentation references from the traceability report
   2. Orphan narrative docs with no traceability link
   3. Detected documentation modes
5. Do not rewrite documentation before the audit identifies the drift.

## 3. Repair The Drift

1. Add missing references into the traceability report.
2. Update stale scenario or case titles so the documentation still matches the executable tests.
3. Preserve stable coverage IDs and test links.
4. Mark intentionally undocumented slices explicitly instead of pretending they are documented.
5. Keep the reporting model documentation-neutral unless the repo has deliberately standardized on one narrative format.

## 4. Keep It Compatible

1. Prefer `Documentation References` for new mapping reports.
2. Accept legacy `BDD References` and legacy reverse-BDD sections when maintaining older artifacts.
3. Do not force BDD labels onto TDD or plain-text docs.
4. Update the session-state artifact after repairing documentation drift.
5. When both a per-scenario doc and an aggregate index exist, keep the per-scenario doc canonical and treat the index as optional navigation only.

## 5. Output Shape

1. Prefer `docs/testing/documentation-sync-report.md` for the audit report.
2. Start from [documentation-sync-report-template.md](assets/documentation-sync-report-template.md).
3. Keep the audit report factual: summarize what is missing, orphaned, or intentionally absent.
4. Keep the audited-roots list explicit so later agents know which documentation trees were checked.

## 6. Examples

1. Input: `Sync the TDD case files with the latest API tests.`
   Output: Audit `docs/tests/`, identify stale or missing references, then update the traceability and case docs.
2. Input: `This repo mixes BDD and plain-text cases. Check what drifted.`
   Output: Generate `docs/testing/documentation-sync-report.md` and repair the mismatches without forcing one format.

## 7. Troubleshooting

1. Problem: The traceability report still uses `BDD References`.
   Fix: Treat it as a legacy-compatible input and only normalize it if the user asked for that rewrite.
2. Problem: Narrative docs exist, but none are referenced from the mapping report.
   Fix: Audit the docs roots, then add the missing links into the mapping report.
3. Problem: Some endpoints intentionally have no narrative docs.
   Fix: Mark them explicitly in the sync report and keep the gap visible.
4. Problem: The sync audit reports only an aggregate index file as documented.
   Fix: Add the per-scenario docs root to the audit, then repoint the traceability report to the canonical scenario files.
