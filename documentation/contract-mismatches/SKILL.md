---
name: restassured-documentation-contract-mismatches
description: Use when Codex needs to document differences between an API contract and the observed live Rest Assured runtime behavior so humans and later agents can implement tests safely and track drift explicitly.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: contract-mismatch-analysis, api-contract-mismatch-analysis
  dispatcher-accepted-intents: analyze_api_contract_mismatches
  dispatcher-input-artifacts: api_contract, runtime_evidence, mismatch_rows
  dispatcher-output-artifacts: contract_mismatch_report, drift_summary
  dispatcher-stack-tags: restassured, documentation, contract
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Document Contract Mismatches

## 1. Confirm The Inputs

1. Require the contract source, the live environment or recorded runtime evidence, and the affected endpoint or operation list.
2. Confirm whether the mismatch was observed in execution, logs, manual probing, or CI artifacts.
3. Refuse to create a mismatch record from guesses or unverified assumptions.

## 2. Choose The File

1. Prefer `docs/testing/contract-mismatches.md` in the target repository.
2. Use an existing project-specific mismatch file when one already exists.
3. Keep one canonical mismatch document per service unless the repo already splits by domain.

## 3. Start From The Template

1. Copy the structure from [contract-mismatch-template.md](assets/contract-mismatch-template.md).
2. Preserve all section headings.
3. Keep one mismatch entry per endpoint, operation, or distinct discrepancy.

## 4. Record Each Mismatch

1. Record the endpoint, method, operation ID, and environment.
2. Record the contract expectation with the source path or schema reference.
3. Record the observed runtime behavior with status code, content type, payload shape, and a short evidence note.
4. Classify the mismatch as status, content type, schema, required field handling, auth, header, or semantic behavior.
5. State whether executable tests must follow the runtime behavior or block on clarification.
6. Link the mismatch to the affected test class, coverage row, and session-state file when they exist.

## 5. Decide The Test Posture

1. Keep executable tests aligned with verified runtime behavior unless the user explicitly wants contract-enforcement tests.
2. Mark the mismatch as `Known drift` when the runtime behavior is stable and intentionally tolerated.
3. Mark the mismatch as `Potential defect` when the runtime behavior appears unintended or unsafe.
4. Mark the mismatch as `Needs product decision` when the correct behavior is unclear.

## 6. Keep The Artifact Actionable

1. End each mismatch entry with the next action, owner, and verification needed.
2. Update the session-state artifact after adding or changing mismatch records.
3. Update the coverage matrix when a mismatch adds or removes executable scenarios.
4. When the repository also has a traceability report, generate the paired HTML reports with `../traceability-report/scripts/generate_html_reports.py`.
5. In HTML, render mismatch entries as grouped evidence cards with search, status filters, resource grouping, and links back to the canonical markdown.
6. Keep the markdown mismatch file canonical and regenerate the HTML after every meaningful change.

## 7. Examples

1. Input: `The live login endpoint returns plain text with application/json. Document it.`
   Output: Create `docs/testing/contract-mismatches.md` with the contract expectation, runtime evidence, affected tests, and next action.
2. Input: `POST /pet accepts missing required fields in the live environment.`
   Output: Add a mismatch entry that classifies the drift as required-field handling and links it to the executed negative or contract test.

## 8. Troubleshooting

1. Problem: The agent only has a failing assertion and no raw response metadata.
   Fix: Re-run the narrowest call and capture status, content type, and body evidence before documenting the mismatch.
2. Problem: The contract and runtime differ in several ways for the same endpoint.
   Fix: Split them into separate mismatch entries when they need different owners or next actions.
3. Problem: The team wants both runtime-regression coverage and contract-enforcement coverage.
   Fix: Document the mismatch, keep the default executable suite runtime-aligned, and create a clearly tagged contract-enforcement slice only if the user asks for it.
4. Problem: The HTML view is stale or no longer matches the markdown artifact.
   Fix: Re-run `../traceability-report/scripts/generate_html_reports.py` after updating `contract-mismatches.md`.
