---
name: restassured-reporter-testrail
description: Use when Codex needs to report Rest Assured API test execution results back to TestRail through its API using local case mappings and execution evidence.
metadata:
  author: jovd83
  version: "1.0"
---

# Report Results To TestRail

## 1. Gather Inputs

1. Collect the TestRail URL and credentials securely.
2. Collect execution results and mappings.

## 2. Report

1. Report statuses per mapped case.
2. Attach concise evidence for failures.

## 3. Troubleshooting

1. Problem: The target run is missing.
   Fix: Create or confirm the correct TestRail run before publishing.
