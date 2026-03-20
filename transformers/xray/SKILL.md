---
name: restassured-transformer-xray
description: Legacy Rest Assured-specific alias for Xray case export. Prefer the standalone `test-artifact-export-skill` skill for transforming approved test cases into Xray-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
metadata:
  author: jovd83
  version: "1.0"
---

# Transform Cases For Xray

## 1. Collect Inputs

1. Read the approved cases.
2. Preserve stable IDs, tags, and requirement links.

## 2. Transform

1. Convert BDD scenarios into Xray-compatible feature content when BDD is used.
2. Convert structured cases into JSON or CSV when BDD is not used.

## 3. Troubleshooting

1. Problem: The source content mixes multiple scenarios in one file.
   Fix: Split them before export.
