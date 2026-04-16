---
name: restassured-documentation-tests
description: Use when Codex needs to add human-readable documentation to Rest Assured automation code, including class purpose, role boundaries, shared specs, and scenario intent.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: automation-documentation, api-test-documentation
  dispatcher-accepted-intents: document_api_tests
  dispatcher-input-artifacts: test_suite, repo_context, traceability_artifacts
  dispatcher-output-artifacts: automation_docs, documentation_update
  dispatcher-stack-tags: restassured, documentation, automation
  dispatcher-risk: low
  dispatcher-writes-files: true
---

# Document Automation Code


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Document Only What Helps

1. Add class-level comments when the test role is not obvious.
2. Add short comments before complex setup or custom filters.
3. Do not add comments that restate the code literally.

## 2. Explain Boundaries

1. Explain shared specs, auth helpers, builders, and virtualization seams.
2. Explain why a test is tagged as smoke, contract, or integration when not obvious.

## 3. Troubleshooting

1. Problem: The code already reads clearly.
   Fix: Do not add noise comments.
