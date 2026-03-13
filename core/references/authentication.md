# Authentication

## Rules

1. Centralize token acquisition.
2. Cache tokens only when they are stable and safe for the suite.
3. Prefer request filters or support helpers over copy-pasted headers.
4. Separate user roles explicitly.

## Common Patterns

1. Client credentials for service-to-service APIs.
2. Login endpoint tokens for user-role tests.
3. Static sandbox keys only when the environment mandates them.
