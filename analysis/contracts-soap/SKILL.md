---
name: restassured-analysis-contracts-soap
description: Use when Codex needs to derive service-test scenarios from WSDL or SOAP contracts and translate them into HTTP and XML checks that can still be implemented with Rest Assured where appropriate.
metadata:
  author: jovd83
  version: '1.0'
  dispatcher-category: testing
  dispatcher-capabilities: soap-contract-analysis, restassured-soap-contract-analysis
  dispatcher-accepted-intents: analyze_soap_contract
  dispatcher-input-artifacts: wsdl_contract, repo_context
  dispatcher-output-artifacts: contract_analysis, api_test_candidates, open_questions
  dispatcher-stack-tags: restassured, analysis, soap
  dispatcher-risk: low
  dispatcher-writes-files: false
---

# Analyze SOAP Contracts


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## 1. Confirm Scope

1. Confirm that SOAP or WSDL is truly in scope.
2. Keep this skill for contract analysis and scenario design.
3. Escalate if the user expects a dedicated SOAP framework rather than Rest Assured-based HTTP and XML checks.

## 2. Load The Contract

1. Run `python scripts/extract_wsdl_summary.py --input <path>` to extract services, ports, and operations.
2. Read [wsdl-analysis.md](references/wsdl-analysis.md) when namespaces or bindings are complex.

## 3. Extract Testable Surface

1. List services, ports, operations, and SOAP actions.
2. List required request elements and expected response elements when visible.
3. List fault contracts and fault codes when declared.

## 4. Convert To Test Candidates

1. Create happy-path candidates per operation.
2. Create XML validation candidates for required fields and namespaces.
3. Create fault-path candidates from declared SOAP faults.
4. Flag WS-Security and complex attachment cases explicitly.

## 5. Examples

1. Input: `Derive tests from legacy/customer.wsdl.`
   Output: A SOAP operation matrix with required XML elements, faults, and auth concerns.

## 6. Troubleshooting

1. Problem: The WSDL imports external schemas that are missing.
   Fix: Resolve the schema set before finalizing the scenario list.
2. Problem: The target uses heavy WS-Security or attachments.
   Fix: State that Rest Assured may not be the best primary implementation tool for that branch.
