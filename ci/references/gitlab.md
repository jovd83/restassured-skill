# GitLab CI

1. Use a Java image that matches the module version.
2. Start dependencies as services only when that is simpler than Testcontainers.
3. Publish JUnit XML via `artifacts:reports:junit`.
