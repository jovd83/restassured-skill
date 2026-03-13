Title: [API-XXX-001] MSS: Describe the scenario behavior
Purpose: Explain the scenario objective in one sentence.
Covered requirement: <Story ID>, <Contract path>, operationId=<operationId>
Preconditions:
- The API is running.
- Authentication and test data are prepared.
- Any scenario-specific setup is complete.
Flow:
- Perform the primary API action.
- Observe the response and any side effects.
Expected outcome:
- The expected status and content type are returned.
- The required business fields, headers, and side effects are correct.
Test script: [ExampleApiTest.java](C:/repo/src/test/java/com/example/api/ExampleApiTest.java)#exampleScenario
