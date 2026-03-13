---
name: restassured-transformer-zephyr
description: Use when Codex needs to transform Rest Assured API test cases from natural language or markdown into a Zephyr-friendly import format.
---

# Transform Cases For Zephyr

## 1. Collect Inputs

1. Read approved source cases.
2. Preserve stable titles and traceability references.

## 2. Transform

1. Map scenario metadata into the Zephyr import structure.
2. Preserve execution labels when the target format supports them.

## 3. Troubleshooting

1. Problem: The source cases are missing expected results.
   Fix: Fill the gap before export.
