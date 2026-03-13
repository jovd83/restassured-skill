---
name: restassured-installer-intellij-junie
description: Use when Codex needs to set up IntelliJ IDEA for Rest Assured API testing with Java, Maven or Gradle, JUnit 5, and Junie-style workflow support.
---

# Install Rest Assured In IntelliJ

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
