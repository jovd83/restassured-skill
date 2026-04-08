---
name: restassured-documentation-plaintext
description: Legacy Rest Assured-specific alias for plain-text case formatting. Prefer the standalone `test-artifact-export-skill` skill for lightweight narrative case output, and use this only when Rest Assured-local conventions must be preserved explicitly.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: test-artifact-formatting, restassured-legacy-test-case-formatting
  dispatcher-accepted-intents: render_test_artifact, export_test_cases
  dispatcher-input-artifacts: approved_test_cases, normalized_test_case_model, scenario_list
  dispatcher-output-artifacts: formatted_test_artifact, export_ready_case_set
  dispatcher-stack-tags: restassured, documentation, legacy-alias
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Document Test Cases In Plain Text

## 1. Store And Organize Files

1. Store plain-text cases under `docs/tests/<feature>/`.
2. Create one `.md` or `.txt` file per scenario even in this lightweight mode.
3. Name files with the scenario purpose and classification, for example `list-vets-mss.md` or `missing-owner-err.txt`.
4. For non-trivial requirements, keep separate files for `MSS`, `EXT`, and `ERR` instead of mixing them into one narrative.
5. Use aggregate files under `docs/testing/` only as indexes when the repo wants a summary.

## 2. Use This Lightweight Structure

1. Start with `Title`.
2. Add `Purpose`.
3. Add `Covered requirement`.
4. Add `Preconditions`.
5. Add `Flow`.
6. Add `Expected outcome`.
7. Add `Test script`.
8. Keep the wording concise, readable, and still traceable.

## 3. Content Rules

1. State the test goal clearly in the first sentence.
2. Mention any setup or auth state before the flow starts.
3. Describe the request flow in a logical sequence.
4. State the expected status, important headers, business fields, and side effects.
5. Link to the exact Java test method in `Test script`.
6. Keep the content API-specific. Do not use UI language.

## 4. Start From The Template

1. Start from [plain-text-case-template.md](assets/plain-text-case-template.md) for new lightweight scenario docs.
2. Keep the headings stable so traceability and documentation-sync work can recognize the file shape consistently.

## 5. Example

```markdown
Title: [SPC-OWN-002] ERR: Missing owner lookup
Purpose: Capture the runtime behavior when a client requests an owner id that does not exist.
Covered requirement: GET /api/owners/{ownerId}, operationId=getOwner, SPC-OWN-002
Preconditions:
- The API is running.
- Owner id `999999` does not exist.
Flow:
- Send `GET /api/owners/999999`.
- Observe the returned status and payload behavior.
Expected outcome:
- The runtime returns status `404`.
- The mismatch report records that the documented problem-detail payload is not returned.
Test script: [OwnerReadApiTest.java](C:/repo/src/test/java/com/example/owner/OwnerReadApiTest.java)#missingOwnerReturnsBare404AtRuntime
```

## 6. Use Cases

1. Use this format for quick reviews or lightweight stakeholder alignment.
2. Use this format when the user rejects formal TDD or BDD structures.
3. Use this format when the team wants readable notes without losing traceability.

## 7. Troubleshooting

1. Problem: Important response details are missing.
   Fix: Add expected status, critical headers, business fields, and side effects explicitly.
2. Problem: The document becomes a vague paragraph with no traceability.
   Fix: Reintroduce `Covered requirement` and `Test script` explicitly.
3. Problem: One document covers too many behaviors.
   Fix: Split it into one scenario file per behavior, even in plain-text mode.
