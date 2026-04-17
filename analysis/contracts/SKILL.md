---
name: restassured-analysis-contracts
description: Use when Codex needs to derive Rest Assured test scenarios from OpenAPI or Swagger contracts, including endpoints, methods, schemas, auth rules, status codes, and error conditions.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: contract-analysis, restassured-contract-analysis
  dispatcher-accepted-intents: analyze_api_contract
  dispatcher-input-artifacts: api_contract, openapi_spec, repo_context
  dispatcher-output-artifacts: contract_analysis, api_test_candidates, open_questions
  dispatcher-stack-tags: restassured, analysis, contract
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Analyze REST Contracts


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Load The Contract

1. Prefer OpenAPI or Swagger files already in the repo.
2. Run `python scripts/extract_openapi_summary.py --input <path-or-url>` to produce a normalized summary.
3. Read [openapi-swagger-analysis.md](references/openapi-swagger-analysis.md) when the contract contains advanced features.

## 2. Extract Testable Surface

1. List paths, methods, tags, and operation IDs.
2. List auth schemes and which operations require them.
3. List path, query, header, and body parameters.
4. List required vs optional request fields.
5. List documented status codes, response schemas, and error payloads.
6. Use the script output as the baseline summary, then read the raw contract only for unresolved details.

## 3. Choose The Assertion Mode

1. Use `runtime-aligned` mode when the suite exists to prove the live service behavior that consumers actually receive.
2. Use `contract-enforcement` mode when the goal is strict specification conformance, drift detection, or contract hardening.
3. Use `mixed` mode when both matter: keep runtime-aligned regression tests separate from contract-enforcement checks.
4. Record the chosen mode in the coverage plan so implementation and reporting stay consistent.
5. Record the dominant OpenAPI tags and any explicit user priority for tags so coverage planning can order work intentionally.

## 4. Convert To Test Candidates

1. Create happy-path candidates for every in-scope operation.
2. Create validation candidates for required fields, formats, enums, and boundaries.
3. Create authorization candidates from security requirements.
4. Create negative candidates from documented `4xx` and `5xx` responses.
5. In `contract-enforcement` or `mixed` mode, add explicit drift-detection candidates for status, content type, auth, required fields, and schema shape.
6. Flag undocumented behavior instead of inventing expected results.
7. Group candidates by tag before handing them to coverage planning when the contract is tag-rich or the user asked for domain-priority ordering.

## 5. Merge With Business Requirements

1. Prefer business requirements when they are more specific than the contract.
2. Flag conflicts instead of silently choosing one source.
3. Hand the merged result to `../../coverage_plan/generation/SKILL.md`.

## 5. Examples

1. Input: `Derive tests from openapi/orders.yaml.`
   Output: A normalized matrix of operations, validations, auth rules, and error responses ready for coverage planning.

## 6. Troubleshooting

1. Problem: The contract is YAML and parsing fails.
   Fix: Install `PyYAML` or convert the file to JSON, then rerun the script.
2. Problem: The contract omits business rules such as inventory side effects.
   Fix: Merge in user stories before finalizing the scenario list.
3. Problem: The live runtime already diverges from the contract.
   Fix: Choose `mixed` mode unless the user asked for pure contract enforcement.
