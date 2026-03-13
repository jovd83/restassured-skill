---
name: restassured-transformer-xray
description: Use when Codex needs to transform Rest Assured API test cases from natural language or markdown into an Xray-friendly import format.
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
