# Read-only repository security audit

Status: `IMPLEMENTED_BOUNDED_AUDIT / HUMAN_REVIEW_REQUIRED`

This minimal scanner implements the P2 candidate canonically recorded by merged
PR #102. The audit receipt is bound to an exact Git `HEAD` commit and tree, so the
scanner reads that same tree through Git object APIs (`ls-tree` / `cat-file`)
rather than reading index or working-tree bytes. Dirty tracked changes and
untracked files are therefore not silently attributed to the recorded HEAD tree.

The scanner records unexpected binary suffixes, a small set of high-confidence
secret markers, required security documents, relative links inside those
documents, top-level workflow permission declarations, and an inventory of
external-download instructions. Relative-link existence is evaluated against the
same HEAD tree. Workflow permission review accepts an explicit read-only baseline
and flags absent or non-read top-level capability for Human review. It does not
fetch, execute or classify downloaded software.

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
SCAN_SOURCE = HEAD_GIT_OBJECTS
WORKING_TREE_CONTENT_USED = FALSE
RECORDED_HEAD_TREE = SCANNED_HEAD_TREE
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
established threat requiring one in this bounded audit. The exact-object scan
improves provenance; it does not expand the scanner into malware analysis or
historical compromise adjudication.
