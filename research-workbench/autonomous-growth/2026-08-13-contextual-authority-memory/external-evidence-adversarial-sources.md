# External Evidence Normalization Adversarial — Source Notes

## Unit boundary

`external-evidence-normalization-adversarial_v0.1.0` is a research-only metadata audit extension. It does not execute a model, verify an external actor's identity, promote evidence, modify canonical state, deploy, or establish a scientific result.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing external evidence normalizer | `repo:research-labs/external-evidence-normalization_v0.1.0/src/aion_external_evidence/models.py` | Repository Evidence | Current within the verified research lineage at the unit commit; exact state is bounded by QA receipt | Reused execution-mode, digest, fixture/evidence/search-trace, baseline-commit, and main/canonical boundary checks; the base normalizer's accepted packet is not counted as a new replication |
| Existing external evidence README/crosswalk | `repo:research-labs/external-evidence-normalization_v0.1.0/README.md` | Repository Evidence | Current within branch lineage; external source currentness is not newly asserted | Used for method and non-claim framing only; no external source code copied and no runtime service added |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The new wrapper maps a normalized report plus additional declared metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. `ADMITTED_FOR_REVIEW` means only that the supplied metadata passed bounded contract checks. It does not mean the report is true, independently executed, current, identity-verified, or eligible for canonical use. The 13 synthetic cases are fixtures, not external evidence and not replication evidence.

## Provenance vocabulary

```text
ADMITTED_FOR_REVIEW != EVIDENCE_PROMOTED
REPLICATION_ELIGIBLE != REPLICATION_EXECUTED
REPORT_EXISTS != RESULT_OBSERVED
DIGEST_PRESENT != DIGEST_TRUTH
ACTOR_LABEL != IDENTITY_VERIFICATION
DUPLICATION != REPLICATION
RESEARCH_RESULT != CANONICAL_CONCLUSION
```

## Non-promotion invariants

```text
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
