# Service Test Types

| Type | Purpose | Typical JUnit tag |
|---|---|---|
| Smoke | Confirm health and one critical path | `smoke` |
| Regression | Validate stable business behavior | `regression` |
| Contract | Validate schema and field-level contract stability | `contract` |
| Integration | Validate behavior with real dependencies | `integration` |
| Negative | Validate failures and abuse handling | `negative` |
| Workflow | Validate multi-step state changes | `workflow` |
