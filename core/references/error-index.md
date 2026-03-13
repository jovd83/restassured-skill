# Error Index

| Error | Likely Cause | Fix |
|---|---|---|
| `Connection refused` | Service not running or bad `BASE_URL` | Start the service or fix the URL |
| `SSLHandshakeException` | TLS mismatch or self-signed cert | Fix trust config; do not default to relaxed SSL |
| `No tests found` | Wrong runner or filter | Check JUnit 5 setup and test task |
| `JsonPathException` | Wrong body path or non-JSON response | Inspect content type and response body |
| `401 Unauthorized` | Missing or invalid auth | Fix token generation or headers |
