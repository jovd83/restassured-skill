---
name: restassured-reporter-zephyr
description: Use when Codex needs to report Rest Assured API test execution results back to Zephyr through its API using local case mappings and execution evidence.
metadata:
  author: jovd83
  version: "1.0"
---

# Report Results To Zephyr

## 1. Gather Inputs

1. Collect Zephyr credentials securely.
2. Collect execution results and mappings.

## 2. Report

1. Map each result to the correct Zephyr case.
2. Attach concise evidence for failures.

## 3. Troubleshooting

1. Problem: The execution status mapping is wrong.
   Fix: Normalize local statuses before sending them.
