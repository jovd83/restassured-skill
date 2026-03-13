# JUnit 5 Patterns

## Preferred Annotations

1. Use `@Test` for single scenarios.
2. Use `@ParameterizedTest` for validation matrices and idempotent status matrices.
3. Use `@Nested` to group endpoint behavior.
4. Use `@Tag` for smoke, regression, contract, integration, and negative.
5. Use `@BeforeEach` only for lightweight setup.

## Example

```java
@Tag("regression")
class OrdersApiTest {

    @Nested
    class CreateOrder {

        @Test
        void rejectsMissingCustomerId() {
        }
    }
}
```
