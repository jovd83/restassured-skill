# Observability And Redaction

1. Prefer `log().ifValidationFails()` over `log().all()`.
2. Redact `Authorization`, `Cookie`, `Set-Cookie`, `X-Api-Key`, and personal identifiers.
3. Attach correlation IDs to aid triage.
