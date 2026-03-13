# Family Conventions

## Directory Layout

```text
src/test/java/<package>/
  clients/
  models/
  support/
  tests/
src/test/resources/
```

## Documentation Layout

```text
docs/
  tests/
    <feature>/
      <scenario>-mss.md
      <scenario>-ext.md
      <scenario>-err.md
    features/
      <capability>.feature
  testing/
    test-mapping-report.md
    contract-mismatches.md
    coverage-gap-report.md
    documentation-sync-report.md
    html/
```

1. Keep TDD and plain-text case files under `docs/tests/<feature>/`.
2. Keep one canonical TDD or plain-text file per executable scenario.
3. Keep BDD feature files under `docs/features/` or `docs/tests/features/`.
4. Keep `docs/testing/` for reports, indexes, and generated HTML, not as the primary home for scenario-level case content.

## Naming

1. Name test classes by resource or workflow, for example `OrdersApiTest`.
2. Name helper specs by role, for example `Specifications`, `AuthSupport`, or `ResponseChecks`.
3. Name JUnit tags from execution intent, for example `smoke`, `regression`, `contract`, `integration`, `negative`.
4. Name scenario docs with a stable purpose and depth suffix such as `create-order-mss.md` or `missing-owner-err.md`.

## Assertion Conventions

1. Assert status first.
2. Assert content type and critical headers next.
3. Assert semantic fields next.
4. Assert cleanup or side effects last when the scenario mutates data.
