---
name: restassured-ci
description: Use when Codex needs to configure or troubleshoot Rest Assured API tests in CI pipelines, including JUnit 5 execution, tags, Docker, containers, artifacts, quality gates, and provider-specific pipeline examples.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: ci-configuration, restassured-ci
  dispatcher-accepted-intents: configure_api_test_ci, optimize_api_test_execution
  dispatcher-input-artifacts: repo_context, ci_pipeline, test_module
  dispatcher-output-artifacts: ci_guidance, execution_plan, pipeline_update
  dispatcher-stack-tags: restassured, ci, api-testing
  dispatcher-risk: medium
  dispatcher-writes-files: true
---

# Rest Assured CI


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Choose The Pipeline Shape

1. Detect the CI system first.
2. Run smoke tags before full regression when pipeline time matters.
3. Use containers or disposable services for integration tests.

## 2. Configure Execution

1. Use provider guidance from [github-actions.md](references/github-actions.md), [gitlab.md](references/gitlab.md), or [other-ci.md](references/other-ci.md).
2. Use [junit5-tagging-and-suites.md](references/junit5-tagging-and-suites.md) for JUnit 5 selection.
3. Use [docker-and-containers.md](references/docker-and-containers.md) for containerized execution.
4. Use [parallelization.md](references/parallelization.md) for sharding or split-by-tag execution.
5. Use [reporting-and-artifacts.md](references/reporting-and-artifacts.md) for JUnit XML and logs.
6. Use [quality-gates.md](references/quality-gates.md) when the pipeline must fail on coverage, drift, or weak-assertion thresholds.
7. Use `python scripts/evaluate_quality_gates.py` when the quality-gate evaluation must be deterministic and reusable across CI jobs.

## 3. Add Quality Gates

1. Fail the pipeline on contract-enforcement regressions only when the repo has explicitly opted into strict gates.
2. Use the coverage-gap report to enforce `no uncovered operations` or `no unreviewed drift-only operations` when the team wants coverage hardening.
3. Use the assertion-strength report to enforce thresholds such as `no weak tests` or `max transport-only tests`.
4. Keep quality gates separate for runtime-aligned suites and contract-enforcement suites when both exist.
5. Regenerate the reporting bundle before applying report-based gates.
6. Prefer `python scripts/evaluate_quality_gates.py --coverage-gap <gap-md> --assertion-strength <strength-md> --contract-mismatches <mismatch-md>` instead of rewriting threshold logic inline in CI YAML.

## 4. Troubleshooting

1. Problem: CI cannot reach the service under test.
   Fix: Verify network, startup ordering, and environment variables before changing the tests.
2. Problem: Tag-based selection runs zero tests.
   Fix: Verify JUnit 5 tag configuration and test task flags.
3. Problem: The pipeline fails because report-based gates are stale.
   Fix: Regenerate the bundle reports before evaluating gate thresholds.
4. Problem: CI duplicates threshold logic in multiple jobs.
   Fix: Move the evaluation into `scripts/evaluate_quality_gates.py`.
