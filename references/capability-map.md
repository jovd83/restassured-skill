# Capability Map

## Documentation Convention

- Keep canonical narrative docs under `docs/tests/<feature>/`.
- Keep `docs/testing/` for reports, indexes, sync artifacts, and HTML portals.
- Keep one TDD or plain-text file per executable scenario.
- Use BDD feature files per capability or resource group, then map individual scenarios from those files.

| Need | Skill |
|---|---|
| Scaffold or retrofit a Rest Assured module | `bootstrap/SKILL.md` |
| Route a generic testing request | `orchestrator/SKILL.md` |
| Implement Rest Assured tests | `core/SKILL.md` |
| Stub downstream APIs | `virtualization/SKILL.md` |
| Extract requirements from epics or stories | `analysis/requirements/SKILL.md` |
| Extract tests from OpenAPI or Swagger | `analysis/contracts/SKILL.md` |
| Extract tests from WSDL or SOAP contracts | `analysis/contracts-soap/SKILL.md` |
| Generate a scenario matrix | `coverage_plan/generation/SKILL.md` |
| Ask the user to approve a scenario matrix | `coverage_plan/review/SKILL.md` |
| Keep docs and coverage aligned | `coverage_plan/auto-sync/SKILL.md` |
| Write test cases in TDD format with one canonical scenario file per case | `documentation/test_cases/tdd/SKILL.md` |
| Write test cases in BDD format grouped by capability or resource | `documentation/test_cases/bdd/SKILL.md` |
| Write concise plain-text cases with one canonical scenario file per case | `documentation/test_cases/plain_text/SKILL.md` |
| Keep narrative docs aligned with tests and traceability | `documentation/documentation-sync/SKILL.md` |
| Document automation code | `documentation/tests/SKILL.md` |
| Explain a failure | `documentation/root_cause/SKILL.md` |
| Map endpoints to tests and docs | `documentation/traceability-report/SKILL.md` |
| Summarize the biggest API coverage gaps | `documentation/coverage-gap-report/SKILL.md` |
| Compare two OpenAPI contracts and map impact to tests | `documentation/openapi-change-impact-report/SKILL.md` |
| Rate the strength of current Rest Assured assertions | `documentation/assertion-strength-report/SKILL.md` |
| Refresh the full HTML and markdown reporting set | `documentation/report-bundle/SKILL.md` |
| Record contract vs runtime drift | `documentation/contract-mismatches/SKILL.md` |
| Persist resume state for human or agent handoff | `documentation/session-state/SKILL.md` |
| Produce a handover note | `documentation/handover/SKILL.md` |
| Configure pipelines | `ci/SKILL.md` |
| Produce stakeholder reports | `reporting/stakeholder/SKILL.md` |
| Transform cases for test tools | `transformers/*/SKILL.md` |
| Map external IDs to local docs | `mappers/*/SKILL.md` |
| Report results back to a test tool | `reporters/*/SKILL.md` |
