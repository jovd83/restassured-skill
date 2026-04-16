---
name: restassured-skill
description: Use when Codex needs to design, implement, run, document, or report Rest Assured API tests for REST services, contract-driven service tests, JUnit 5 automation, CI pipelines, or test-management integrations.
metadata:
    dispatcher-layer: execution
    dispatcher-lifecycle: active
  author: jovd83
  version: "1.1"
  dispatcher-category: testing
  dispatcher-capabilities: api-automation, restassured, api-test-planning, api-test-reporting
  dispatcher-accepted-intents: implement_api_confirmation_test, plan_api_test_coverage, document_api_tests, report_api_test_results
  dispatcher-input-artifacts: repo_context, api_requirements, api_contract, approved_test_cases, failing_api_scenario
  dispatcher-output-artifacts: restassured_test, coverage_plan, api_test_docs, traceability_report, routing_request
  dispatcher-stack-tags: restassured, api-testing, junit5
  dispatcher-risk: high
  dispatcher-writes-files: true
---

# Rest Assured Skill


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Start

1. Classify the request before writing files.
2. Use `bootstrap/SKILL.md` for new modules, missing dependencies, or missing test structure.
3. Use `orchestrator/SKILL.md` when the user asks for generic testing help and has not chosen planning, implementation, documentation, or reporting.
4. Use `core/SKILL.md` for Rest Assured implementation, assertions, auth, specs, DTOs, JUnit 5 structure, and execution.
5. Use `virtualization/SKILL.md` for WireMock, fault injection, or downstream API simulation.
6. Use `analysis/requirements/SKILL.md` for epics, stories, acceptance criteria, or prose requirements.
7. Use `analysis/contracts/SKILL.md` for OpenAPI or Swagger.
8. Use `analysis/contracts-soap/SKILL.md` for WSDL or SOAP contract analysis.
9. Use `coverage_plan/generation/SKILL.md` to turn approved requirements and contracts into scenarios.
10. Use `coverage_plan/review/SKILL.md` to request user approval before implementation.
11. Use `documentation/` skills for TDD, BDD, plain-text, mixed or absent narrative documentation, documentation sync, code docs, root-cause writeups, traceability reports, coverage-gap reports, OpenAPI change-impact reports, assertion-strength reports, bundled report regeneration, contract-mismatch notes, session-state tracking, or handover.
12. Use `ci/SKILL.md` for GitHub Actions, GitLab, Docker, tagging, parallelization, and artifacts.
13. Use `C:\projects\skills\test-artifact-export-skill\SKILL.md` for narrative test-case formatting and export artifacts.
14. Use `mappers/`, `reporters/`, and `reporting/stakeholder/` for execution reporting and stakeholder workflows.
15. Prefer canonical narrative docs under `docs/tests/<feature>/`; keep `docs/testing/` for reports, indexes, and generated human-readable portals.

## 1a. Dispatcher Integration

Use `skill-dispatcher` as the primary integration layer whenever this skill family needs help from another skill or when a broader orchestrator is deciding whether Rest Assured is the right execution layer.

1. Prefer dispatcher-led routing by intent, especially for `implement_api_confirmation_test`, `plan_api_test_coverage`, `render_test_artifact`, and `report_api_test_results`.
2. Prefer the repository's native API test stack over a new Rest Assured introduction when repo evidence points elsewhere.
3. Treat direct paths to sibling skills as a compatibility fallback, not as the primary integration contract.
4. Keep shared-memory usage limited to stable cross-project policy supplied externally, never task-local routing state.

## 2. Golden Rules

1. Inspect `pom.xml`, `build.gradle`, `build.gradle.kts`, and CI files before choosing dependency versions.
2. Default to JUnit 5 for new work unless the repository already standardizes on TestNG.
3. Prefer reusable `RequestSpecification` and `ResponseSpecification` objects over duplicated `given()` chains.
4. Assert status, headers, body semantics, and error payloads; do not stop at status code checks.
5. Create test data per test or per fixture; do not rely on execution order.
6. Log on failure and redact tokens, cookies, API keys, and personal data.
7. Use Testcontainers for dependencies owned by the system under test.
8. Use WireMock only for third-party or unstable dependencies that must be simulated.
9. Merge business requirements with API contracts before finalizing scenario coverage.
10. When a live service is available, prefer runtime-observed assertions over contract assumptions and record any mismatch explicitly.
11. Refuse placeholder tests, fake assertions, and undocumented assumptions.
12. Keep one canonical narrative artifact per executable scenario whenever the repo uses TDD or plain-text cases.
13. Use aggregate files under `docs/testing/` only as indexes or report entry points when scenario-level files exist.

