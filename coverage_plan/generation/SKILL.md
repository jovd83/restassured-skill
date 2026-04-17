---
name: restassured-coverage-plan-generation
description: Use when Codex needs to generate a Rest Assured API test coverage plan from approved requirements, OpenAPI or Swagger contracts, WSDL analysis, and explicit scope constraints.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: coverage-planning, api-coverage-planning, restassured-coverage-planning
  dispatcher-accepted-intents: plan_api_test_coverage, generate_api_test_coverage_plan
  dispatcher-input-artifacts: analysis_baseline, approved_requirements, api_contract, scope_constraints, repo_context
  dispatcher-output-artifacts: coverage_plan, scenario_matrix, approval_request
  dispatcher-stack-tags: restassured, coverage-planning, api-testing
  dispatcher-risk: medium
  dispatcher-writes-files: false
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Generate Coverage Plan

## 1. Confirm Inputs

1. Require approved requirements, approved contract analysis, or both.
2. List the in-scope features, endpoints, roles, and environments.
3. List the excluded scope explicitly.
4. Capture any explicit priority order for OpenAPI tags, business domains, or endpoint groups before ordering the matrix.

## 2. Build The Scenario Matrix

1. Create happy-path scenarios.
2. Create validation scenarios for required fields, formats, ranges, enums, and body shape.
3. Create authentication and authorization scenarios.
4. Create negative and error-response scenarios.
5. Create workflow and state-transition scenarios.
6. Create integration or virtualization scenarios when dependencies matter.
7. Create a dedicated contract-mismatch section whenever a live environment already exists or historical drift is known.
8. When the contract uses tags, group the scenario matrix by tag unless the user asked for a different grouping.
9. Order tag groups by explicit user priority first, then by business criticality, then by contract breadth.

## 3. Add Traceability

1. Map each scenario to its requirement ID, contract path, or WSDL operation.
2. Keep one row per scenario.
3. Mark the intended execution type, for example smoke, regression, contract, or integration.
4. Mark mismatch rows explicitly as `Contract mismatch` instead of hiding them inside generic negative coverage.
5. Keep the tag or domain group visible in each row when tag-based prioritization is active.

## 4. Output

1. Output a human-readable matrix.
2. Start from [coverage-matrix-template.md](assets/coverage-matrix-template.md) when the user has not specified a different format.
3. Keep the columns stable so later sync and reporting work can reuse the matrix.
4. Hand the matrix to dispatcher intent `review_api_test_coverage_plan` for explicit approval.
5. If mismatch scenarios exist, send the approved mismatch rows to `../../documentation/contract-mismatches/SKILL.md`.

If dispatcher routing is unavailable, use `../review/SKILL.md` for approval.

## 5. Examples

1. Input: `Generate coverage for Orders from AUTH-US02 and openapi/orders.yaml.`
   Output: A matrix that merges story coverage with contract-derived validations and errors.
2. Input: `Generate coverage for the live Petstore API and capture known drift from OpenAPI.`
   Output: A matrix with separate happy-path, negative, and contract-mismatch rows.
3. Input: `Generate coverage for the billing API, but prioritize the Payments and Refunds tags first.`
   Output: A matrix grouped by tag with Payments and Refunds ordered ahead of the remaining tag groups.

## 6. Troubleshooting

1. Problem: The contract contains endpoints outside the user scope.
   Fix: Exclude them explicitly instead of silently dropping them.
2. Problem: The live API already behaves differently from the contract.
   Fix: Add dedicated `Contract mismatch` rows and keep them traceable to both the contract path and the observed runtime evidence.
3. Problem: The contract has many tags and the matrix becomes noisy.
   Fix: Keep only in-scope tags, order them explicitly, and group rows under the surviving tag headings.