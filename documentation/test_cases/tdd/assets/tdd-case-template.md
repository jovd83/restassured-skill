title: [API-XXX-001] MSS: Describe the scenario behavior
description: Summarize the scenario intent in one sentence.
test_suite: <Feature or resource>
Covered requirement: <Story ID>, <Contract path>, operationId=<operationId>
preconditions:
A) The API is running.
B) Authentication and test data are prepared.
C) Any scenario-specific setup is complete.
steps:
| Step | Action | Expected result |
|---|---|---|
| 1 | Perform the primary API action. | The expected status and content type are returned. |
| 2 | Inspect the returned data. | The required business fields and headers are correct. |
| 3 | Verify any follow-up read or side effect. | The system state matches the expected outcome. |
execution_type: Automated
design_status: Draft
test_engineer: Codex
test_level: 1
jira: N/A
Test script: [ExampleApiTest.java](C:/repo/src/test/java/com/example/api/ExampleApiTest.java)#exampleScenario
