# Debugging

1. Reproduce with the narrowest failing test.
2. Log on validation failure.
3. Print the actual response body when deserialization fails.
4. Compare the failing environment against local config, auth, and test data assumptions.
5. Capture request IDs and container logs when dependencies are involved.
