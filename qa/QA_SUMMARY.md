# Review Candidate v2 QA Summary

This is current review-candidate evidence, not a release approval. Historical main/release evidence and formal research evidence are not silently mixed into these counts.

| Evidence | Current v2 disposition | Scope |
|---|---|---|
| Eligible project targets | **48** | components + examples + research-labs direct children |
| Test-bearing targets | **46** | dynamic pytest matrix |
| Explicit non-applicable targets | **2** | research-only surfaces without tests directory |
| Component tests | **866 passed / 0 failed** | current v2 candidate |
| Whole-system tests | **21 cases / 11 scenario classes, PASS** | one-to-one registry in `WHOLE_SYSTEM_VALIDATION.json` |
| Branch coverage | **PASS measured** | 46 targets; report-only policy |
| Compileall, manifest, privacy, secret scans | **PENDING_FINAL_QA** | updated only after final evidence chain |

The old `412 PASSED / whole_system_validation = NOT_EXECUTED` wording is historical stale evidence and is not reused. The 48-target project surface and the 46-test-bearing/2-explicitly-non-applicable split are current v2 evidence.

Subjectivity, identity continuity, deployment, canonical promotion and independent IV&V remain unestablished or false.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```
