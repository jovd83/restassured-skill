---
name: restassured-installer-intellij-junie
description: Use when Codex needs to set up IntelliJ IDEA for Rest Assured API testing with Java, Maven or Gradle, JUnit 5, and Junie-style workflow support.
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

# Install Rest Assured In IntelliJ


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Set Up The IDE

1. Import the project with the correct JDK.
2. Enable Maven or Gradle sync.
3. Confirm JUnit 5 test discovery works in the IDE.

## 2. Set Up The Project

1. Use `../../bootstrap/SKILL.md` when the repo lacks the required test structure.
2. Confirm the target run configuration uses the right env vars.

## 3. Troubleshooting

1. Problem: IntelliJ runs a different JDK than CI.
   Fix: Align the project SDK, Gradle JVM, and test runtime.
