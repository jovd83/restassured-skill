---
name: restassured-documentation-bdd
description: Legacy Rest Assured-specific alias for BDD case formatting. Prefer the standalone `test-artifact-export-skill` skill for Gherkin, BDD, and export-ready case rendering, and use this only when Rest Assured-local conventions must be preserved explicitly.
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

# Document Test Cases In BDD

## 1. Store And Organize Files

1. Store feature files under `docs/features/` or `docs/tests/features/`.
2. Create one `.feature` file per API capability, feature, or resource group.
3. Group scenarios by requirement or business rule, not by raw HTTP method alone.
4. Keep aggregate index files under `docs/testing/` optional; treat the `.feature` files themselves as the canonical narrative artifacts.
5. For non-trivial requirements, document at least three scenarios:
   1. `MSS` for the main success path.
   2. `EXT` for meaningful valid variations.
   3. `ERR` for validation, auth, not-found, conflict, or drift behavior.
6. For trivial low-risk reads, one `MSS` scenario is sufficient.

## 2. Use Standard Gherkin Structure

1. Start with a `Feature:` statement that names the API capability.
2. Use `Background:` only for shared setup such as base environment, auth state, seeded data, or contract version.
3. Use `Scenario:` for single cases and `Scenario Outline:` only when the same behavior really varies by data.
4. Use `Examples:` tables for compact data variations.
5. Add tags above scenarios for requirement ids, operation ids, and scope such as `@smoke`, `@regression`, `@contract`, `@negative`, or `@US-123`.

## 3. Write API-Focused Steps

1. Put environment, auth state, or seeded data in `Given`.
2. Put request actions in `When`.
3. Put status, content type, critical headers, body semantics, and side effects in `Then`.
4. Use `And` and `But` only to extend the current clause clearly.
5. Keep wording business-readable and API-specific.
6. Do not turn the scenario into a low-value transcript of raw HTTP syntax.

## 4. Start From The Template

1. Start from [feature-template.feature](assets/feature-template.feature) for new capability files.
2. Keep scenario titles stable because traceability reports link to them.
3. Keep one feature file per capability or resource group; do not collapse the whole service into one giant file.

## 5. Depth Rules

1. Always include a standard `MSS` scenario for the primary valid request.
2. Add `EXT` coverage for optional fields, alternate filters, paging, sorting, or valid role-specific variants.
3. Add `ERR` coverage for invalid input, unauthorized access, missing resources, duplicate requests, or contract drift.
4. Add a dedicated drift scenario when the runtime behavior does not match the documented contract.

## 6. Example

```gherkin
@SPC-OWN-003 @addOwner @workflow
Feature: Owner management

  Scenario: Create an owner with required fields
    Given the Spring Petclinic API is available
    And no owner exists for the generated last name
    When a client submits a valid owner payload to POST /api/owners
    Then the response status is 201
    And the response body contains the created owner id
    And the created owner can be retrieved by id
```

## 7. Examples

1. Input: `Write BDD for GET /orders/{id} unauthorized access.`
   Output: A tagged `ERR` scenario with `Given`, `When`, and `Then` steps for `401` behavior.
2. Input: `Document the create-order requirement in BDD.`
   Output: Separate `MSS`, `EXT`, and `ERR` scenarios unless the requirement is trivial.

## 8. Troubleshooting

1. Problem: The scenario reads like a curl command transcript.
   Fix: Keep steps behavioral and move raw payload detail into data tables or examples only when needed.
2. Problem: One feature file mixes unrelated capabilities.
   Fix: Split by resource or business capability.
3. Problem: A complex requirement has only one scenario.
   Fix: Add the missing `EXT` and `ERR` scenarios before calling the documentation complete.
