---
name: restassured-coverage-plan-review
description: Use when Codex needs to present a generated Rest Assured API coverage plan to the user, request explicit approval, and block implementation until the scope is confirmed.
metadata:
  author: jovd83
  version: "1.0"
---

# Review Coverage Plan

## 1. Present The Plan

1. Show the scenario matrix grouped by feature or endpoint.
2. Show the traceability source for each scenario.
3. Show explicit exclusions and open questions.

## 2. Request Approval

1. Ask whether the proposed scenario set is correct and complete.
2. Ask whether any scenario should be added, removed, or reprioritized.
3. Stop until the user approves the plan.

## 3. Record Decisions

1. Capture approved scope.
2. Capture deferred scope.
3. Capture assumptions that implementation may depend on.

## 4. Troubleshooting

1. Problem: The user wants direct implementation without review.
   Fix: Proceed only when the scenarios are already clearly defined or the user explicitly accepts the risk.
