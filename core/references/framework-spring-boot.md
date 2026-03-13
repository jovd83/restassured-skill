# Spring Boot Recipe

1. Prefer Rest Assured against a running service for black-box API tests.
2. Use Spring profiles or test properties to point the service to disposable dependencies.
3. Use `@DynamicPropertySource` only when the repository already uses Spring test context patterns.
