# Privacy Review

Audit date: 2026-10-08  
Status: `PRIVACY_REMEDIATION_CANDIDATE / HUMAN_REVIEW_REQUIRED`

This review distinguishes current public-tree content from immutable/reachable historical Git metadata.

## Scope reviewed

- current default-branch tracked text and provenance records;
- public PR/issue text searches for direct chat identifiers;
- direct-linkability terms found in Human-origin/history documents;
- recent Git commit author-email metadata sampling;
- existing security/privacy scanner coverage.

## Direct-linkability findings and remediation

1. A private chat nickname appeared as a named `HUMAN_ORIGIN` actor in one public research document.
   The privacy branch replaces it with a generic Human-user label.
2. A private third-party teacher identity appeared in two public history/research documents.
   The privacy branch removes the identity while preserving the minimum research meaning.
3. PR #298 contained a chat nickname, exact chat time, and local timezone in the public PR body.
   The PR body was edited after merge to remove those linkable fields without changing Git history.
4. The governed owner-learning source digest is re-bound to the sanitized current bytes and its source version is incremented.

## Git metadata finding

A sample of the 100 most recent commits reachable from main found 99 commit-author addresses using a
general personal-email provider class and 1 privacy-preserving GitHub noreply address.

The address values are intentionally not reproduced in this review.

An ordinary PR cannot remove author email from existing commit objects. Full removal would require a
history rewrite/force push, coordination of branches/tags/clones, and potentially GitHub cache/support
cleanup. That destructive operation is **not authorized by this privacy-remediation branch**.

```text
CURRENT_TREE_DIRECT_LINKABILITY = REMEDIATION_CANDIDATE
GIT_HISTORY_AUTHOR_EMAIL_EXPOSURE = PRESENT
HISTORY_REWRITE = HOLD
FORCE_PUSH = NOT_AUTHORIZED
CURRENT_PR_MERGE = NOT_AUTHORIZED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
HUMAN_OWNER_REVIEW_REQUIRED
```

## Non-findings / retained material

- No current tracked-file occurrence of the sampled private author-email value was found by repository code search.
- No public PR/issue search hit was found for the removed chat nickname or sampled private author-email value after the PR #298 body redaction.
- Public-source author/contact metadata inside reviewed external-source snapshots is not treated as the Human user's private identity.
- Generic timezones, cities, dates, and synthetic fixtures are not automatically personal data; linkability and source role control the decision.
- De-identified naturalistic Human–AI learning observations remain research abstractions unless they contain direct or reasonably linkable personal details.

## Control correction

The earlier statement that the reconstructed public tree had simply "passed" privacy review was too broad.
The repository security audit is extended in this branch to:

- report a non-noreply HEAD author email without printing the address;
- review email-shaped contact identifiers outside external-source paths;
- flag non-generic actor labels in section-style `HUMAN_ORIGIN` records;
- require the public privacy-minimization control document.

References:

- GitHub: Removing sensitive data from a repository  
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- NIST Privacy Framework  
  https://www.nist.gov/privacy-framework
