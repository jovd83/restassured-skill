---
name: restassured-orchestrator
description: Use when Codex receives a generic Rest Assured or service-testing request and must route the work into planning, implementation, documentation, execution, CI, virtualization, or test-management flows.
---

# Rest Assured Orchestrator

## 1. Clarify the Goal

1. Ask for the primary goal if the user request is ambiguous.
2. Classify the request into one of these buckets:
   1. Bootstrap a test module.
   2. Analyze requirements.
   3. Analyze OpenAPI or Swagger contracts.
   4. Analyze WSDL or SOAP contracts.
   5. Generate or review coverage.
   6. Implement or fix tests.
   7. Stub or virtualize downstream services.
   8. Configure CI.
   9. Document tests, traceability, quality, or failures.
   10. Regenerate a bundled reporting set.
   11. Transform, map, or report results to a test-management tool.

## 2. Route

1. Use `../bootstrap/SKILL.md` for missing setup.
2. Use `../analysis/requirements/SKILL.md` for stories, epics, and acceptance criteria.
3. Use `../analysis/contracts/SKILL.md` for REST contracts.
4. Use `../analysis/contracts-soap/SKILL.md` for SOAP contracts.
5. Use `../coverage_plan/generation/SKILL.md` for scenario generation.
6. Use `../coverage_plan/review/SKILL.md` for explicit approval.
7. Use `../core/SKILL.md` for implementation and defect fixing.
8. Use `../virtualization/SKILL.md` for WireMock and fault injection.
9. Use `../ci/SKILL.md` for pipeline work.
10. Use `../documentation/report-bundle/SKILL.md` when the goal is to refresh the reporting set as one operation.
11. Use `../documentation/*/SKILL.md` for documentation and diagnosis.
12. Use `../transformers`, `../mappers`, or `../reporters` for external tools.
13. When routing into test-case documentation, treat `docs/tests/<feature>/` as the canonical home for scenario-level docs and treat `docs/testing/` as index and reporting space.

## 3. Enforce the Sequence

1. Require approved requirements before generating a coverage plan.
2. Require an approved coverage plan before large-scale test implementation when the scenarios are AI-defined.
3. Skip approval only when the user already supplied the test cases or explicitly asked for direct implementation.
4. When the user asks for narrative documentation but not a format, choose TDD, BDD, plain text, or mixed mode explicitly before writing files.

## 4. Read When Needed

1. Read [routing-matrix.md](references/routing-matrix.md) for trigger phrases and routing shortcuts.

## 5. Examples

1. Input: `Help me test this payments service.`
   Output: Ask whether the goal is setup, planning, implementation, CI, documentation, or reporting.
2. Input: `Create scenarios from this OpenAPI and then implement them.`
   Output: Route to contracts analysis, coverage generation, review, then core.
3. Input: `Rebuild the coverage and quality reports for this API module.`
   Output: Route to `../documentation/report-bundle/SKILL.md`.
4. Input: `Check whether the narrative docs still match the API tests.`
   Output: Route to `../documentation/documentation-sync/SKILL.md`.
5. Input: `Document these approved payment scenarios, but keep each scenario separate.`
   Output: Route to the requested test-case format skill and store the canonical files under `docs/tests/payments/`.

## 6. Troubleshooting

1. Problem: The user mixes setup and implementation.
   Fix: Complete bootstrap first, then move into `core`.
2. Problem: The user asks for implementation without requirements or contracts.
   Fix: Proceed only if the requested tests are already enumerated or narrow enough to infer safely.
3. Problem: Documentation requests default to one oversized markdown file.
   Fix: Split TDD and plain-text docs into one scenario file per behavior and use feature files only where BDD grouping adds value.
