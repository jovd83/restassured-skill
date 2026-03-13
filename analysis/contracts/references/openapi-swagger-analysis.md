# OpenAPI And Swagger Analysis

1. Use `operationId` when present; otherwise use method plus path.
2. Treat `required` request fields as mandatory validation candidates.
3. Treat enums, patterns, min/max constraints, and formats as boundary candidates.
4. Treat `security` blocks as auth scenario drivers.
5. Treat every documented response code as an explicit scenario candidate.
6. Flag undocumented error behavior instead of guessing it.
7. Use `tags` as planning metadata, not just labels. They are often the cleanest way to prioritize scenario groups when the user thinks in business domains.
8. When tags are too broad or inconsistent, fall back to business requirements or path groups instead of forcing tag-based ordering.
