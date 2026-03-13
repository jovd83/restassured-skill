# Version Compatibility

| Java | Rest Assured guidance | Action |
|---|---|---|
| 17+ | Prefer `6.x` | Use the latest compatible 6.x release present in the repo or organization standard |
| 11 | Prefer `5.5.x` unless the repo already upgraded | Keep the 5.x line to avoid a forced Java uplift |
| 8 | Treat as legacy | Do not add modern dependencies until the user approves a compatibility path |

## Selection Rules

1. Read the build file before choosing a version.
2. Match the version already used elsewhere in the mono-repo when possible.
3. Prefer upgrading only the target module, not unrelated modules.
4. Keep JUnit 5 as the default test engine for new work.
