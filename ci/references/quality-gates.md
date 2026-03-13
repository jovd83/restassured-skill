# Quality Gates

## Use These Gates Only When The Team Asked For Them

1. Keep report-driven quality gates opt-in.
2. Start with warning-only mode before switching the pipeline to fail-fast.
3. Keep runtime-aligned and contract-enforcement gates separate when both suites exist.

## Recommended Gate Types

1. Coverage gate
   - Fail when `Not covered > 0` for in-scope operations.
   - Fail when `Contract drift > 0` unless each drift row is explicitly accepted.
2. Assertion-strength gate
   - Fail when `Weak > 0` for critical suites.
   - Warn when `Transport-only` exceeds the agreed threshold.
3. Contract-enforcement gate
   - Fail only the contract lane when a strict spec-conformance check regresses.
4. Report freshness gate
   - Regenerate the bundle first so the gate evaluates current artifacts.
5. Deterministic evaluation gate
   - Use `python scripts/evaluate_quality_gates.py` so threshold logic does not get duplicated across CI jobs.

## Keep The Gates Practical

1. Do not fail the main regression lane just because a known-drift contract test exists in a separate contract lane.
2. Do not gate on narrative documentation format. BDD, TDD, plain text, mixed, or absent narrative docs must all remain valid.
3. Make thresholds explicit in CI variables or build parameters instead of hardcoding them into scripts.
