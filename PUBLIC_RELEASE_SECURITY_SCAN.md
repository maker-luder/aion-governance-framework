# Public Release Security and Privacy Scan

Status: `PRIVACY_CONTROL_HARDENING / HUMAN_REVIEW_REQUIRED`

The repository security audit scans exact HEAD Git objects for high-confidence secrets,
unexpected binaries, security-boundary documents, workflow permissions, and selected
privacy/linkability indicators.

Privacy checks now include:

- non-noreply HEAD author-email classification without printing the address;
- email-shaped contact identifiers outside external-source paths;
- non-generic actor labels in section-style `HUMAN_ORIGIN` records;
- required public privacy-minimization documentation.

This is an offline heuristic scan, not penetration testing, legal privacy certification,
identity verification, or a complete Git-history purge.

```text
READ_ONLY
CURRENT_TREE_SCAN != FULL_HISTORY_ERASURE
HISTORY_REWRITE = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
HUMAN_OWNER_REVIEW_REQUIRED
```
