---
name: restassured-analysis-requirements
description: Use when Codex needs to extract testable API behavior from epics, user stories, acceptance criteria, tickets, markdown docs, or other prose requirements before generating Rest Assured scenarios.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: requirements-analysis, api-requirements-analysis, restassured-requirements-analysis
  dispatcher-accepted-intents: analyze_api_requirements, derive_api_testable_behaviors
  dispatcher-input-artifacts: requirements, user_story, acceptance_criteria, ticket, markdown_docs, repo_context
  dispatcher-output-artifacts: analysis_baseline, requirement_summary, open_questions, routing_request
  dispatcher-stack-tags: restassured, analysis, api-testing
  dispatcher-risk: low
  dispatcher-writes-files: false
---

## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `./log-dispatch.cmd --skill <skill_name> --intent <intent> --reason <reason>` (or `./log-dispatch.sh` on Linux)

# Analyze Requirements

## 1. Find Sources

1. Search the repo for stories, epics, acceptance criteria, ADRs, specs, and tickets.
2. Read the user-provided requirement source completely.
3. Extract only behavior that affects API requests, responses, authorization, validation, workflow state, integrations, or observability.

## 2. Normalize The Requirements

1. Convert prose into testable behaviors.
2. Separate happy path, validation, authorization, negative, and workflow behaviors.
3. Mark missing details explicitly instead of inventing them.

## 3. Validate With The User

1. Present the summarized behaviors.
2. Ask the user to confirm that the requirement summary is complete.
3. Stop before coverage generation when the summary is not approved.

## 4. Output Shape

1. Group the output by feature or endpoint area.
2. Include the source identifier for each behavior when available.
3. Highlight gaps that must be resolved by contract analysis or user clarification.

## 5. Examples

1. Input: `Derive tests from these checkout user stories.`
   Output: A grouped list of API behaviors, validations, permissions, and edge cases tied back to story IDs.

## 6. Troubleshooting

1. Problem: The requirements mention UI behavior only.
   Fix: Extract only the backend behavior that the API must enforce or expose.
2. Problem: The requirements conflict with the contract.
   Fix: Surface the mismatch and request clarification before implementation.

## 7. Handoff

Use dispatcher intent `plan_api_test_coverage` when the next step is scenario planning.

If dispatcher routing is unavailable, hand off to `../coverage_plan/generation/SKILL.md`.