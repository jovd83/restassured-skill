# Project Structure

```text
src/test/java/com/example/api/
  clients/
  models/
  support/
  tests/
src/test/resources/
```

## Rules

1. Put shared request and response specs under `support/`.
2. Put endpoint wrappers under `clients/` only when repetition justifies them.
3. Put DTOs under `models/`.
4. Put scenario classes under `tests/`.