## 3. Read Only What You Need

1. Read [capability-map.md](references/capability-map.md) when you need a routing shortcut.
2. Read [version-compatibility.md](references/version-compatibility.md) when Java or Rest Assured version selection is unclear.
3. Read [family-conventions.md](references/family-conventions.md) when naming, directory, or tagging conventions are needed.
4. Read [release-checklist.md](references/release-checklist.md) when preparing the skill family for publishing.

## 4. Examples

1. Input: `Create Rest Assured smoke tests for the order API from this OpenAPI file.`
   Output: Use `analysis/contracts`, then `coverage_plan/generation`, then `core`.
2. Input: `Set up a Maven JUnit 5 Rest Assured module in this repo.`
   Output: Use `bootstrap`.
3. Input: `Document the approved API scenarios as BDD and export them for Xray.`
   Output: Dispatch `render_test_artifact` through `skill-dispatcher`, then fall back to `C:\projects\skills\test-artifact-export-skill\SKILL.md` when needed.
4. Input: `The suite fails in CI only when the payment provider is down.`
   Output: Use `virtualization`, `ci`, and `documentation/root_cause`.
5. Input: `Create a resumable checkpoint so another agent can continue tomorrow.`
   Output: Use `documentation/session-state`.
6. Input: `The live API does not match OpenAPI. Document the gaps.`
   Output: Use `documentation/contract-mismatches`.
7. Input: `Show which tests cover each endpoint and method.`
   Output: Use `documentation/traceability-report`.
8. Input: `Show the biggest API coverage gaps.`
   Output: Use `documentation/coverage-gap-report`.
9. Input: `Compare these two API contracts and tell me which tests are affected.`
   Output: Use `documentation/openapi-change-impact-report`.
10. Input: `Tell me which Rest Assured tests are weak or only assert status codes.`
    Output: Use `documentation/assertion-strength-report`.
11. Input: `Refresh the full human-readable reporting set for this API module.`
    Output: Use `documentation/report-bundle`.
12. Input: `Check whether the TDD, BDD, or plain-text case files drifted away from the tests.`
    Output: Use `documentation/documentation-sync`.
13. Input: `Document the approved owner API scenarios as TDD.`
    Output: Dispatch `render_test_artifact` through `skill-dispatcher` and write one canonical file per scenario under `docs/tests/owner/`.

## 5. Troubleshooting

1. Problem: The user asks for generic API testing help with no scope.
   Fix: Use `orchestrator/SKILL.md` and force the user goal into planning, implementation, execution, documentation, or reporting.
2. Problem: The repository mixes Java 11 and Java 17 modules.
   Fix: Read `references/version-compatibility.md` and choose per-module compatibility instead of forcing one global version.
3. Problem: The request mixes user stories and OpenAPI input.
   Fix: Run both analysis skills and merge the result in `coverage_plan/generation`.
4. Problem: The live service contradicts the contract.
   Fix: Keep the tests aligned with observed runtime behavior and create a mismatch artifact with `documentation/contract-mismatches`.
5. Problem: The skill family needs a publish-readiness check before release.
   Fix: Run `python scripts/validate_skill_family.py`.
6. Problem: The mapping report points to aggregate documentation files instead of scenario-level artifacts.
   Fix: Move canonical narrative docs into `docs/tests/<feature>/` and update traceability to point to the scenario files, not only the index.

## 6. Gotchas

1. **Static Pollution:** `RestAssured.baseURI`, `port`, and `config` are static and persist across tests. Always reset them in `@AfterEach` or use `RequestSpecification` objects to avoid leaking state between test classes.
2. **Missing Content-Type:** Passing a DTO (POJO) to `.body()` does not automatically set `Content-Type: application/json`. Explicitly set the format via `.contentType(ContentType.JSON)` to avoid `415 Unsupported Media Type` errors.
3. **Logging Sensitive Data:** `.log().all()` captures everything, including Authorization headers and tokens. Use `.log().ifValidationFails()` or custom filters to redact sensitive information in CI/CD logs.
4. **Hamcrest Matcher Conflicts:** `org.hamcrest.Matchers` contains many common method names. Be careful with static imports if using other assertion libraries like AssertJ to avoid compilation errors or confusing IDE suggestions.
5. **JSON Path vs XML Path:** Rest Assured uses different GPath-like syntaxes for JSON and XML. A valid JSON path expression may not work for XML and vice-versa.
6. **Path Parameters Ordering:** When using unnamed path parameters (e.g., `.get("/{id}/{name}", 123, "test")`), the order is strict. Prefer named path parameters for clarity and robustness.
