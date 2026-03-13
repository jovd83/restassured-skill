# Coverage Matrix

| Scenario ID | Feature | Endpoint Or Operation | Scenario | Type | Priority | Source | Execution Tag | Status |
|---|---|---|---|---|---|---|---|---|
| ORD-001 | Orders | `POST /orders` | Create order with valid payload | Happy path | High | `ORD-US01`, `createOrder` | `smoke`, `regression` | Proposed |

## Column Rules

1. `Scenario ID`: Use a stable local identifier.
2. `Feature`: Use the business feature or endpoint family.
3. `Endpoint Or Operation`: Use the REST path plus method or WSDL operation name.
4. `Scenario`: Describe one testable behavior only.
5. `Type`: Use values such as `Happy path`, `Validation`, `Auth`, `Negative`, `Workflow`, `Integration`, or `Contract`.
6. `Priority`: Use `High`, `Medium`, or `Low`.
7. `Source`: Include requirement IDs, contract operation IDs, or WSDL operations.
8. `Execution Tag`: List intended execution buckets such as `smoke`, `regression`, `contract`, or `integration`.
9. `Status`: Use `Proposed`, `Approved`, `Deferred`, `Blocked`, or `Implemented`.
