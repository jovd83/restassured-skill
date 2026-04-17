---
name: restassured-bootstrap
description: Use when Codex needs to scaffold, retrofit, or normalize a Java Rest Assured test module with JUnit 5, Maven or Gradle, shared specifications, and an initial runnable smoke test.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: test-bootstrap, restassured-bootstrap
  dispatcher-accepted-intents: bootstrap_api_test_module
  dispatcher-input-artifacts: repo_context, build_tool, target_module
  dispatcher-output-artifacts: bootstrap_changes, smoke_test, setup_guidance
  dispatcher-stack-tags: restassured, bootstrap, api-testing
  dispatcher-risk: high
  dispatcher-writes-files: true
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Bootstrap Rest Assured

## 1. Inspect

1. Detect the build tool from `pom.xml`, `build.gradle`, or `build.gradle.kts`.
2. Detect the Java version from compiler settings, toolchains, or CI.
3. Detect the active test engine from dependencies and existing tests.
4. Detect existing HTTP test libraries before adding Rest Assured.

## 2. Choose a Baseline

1. Use JUnit 5 for new work unless the repository clearly standardizes on TestNG.
2. Use Rest Assured `6.x` only when Java `17+` is available.
3. Use Rest Assured `5.5.x` for Java `11` compatibility.
4. Add `json-schema-validator`, Testcontainers, or WireMock only when the request requires them.

## 3. Scaffold

1. Run `python bootstrap/scripts/init_restassured_module.py --help` to inspect options.
2. Run the script with the target path, package, build tool, and Java version.
3. Pass a known stable smoke endpoint with `--smoke-path` when the target API does not expose `/health`.
4. Let the script derive an endpoint-specific smoke test class name from `--smoke-path`, or override it explicitly with `--smoke-class-name`.
3. Generate:
   1. The build file additions.
   2. `src/test/java/<package>/support/Specifications.java`.
   3. `src/test/java/<package>/tests/<DerivedSmokeClass>.java`.
   4. `src/test/resources/test.properties`.
4. Skip overwriting user files unless the request explicitly allows replacement.

## 4. Verify

1. Run the narrowest test command first.
2. Use the generated smoke test class name for the first targeted run, for example `mvn -Dtest=OpenapiSmokeTest test`.
3. Use the generated smoke test class name for Gradle, for example `./gradlew test --tests '*OpenapiSmokeTest'`.
4. Fix missing env vars, base URLs, or TLS settings before writing more tests.

## 5. Read When Needed

1. Read [bootstrap-checklist.md](references/bootstrap-checklist.md) before scaffolding a new module.
2. Read [dependency-matrix.md](references/dependency-matrix.md) when choosing dependencies or plugin wiring.

## 6. Examples

1. Input: `Set up Maven JUnit 5 Rest Assured tests under services/orders.`
   Output:
   ```bash
   python bootstrap/scripts/init_restassured_module.py --path services/orders --build maven --package com.example.orders --java-version 17
   ```
2. Input: `Retrofit this Gradle Java 11 repo without forcing a Java upgrade.`
   Output:
   ```bash
   python bootstrap/scripts/init_restassured_module.py --path . --build gradle --package com.example.api --java-version 11 --restassured-version 5.5.7
   ```
3. Input: `Bootstrap tests for Swagger Petstore, using the OpenAPI endpoint as smoke check.`
   Output:
   ```bash
   python bootstrap/scripts/init_restassured_module.py --path dry-run/petstore-tests --build maven --package com.example.petstore --java-version 17 --smoke-path /api/v3/openapi.json
   ```
4. Input: `Bootstrap tests for /store/inventory and force a specific smoke class name.`
   Output:
   ```bash
   python bootstrap/scripts/init_restassured_module.py --path services/store-tests --build maven --package com.example.store --java-version 17 --smoke-path /store/inventory --smoke-class-name StoreInventorySmokeTest
   ```

## 7. Troubleshooting

1. Problem: The repo already has JUnit 4 only.
   Fix: Add JUnit Jupiter carefully and update the selected test task or Surefire version.
2. Problem: The smoke test fails with `Connection refused`.
   Fix: Confirm `BASE_URL` and server startup order before changing the test.
3. Problem: The target repo uses Kotlin Gradle scripts.
   Fix: Generate Gradle output for `.kts` syntax and keep the repo's existing style.
4. Problem: The generated smoke test uses the wrong endpoint.
   Fix: Rerun the bootstrap script with `--smoke-path` pointing at a stable endpoint exposed by the target API.
5. Problem: The generated smoke test class name is too generic or awkward.
   Fix: Rerun the bootstrap script with `--smoke-class-name` and keep the endpoint-specific path.