# Maven And Gradle

## Maven

1. Use Surefire for normal test execution.
2. Use Failsafe only when the repo already splits integration tests by phase.
3. Run a narrow scope with `mvn -Dtest=OrdersApiTest test`.

## Gradle

1. Use `useJUnitPlatform()`.
2. Run a narrow scope with `./gradlew test --tests '*OrdersApiTest'`.
3. Separate custom tasks only when the repo already uses tag-based segmentation.
