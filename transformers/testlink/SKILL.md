---
name: restassured-transformer-testlink
description: Use when Codex needs to transform Rest Assured API test cases from natural language or markdown into a TestLink-friendly import format.
---

# Transform Cases For TestLink

## 1. Collect Inputs

1. Read the approved TDD, BDD, or plain-text cases.
2. Preserve stable scenario IDs and titles.

## 2. Transform

1. Map titles, preconditions, steps, and expected results into the target TestLink structure.
2. Keep traceability references in the description or custom fields.

## 3. Troubleshooting

1. Problem: The source cases do not have stable IDs.
   Fix: Generate consistent local IDs before export.
