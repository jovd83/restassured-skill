# Schema And Contract Validation

1. Use JSON schema validation for stable structural guarantees.
2. Keep business assertions even when schema validation exists.
3. Validate required and optional fields from OpenAPI or Swagger artifacts.
4. Fail loudly on undocumented status codes.

## Example

```java
then()
    .body(matchesJsonSchemaInClasspath("schemas/orders/create-order-response.json"));
```
