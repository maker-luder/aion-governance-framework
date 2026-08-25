## Scope

Describe the bounded maintenance or preservation change and why it is needed.

> Public contribution intake is closed while the repository is frozen. This template is for explicitly authorized maintenance, preservation, security, or historical-integrity work; it does not reopen the terminated project work loop.

## Boundary checklist

- [ ] This change does not restart active research or feature development.
- [ ] This change does not authorize deployment or canonical promotion.
- [ ] Historical event-time records are preserved; any correction is additive or clearly scoped.
- [ ] No private conversations, credentials, tokens, personal data, or unrelated private material are added.
- [ ] Conceptual authorship, implementation provenance, review, approval, and Git commit identity are not silently conflated.
- [ ] Any scientific or subjectivity-related statement preserves the repository's standing non-claims unless new independently sufficient evidence is explicitly reviewed.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
AUTOMATIC_RESTART = NO
```

## Validation

List the exact tests, scans, build checks, and relevant GitHub Actions evidence for the proposed head. A passing CI result is evidence about the checked state; it is not merge authority, scientific validation, certification, or deployment authority.

## Main transition authority

A change targeting `main` requires a **fresh, exact-head, target-specific Human Owner approval receipt** under the repository's Main Transition Authority Gate. Prior approval, broad maintenance permission, CI success, or AI review must not be reused as merge authority for a different head.
