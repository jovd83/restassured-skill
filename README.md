# Rest Assured Skill Guides

Battle-tested Rest Assured and service-testing skills for REST APIs, contract analysis, documentation, CI, and reporting. **41 skills** covering bootstrap, execution, planning, virtualization, traceability, and test-management integrations.

## What are Agent Skills?
[Agent Skills](https://github.com/agentskills/agentskills) are a simple, open format for giving AI agents capabilities and expertise. They are folders of instructions, scripts, and resources that agents can discover and use to perform better at specific tasks. Write once, use everywhere.

## Installation Manual

This repository provides Rest Assured skills designed for AI coding assistants such as OpenAI Codex, Junie, and other agents that support the Agent Skills format.

### Step 1: Base Installation
Add the full skill family and let the agent route to the right sub-skill:

```bash
npx skills add jovd83/restassured-skill
```

### Step 2: Customizing Your Setup
If you only need specific packs, add only those folders.

**Core Delivery**

```bash
npx skills add jovd83/restassured-skill/orchestrator
npx skills add jovd83/restassured-skill/bootstrap
npx skills add jovd83/restassured-skill/core
npx skills add jovd83/restassured-skill/virtualization
npx skills add jovd83/restassured-skill/ci
```

**Planning, Contracts, and Documentation**

```bash
npx skills add jovd83/restassured-skill/analysis/requirements
npx skills add jovd83/restassured-skill/analysis/contracts
npx skills add jovd83/restassured-skill/analysis/contracts-soap
npx skills add jovd83/restassured-skill/coverage_plan/generation
npx skills add jovd83/restassured-skill/coverage_plan/review
npx skills add jovd83/restassured-skill/coverage_plan/auto-sync
npx skills add jovd83/restassured-skill/documentation/report-bundle
npx skills add jovd83/restassured-skill/documentation/traceability-report
npx skills add jovd83/restassured-skill/documentation/documentation-sync
npx skills add jovd83/restassured-skill/documentation/test_cases/tdd
npx skills add jovd83/restassured-skill/documentation/test_cases/bdd
npx skills add jovd83/restassured-skill/documentation/test_cases/plain_text
```

**Reporting and Integrations**

```bash
npx skills add jovd83/restassured-skill/reporting/stakeholder
npx skills add jovd83/restassured-skill/transformers/xray
npx skills add jovd83/restassured-skill/mappers/xray
npx skills add jovd83/restassured-skill/reporters/xray
npx skills add jovd83/restassured-skill/installers/vscode-codex
npx skills add jovd83/restassured-skill/installers/intellij-junie
```

### Manual Installation (Alternative)
If you prefer not to use `npx skills`, clone the repository and place it where your agent looks for local skills:

```bash
git clone https://github.com/jovd83/restassured-skill.git
```

Typical locations:

- `~/.agents/skills/`
- `~/.cursor/skills/`
- IDE-specific local skills directories supported by your agent tooling

Because this repository root is the skill root, copy the repository contents directly into the target skills location or keep the cloned folder as `restassured-skill`.

## Skills Overview

| Skill Pack | Scope | What's Covered |
|---|---|---|
| **bootstrap** | Setup | Maven and Gradle setup, dependency wiring, starter module scaffolding, smoke-test generation |
| **core** | Implementation | Rest Assured patterns, JUnit 5 structure, request and response specs, auth, data, schema checks, framework recipes |
| **analysis** | Inputs | Requirements extraction, OpenAPI and Swagger analysis, SOAP and WSDL analysis |
| **coverage_plan** | Planning | Scenario matrix generation, review, and auto-sync |
| **documentation** | Documentation and reports | TDD, BDD, plain text, traceability, mismatch reports, coverage gaps, assertion strength, report bundles, session state |
| **virtualization** | Dependencies | WireMock patterns, fault injection, mock-vs-real guidance |
| **ci** | Delivery | GitHub Actions, GitLab, containers, parallelization, quality gates |
| **reporting / transformers / mappers / reporters** | Enterprise integration | Stakeholder reporting and test-management tool flows for TestLink, TestRail, Xray, and Zephyr |
| **installers** | IDE setup | VS Code + Codex and IntelliJ + Junie guidance |

## Highlights

- Rest Assured-first API automation with JUnit 5 defaults
- Requirements-driven and contract-driven coverage generation
- Support for TDD, BDD, plain-text, mixed, or absent narrative documentation
- Human-readable markdown and HTML reporting bundles
- Contract mismatch, coverage gap, assertion strength, and OpenAPI change-impact reporting
- Session-state and handover flows for human-in-the-loop work
- Deterministic helper scripts for extraction, reporting, validation, and release packaging

## Repository Layout

```text
SKILL.md
bootstrap/
core/
analysis/
coverage_plan/
documentation/
virtualization/
ci/
reporting/
transformers/
mappers/
reporters/
installers/
scripts/
references/
```

## Validation

Run the built-in family validator:

```powershell
python .\scripts\validate_skill_family.py --root .
```

Generate a release manifest for packaging reviews:

```powershell
python .\scripts\generate_release_manifest.py --root . --output .\release-manifest.md
```

## Defaults Used Across This Repo

- Prefer JUnit 5 for new Rest Assured work unless the target repo already standardizes differently.
- Prefer reusable request and response specifications over duplicated `given()` chains.
- Prefer scenario-level narrative docs under `docs/tests/<feature>/`.
- Keep `docs/testing/` for reports, indexes, and generated HTML portals.
- Prefer runtime-observed assertions over contract assumptions once a live service is available.
