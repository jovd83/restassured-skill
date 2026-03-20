---
name: restassured-transformer-testlink
description: Legacy Rest Assured-specific alias for TestLink case export. Prefer the standalone `test-artifact-export-skill` skill for transforming approved test cases into TestLink-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
metadata:
  author: jovd83
  version: "1.0"
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
