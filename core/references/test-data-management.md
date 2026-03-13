# Test Data Management

1. Prefer builders or factories over inline maps for complex bodies.
2. Generate unique identifiers with timestamps, UUIDs, or deterministic counters.
3. Clean up created resources when the API allows it.
4. Avoid shared mutable fixtures across parallel tests.
