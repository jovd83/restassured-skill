---
name: restassured-documentation-handover
description: Use when Codex needs to produce a concise handover for completed Rest Assured API testing work, including what changed, what remains open, and how to continue safely.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: handover, api-test-handover
  dispatcher-accepted-intents: create_api_test_handover
  dispatcher-input-artifacts: work_summary, validation_status, blockers
  dispatcher-output-artifacts: handover_document, resume_steps
  dispatcher-stack-tags: restassured, handover, operations
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Handover

## 1. Summarize The Work

1. List the implemented or updated tests.
2. List the environments or contracts used.
3. List the commands used for verification.
4. Update the session-state artifact before finalizing the handover.
5. If contract drift was observed, point the reader to the contract-mismatch artifact.

## 2. Record Remaining Risk

1. List open questions.
2. List blocked scenarios.
3. List unverified assumptions.

## 3. Point To Next Actions

1. State what should happen next.
2. State who or what input is needed next.
3. Point the reader to the persisted session-state file.
4. Point the reader to the mismatch artifact when executable tests had to diverge from the contract.
