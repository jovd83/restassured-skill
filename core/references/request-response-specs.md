# Request And Response Specs

## Request Spec Rules

1. Put base URI, common headers, auth filters, and content type in a shared request spec.
2. Keep scenario-specific path params, query params, and bodies in the test.

## Response Spec Rules

1. Reuse response specs only for stable expectations such as `200 + JSON`.
2. Keep business assertions in the scenario.

## Example

```java
RequestSpecification api = new RequestSpecBuilder()
        .setBaseUri(baseUrl)
        .setContentType(ContentType.JSON)
        .build();
```
