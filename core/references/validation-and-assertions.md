# Validation And Assertions

1. Assert status first.
2. Assert `Content-Type` next.
3. Assert required headers next.
4. Assert semantic body fields next.
5. Assert side effects or cleanup last.

## Example

```java
then()
    .statusCode(201)
    .contentType(ContentType.JSON)
    .body("id", notNullValue())
    .body("status", equalTo("CREATED"));
```
