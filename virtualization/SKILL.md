---
name: restassured-virtualization
description: Use when Codex needs to simulate downstream HTTP services for Rest Assured suites with WireMock, stub mappings, latency, retries, fault injection, or isolation from unstable third-party dependencies.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: service-virtualization, api-dependency-virtualization
  dispatcher-accepted-intents: virtualize_api_dependencies
  dispatcher-input-artifacts: dependency_contract, virtualization_scope, repo_context
  dispatcher-output-artifacts: virtualization_config, test_stubs, guidance
  dispatcher-stack-tags: restassured, virtualization, api-testing
  dispatcher-risk: medium
  dispatcher-writes-files: true
---

# Service Virtualization

## 1. Decide Whether To Mock

1. Mock only third-party or unstable dependencies.
2. Keep real dependencies for the system under test whenever practical.
3. Read [when-to-mock-vs-real.md](references/when-to-mock-vs-real.md) before adding stubs.

## 2. Create The Stub Layer

1. Use WireMock for HTTP downstream dependencies.
2. Model stable happy-path stubs first.
3. Add negative behavior only when the scenario requires it.
4. Read [wiremock-patterns.md](references/wiremock-patterns.md) for stub structure.

## 3. Inject Failure Modes

1. Add latency, resets, malformed payloads, and error statuses deliberately.
2. Read [fault-injection.md](references/fault-injection.md) before writing resilience tests.

## 4. Verify Intent

1. Assert that the system under test handled the dependency behavior correctly.
2. Assert that the stub was called only when interaction verification matters.

## 5. Examples

1. Input: `Simulate the shipping provider timing out.`
   Output: Add a WireMock delayed response and assert the API returns the documented fallback error.
2. Input: `Stub the tax provider for local CI.`
   Output: Add deterministic success and validation-failure stubs, then route the tests to the stub base URL.

## 6. Troubleshooting

1. Problem: The suite still calls the live dependency.
   Fix: Verify the service under test points to the stubbed base URL.
2. Problem: Contract drift breaks the stub.
   Fix: Rebuild the stub from the latest contract or response samples.
