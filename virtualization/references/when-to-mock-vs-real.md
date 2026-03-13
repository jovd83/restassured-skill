# When To Mock Vs Real

| Situation | Use Real Dependency | Use Stub |
|---|---|---|
| Owned database or queue | Yes | No |
| Third-party billing API | No | Yes |
| Unstable sandbox | Maybe | Often yes |
| Contract verification against provider | Prefer real or provider contract checks | No |
