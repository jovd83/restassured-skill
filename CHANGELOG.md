# Changelog

All notable changes to the `restassured-skill` repository will be documented in this file.

The format is based on Keep a Changelog and uses a simple `Added`, `Changed`, and `Fixed` structure so future releases stay easy to scan.

## [Unreleased]

### Added
- Placeholder for new skills, references, templates, or helper scripts.

### Changed
- Placeholder for updates to prompts, routing, report formats, or packaging.

### Fixed
- Placeholder for script fixes, validation fixes, or documentation corrections.

## [2.0.0] - 2026-09-27

### Removed
- `transformers/`, `mappers/` and `reporters/` for TestRail, Xray, Zephyr and TestLink (12 sub-skills). They were near-identical copies of the same work in the Playwright, Cypress and Rest Assured packs. Exporting cases, mapping tool IDs back into tests, and publishing results now live in the standalone `test-management-sync` skill (formerly `test-artifact-export-skill`).

### Changed
- Routing names `test-management-sync` directly, instead of going through the retired skill-dispatcher with a hard-coded `C:\projects\skills\...` fallback path.
- The legacy test-case formatting aliases point to `test-management-sync`.
- Version markers reconciled: SKILL.md said 1.1 and the README badge 1.0, with no changelog entry after 0.1.0.

## [0.1.0] - 2026-03-13

### Added
- Initial public release of the Rest Assured skill family.
- 41 skills covering bootstrap, core implementation, requirements and contract analysis, coverage planning, documentation, virtualization, CI, installers, and test-management integrations.
- Deterministic helper scripts for OpenAPI and WSDL extraction, HTML report generation, quality gates, release manifests, and family validation.
- Support for TDD, BDD, plain-text, mixed, and no-narrative reporting workflows.

### Changed
- Standardized the repository layout so the GitHub repository root is the skill root.

### Fixed
- Corrected plain-text documentation detection in the documentation-sync audit workflow.
