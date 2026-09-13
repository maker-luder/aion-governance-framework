# Read-only repository security audit

Status: `IMPLEMENTED_BOUNDED_AUDIT / HUMAN_REVIEW_REQUIRED`

This minimal scanner implements the PR #102 P2 candidate by examining only files
already tracked in a local Git worktree. It records the exact commit and tree,
unexpected binary suffixes, a small set of high-confidence secret markers,
required security documents, relative links inside those documents, top-level
workflow permission declarations and an inventory of external-download
instructions. It does not fetch, execute or classify downloaded software.

Run from the repository root:

```text
python scripts/audit_repository_security.py --root . --output receipt.json
```

Exit status is `1` when HIGH or CRITICAL findings exist and `0` otherwise.
MEDIUM findings remain visible for Human review. Matching is intentionally narrow:
a clean result is not a complete security assessment or evidence that no secret,
malware, dependency vulnerability or compromised history exists.

```text
READ_ONLY
AUDIT_PASS != SECURITY_ASSURED
PATTERN_MATCH != CONFIRMED_SECRET
NO_PATTERN_MATCH != NO_SECRET
UNEXPECTED_BINARY != MALWARE
CODEQL_PASS != REPOSITORY_SECURITY_VALIDATED
HUMAN_OWNER_REVIEW_REQUIRED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

Backup and restore verification remains the separate Draft PR #105 surface. No
security-product binary or malware scanner is added because the repository has no
tracked executable payload and the source note makes a justified threat a
precondition for that later step.
