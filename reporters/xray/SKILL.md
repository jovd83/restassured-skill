---
name: restassured-reporter-xray
description: Use when Codex needs to report Rest Assured API test execution results back to Xray through its API using local case mappings and execution evidence.
metadata:
  author: jovd83
  version: "1.0"
---

# Report Results To Xray

## 1. Gather Inputs

1. Collect Xray or Jira credentials securely.
2. Collect execution results and mappings.

## 2. Report

1. Map results to test issue keys.
2. Send concise evidence for failures and blocked states.

## 3. Troubleshooting

1. Problem: The execution file format is rejected.
   Fix: Validate the payload shape against the selected Xray API.
