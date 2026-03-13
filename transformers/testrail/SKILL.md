---
name: restassured-transformer-testrail
description: Use when Codex needs to transform Rest Assured API test cases from natural language or markdown into a TestRail-friendly import format.
---

# Transform Cases For TestRail

## 1. Collect Inputs

1. Read the approved cases.
2. Preserve requirement and contract references.

## 2. Transform

1. Map titles, sections, preconditions, steps, and expected results into the TestRail format.
2. Keep tags or labels for smoke, regression, contract, and integration when supported.

## 3. Troubleshooting

1. Problem: The suite hierarchy is unclear.
   Fix: Group by feature or endpoint family before export.
