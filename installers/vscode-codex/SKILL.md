---
name: restassured-installer-vscode-codex
description: Use when Codex needs to set up VS Code for Rest Assured API testing with Java, Maven or Gradle, JUnit 5, and Codex-driven workflow support.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: editor-setup, api-test-editor-setup
  dispatcher-accepted-intents: setup_api_test_editor
  dispatcher-input-artifacts: editor_choice, repo_context, local_environment
  dispatcher-output-artifacts: editor_setup_steps, configuration_guidance
  dispatcher-stack-tags: restassured, setup, editor
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Install Rest Assured In VS Code


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Set Up The IDE

1. Install Java support extensions.
2. Install Maven or Gradle support.
3. Confirm the Java runtime matches the target repo.

## 2. Set Up The Project

1. Use `../../bootstrap/SKILL.md` if the project lacks a Rest Assured test module.
2. Confirm test commands run from the integrated terminal.

## 3. Troubleshooting

1. Problem: Test discovery fails.
   Fix: Verify JUnit 5 support and the selected Java runtime.
