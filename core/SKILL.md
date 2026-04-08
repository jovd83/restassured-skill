---
name: restassured-core
description: Use when Codex needs to implement, refactor, debug, or extend Rest Assured API tests with JUnit 5, reusable request and response specifications, authentication helpers, DTOs, contract checks, and service-test best practices.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: api-automation, restassured-core, api-test-implementation
  dispatcher-accepted-intents: implement_api_confirmation_test, debug_api_test, review_api_test
  dispatcher-input-artifacts: repo_context, requirements, api_contract, failing_api_scenario
  dispatcher-output-artifacts: api_test, implementation_guidance, fix_plan
  dispatcher-stack-tags: restassured, api-testing, implementation
  dispatcher-risk: high
  dispatcher-writes-files: true
---

# Rest Assured Core

## 1. Preflight

1. Inspect the build file, Java version, test engine, and module boundaries.
2. Inspect API documentation, existing contracts, auth flow, and environment variables.
3. Read [preflight.md](references/preflight.md) before major changes.

## 2. Choose the Test Shape

1. Use [service-test-types.md](references/service-test-types.md) to classify the test as smoke, regression, contract, integration, negative, or workflow.
2. Read [project-structure.md](references/project-structure.md) before creating new packages.
3. Use JUnit 5 patterns from [junit5-patterns.md](references/junit5-patterns.md).
4. Use build guidance from [maven-and-gradle.md](references/maven-and-gradle.md).
5. Decide whether the suite is `runtime-aligned`, `contract-enforcement`, or `mixed` before writing assertions.

## 3. Implement the Backbone

1. Build shared request and response specs from [request-response-specs.md](references/request-response-specs.md).
2. Centralize auth logic with [authentication.md](references/authentication.md).
3. Add semantic assertions using [validation-and-assertions.md](references/validation-and-assertions.md).
4. Add schema or contract checks only when they increase signal; use [schema-and-contract-validation.md](references/schema-and-contract-validation.md).
5. Build deterministic test data with [test-data-management.md](references/test-data-management.md).
6. In `runtime-aligned` mode, assert the live behavior in executable tests and route discrepancies to `../documentation/contract-mismatches/SKILL.md`.
7. In `contract-enforcement` mode, keep assertions aligned to the specification and tag the tests so drift is visible as an explicit contract failure.
8. In `mixed` mode, keep runtime-aligned regression tests separate from contract-enforcement checks by tag, package, or class naming.

## 4. Add Service-Test Details

1. Read [testcontainers-and-wiremock.md](references/testcontainers-and-wiremock.md) before introducing containers or stubs.
2. Read [observability-and-redaction.md](references/observability-and-redaction.md) before enabling request or response logging.
3. Read [security-negative-testing.md](references/security-negative-testing.md) for authz, authn, and abuse cases.
4. Read [graphql-and-file-upload.md](references/graphql-and-file-upload.md) for GraphQL or multipart endpoints.
5. Read [xml-and-soap-payloads.md](references/xml-and-soap-payloads.md) for XML or SOAP payload handling.
6. Read the framework recipe that matches the repo: [framework-spring-boot.md](references/framework-spring-boot.md), [framework-quarkus.md](references/framework-quarkus.md), or [framework-micronaut.md](references/framework-micronaut.md).

## 5. Run and Debug

1. Run the narrowest relevant test first.
2. Use [debugging.md](references/debugging.md) for triage.
3. Use [error-index.md](references/error-index.md) when a common failure pattern appears.
4. If a failure reveals contract drift, capture the raw request, raw response metadata, and affected contract path before changing assertions.
5. When a contract-enforcement test fails because the runtime drift is already known, preserve the failing evidence and link it to the mismatch artifact instead of muting the test silently.

## 6. Examples

1. Input: `Implement POST /orders negative tests from the approved coverage plan.`
   Output: Add `OrdersApiTest`, shared specs, data builders, and explicit `400`, `401`, `403`, `409`, and `422` assertions.
2. Input: `Refactor these duplicated given/when/then chains.`
   Output: Extract request and response specs plus auth support before changing test intent.
3. Input: `The OpenAPI says JSON but the live 404 returns XML.`
   Output: Keep the executable test aligned to the live XML response, then document the contract mismatch separately.
4. Input: `Keep strict contract checks, but do not break the main regression suite.`
   Output: Put the contract-enforcement assertions in a separate tagged slice and keep the runtime-aligned suite stable.

## 7. Troubleshooting

1. Problem: The suite uses static `RestAssured.baseURI` everywhere.
   Fix: Move configuration into request specs or JUnit lifecycle setup.
2. Problem: Tests pass only when run in order.
   Fix: Isolate data setup and cleanup per test or per fixture.
3. Problem: Logs expose secrets.
   Fix: Add redaction filters and restrict full logging to failures.
4. Problem: The contract and runtime disagree on status, content type, or payload shape.
   Fix: Treat the live runtime as the source for executable assertions, then create a mismatch record instead of forcing the test to match the contract.
5. Problem: The user needs both regression stability and strict spec conformance.
   Fix: Split the suite into runtime-aligned and contract-enforcement slices instead of forcing one assertion mode to do both jobs.
