# Coupled-Cognition Quality Factory — external post-freeze record

A new external research module was added to address the failure mode in which a human and LLM mutually correct each other yet can still converge on the same false model.

The research direction uses the repository's existing IQC/IPQC/QC/QA and NCR/CAPA vocabulary and adds a mandatory counterevidence lane plus independent-evidence release gates.

Core invariants:

- `MUTUAL_AGREEMENT != TRUTH`
- `CONVERGENCE != VALIDATION`
- `COHERENCE != CORRECTNESS`
- `COUNTEREVIDENCE_ROUTE_REQUIRED`
- `OPEN_NCR -> RELEASE_HOLD`
- `CAPA_APPLIED != CAPA_EFFECTIVENESS_VERIFIED`
- `PASSING_TESTS != GOVERNANCE_CONFORMANCE`

Status boundaries:

```text
EXTERNAL_POST_FREEZE_RESEARCH = YES
OLD_PROJECT_RESTORATION = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
