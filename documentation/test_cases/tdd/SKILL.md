---
name: restassured-documentation-tdd
description: Legacy Rest Assured-specific alias for TDD-style case documentation. Prefer the standalone `test-artifact-export-skill` skill for formatting approved test cases or building export-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
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

# Document Test Cases In TDD

## 1. Store And Organize Files

1. Store TDD documents under `docs/tests/`.
2. Mirror the automation or business-domain structure with feature folders such as `docs/tests/orders/` or `docs/tests/auth/`.
3. Create one `.md` file per executable scenario, not one file per epic.
4. Name files with a stable scenario purpose and classification such as `create-order-mss.md`, `create-order-optional-fields-ext.md`, or `create-order-missing-customer-err.md`.
5. For non-trivial or high-risk requirements, document multiple scenarios:
   1. `MSS` for the main success path.
   2. `EXT` for valid variants such as optional fields or alternate filters.
   3. `ERR` for validation, auth, not-found, conflict, or drift behavior.
6. For trivial low-risk reads, one `MSS` scenario is sufficient.
7. Do not force redundant scenarios when the requirement has no meaningful variation.

## 2. Use This Exact Case Structure

1. Write fields in this order:
   1. `title`
   2. `description`
   3. `test_suite`
   4. `Covered requirement`
   5. `preconditions`
   6. `steps`
   7. `execution_type`
   8. `design_status`
   9. `test_engineer`
   10. `test_level`
   11. `jira`
   12. `Test script`
2. Keep `title` informative and unique. Include requirement or contract reference, scenario classification, and a concise behavior name.
3. Keep `preconditions` as a lettered list: `A)`, `B)`, `C)`.
4. Keep `steps` as a markdown table with columns `Step`, `Action`, and `Expected result`.
5. Keep `execution_type` as `Automated` unless the user explicitly wants manual cases.
6. Use `design_status` as `Draft`, `Ready`, or `Obsolete`.
7. Keep `Test script` granular. Link to the exact Java test file and the specific test method or display name, not only the file.

## 3. Make The Content API-Specific

1. Describe API behavior, not UI behavior.
2. Put auth state, seeded data, feature flags, or contract version details in `preconditions`.
3. In `steps`, describe the request action at a high level and put status, content type, headers, body semantics, and side effects in `Expected result`.
4. Include contract paths, operation ids, requirement ids, or acceptance-criteria ids in `Covered requirement`.
5. When runtime behavior differs from the documented contract, document the live executable expectation and reference the mismatch artifact separately.

## 4. Start From The Template

1. Start from [tdd-case-template.md](assets/tdd-case-template.md) for new case files.
2. Keep the field order unchanged so later sync and traceability work stays deterministic.
3. Use aggregate index files under `docs/testing/tdd/` only as navigation aids when the repo wants them.

## 5. Template

```markdown
title: [ORD-POST-001] MSS: Create order with required fields
description: Validates successful order creation for the standard required-field payload.
test_suite: Orders
Covered requirement: US-123, POST /api/orders, operationId=createOrder
preconditions:
A) The API is running.
B) Authentication is configured for a valid user.
C) No conflicting order id is pre-seeded.
steps:
| Step | Action | Expected result |
|---|---|---|
| 1 | Send `POST /api/orders` with a valid required-field payload | Status `201` is returned with JSON content. |
| 2 | Inspect the response body | The response includes the created order id and submitted business fields. |
| 3 | Retrieve the new order through `GET /api/orders/{id}` | The order is persisted and matches the creation response. |
execution_type: Automated
design_status: Ready
test_engineer: Codex
test_level: 1
jira: N/A
Test script: [OrderApiTest.java](C:/repo/tests/src/test/java/com/example/orders/OrderApiTest.java)#createOrderWithRequiredFields
```

## 6. Scenario Depth Decision

1. Use `MSS`, `EXT`, and `ERR` for CRUD, authentication, validation-heavy, workflow, or integration-sensitive requirements.
2. Use one `MSS` only for low-risk stable reads when optional data and error paths add little value.
3. Add a dedicated drift or compatibility scenario when the live runtime contradicts the contract or requirement.

## 7. Examples

1. Input: `Document POST /orders missing-customer-id as TDD.`
   Output: A dedicated `ERR` markdown case with lettered preconditions, a step table, and a direct link to the negative Rest Assured test method.
2. Input: `Document the owner create flow as TDD.`
   Output: One `MSS` case for successful creation and separate `EXT` or `ERR` cases only when the requirement meaningfully varies.

## 8. Troubleshooting

1. Problem: The automation file contains multiple test methods.
   Fix: Point `Test script` to the exact method anchor, not only the file.
2. Problem: The case reads like a raw HTTP transcript.
   Fix: Keep the action concise and move the protocol details into the expected result only where they matter.
3. Problem: A single document mixes success, variation, and error behavior.
   Fix: Split it into separate scenario files and classify them as `MSS`, `EXT`, or `ERR`.
