---
name: restassured-transformer-testrail
description: Legacy Rest Assured-specific alias for TestRail case export. Prefer the standalone `test-artifact-export-skill` skill for transforming approved test cases into TestRail-ready artifacts, and use this only when Rest Assured-local conventions must be preserved explicitly.
metadata:
  author: jovd83
  version: "1.0"
  dispatcher-category: testing
  dispatcher-capabilities: test-artifact-formatting, api-legacy-export-transform
  dispatcher-accepted-intents: render_test_artifact, export_test_cases
  dispatcher-input-artifacts: approved_test_cases, normalized_test_case_model, destination_constraints
  dispatcher-output-artifacts: transformed_test_artifact, export_bundle
  dispatcher-stack-tags: restassured, transform, legacy-alias
  dispatcher-risk: low
  dispatcher-writes-files: true
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
