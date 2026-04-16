---
name: restassured-documentation-session-state
description: Use when Codex needs to persist a durable resume checkpoint for Rest Assured API testing work so a human or later agent can see what is done, what is blocked, and exactly how to continue.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: session-state, api-test-session-state
  dispatcher-accepted-intents: record_api_test_session_state
  dispatcher-input-artifacts: work_state, touched_files, blockers
  dispatcher-output-artifacts: session_state_record, resume_pointer
  dispatcher-stack-tags: restassured, session-state, operations
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Persist Session State


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Choose The File

1. Prefer `docs/testing/session-state.md` in the target repository.
2. Use `.ai/session-state.md` only when the repository already stores agent artifacts under `.ai/`.
3. Keep one active session-state file per workstream.

## 2. Start From The Template

1. Copy the structure from [session-state-template.md](assets/session-state-template.md).
2. Preserve all section headings.
3. Replace placeholder text with concrete repo-specific state.

## 3. Record The Current State

1. State the objective in one sentence.
2. State the current status, last update time, active owner, and intended next owner.
3. State the approved scope and exclusions.
4. List the inputs used, including requirements, contracts, tickets, and environments.
5. List the files created or changed.
6. List the commands already run and their outcomes.
7. List completed work.
8. List remaining work in execution order.
9. List blockers and open questions separately.
10. List assumptions and risks explicitly.

## 4. Make The File Resumable

1. Add the exact next command or first next step.
2. Add the exact file or class that should be opened next.
3. Add the exact verification step still required.
4. Add a short `Resume Here` section that another agent can follow without re-reading the full thread.

## 5. Update It At The Right Times

1. Update the file after major implementation steps.
2. Update the file after each new test slice, coverage artifact, or contract-analysis expansion.
3. Update the file before handing work back to a human.
4. Update the file before stopping with blockers or unresolved failures.
5. Update the file after changing scope, assumptions, or contracts.
6. Update the file after every verification run that changes the known result, even when the run fails.

## 6. Keep It Honest

1. Do not mark work complete unless the relevant files exist.
2. Do not claim verification unless the command was actually run.
3. Do not hide blockers inside assumptions.
4. Do not delete unresolved questions; move them into the open-questions section.
5. Do not let the session-state lag behind the actual scope by more than one major work item.

## 7. Examples

1. Input: `Leave a checkpoint so another agent can resume the payments API work.`
   Output: Create or update `docs/testing/session-state.md` with completed files, failed and pending commands, blockers, and the next exact step.
2. Input: `Summarize where you left off after this contract-analysis pass.`
   Output: Update the session-state artifact with the analyzed contracts, unresolved mismatches, and the next coverage-planning step.

## 8. Troubleshooting

1. Problem: The repository already has multiple ad hoc status files.
   Fix: Consolidate the active state into one canonical session-state file and link older notes under `Inputs Used` or `History`.
2. Problem: The next agent cannot tell what was verified.
   Fix: Add exact commands and outcomes under `Verification Run`.
3. Problem: The work stopped because of a human decision.
   Fix: Put the decision request under `Blockers` and repeat it in `Resume Here`.
4. Problem: The session-state still reflects an earlier slice after new tests or docs were added.
   Fix: Reconcile `Scope`, `Files Created Or Changed`, `Verification Run`, and `Remaining Work` immediately before stopping.
