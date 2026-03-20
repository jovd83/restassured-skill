---
name: restassured-transformer-zephyr
description: Legacy Rest Assured-specific alias for Zephyr case export. Prefer the standalone `test-artifact-export-skill` skill for transforming approved test cases into Zephyr-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
metadata:
  author: jovd83
  version: "1.0"
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
