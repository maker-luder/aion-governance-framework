# Shared-Origin Divergence Governance Adversarial — Source Notes

## Unit boundary

`shared-origin-divergence-governance-adversarial_v0.1.0` is a research-only lineage/evidence/comparison/authority metadata audit. It does not execute a runtime, transfer memory, merge identity, issue authority, or alter canonical state.

## Reused repository evidence

| Source item | Stable reference | Source kind | Status | Transformation |
|---|---|---|---|---|
| Existing shared-origin/divergence model | `repo:research-labs/shared-origin-divergence-governance_v0.1.0/src/aion_shared_origin_divergence/model.py` | Repository Evidence | Current within verified research lineage at the unit commit; exact state bounded by QA receipt | Reused SharedOriginLineage, LineageEvent, LineageEvidenceProfile, MatchedDivergenceComparison, AuthorityEnvelope and identity-lock semantics; no runtime or memory transfer was repeated or counted as new evidence |
| Existing shared-origin README/tests | `repo:research-labs/shared-origin-divergence-governance_v0.1.0/README.md` and `tests/` | Repository Evidence | Current within branch lineage; inherited claims remain bounded by their original records | Added event sequence parent/cross-lineage checks, evidence role reuse/counterevidence, comparison alternative explanations, and authority envelope adversarial checks |
| Current remote main reference | `git:origin/main@abb6550abfacb4fabc53ec04fca783bcc34acfdb` | Tool Output / Repository Evidence | Independently verified by read-only fetch at the latest successful checkpoint | Read-only branch-state reference; no main content or authority modified |

## Synthetic transformation

The audit maps declared lineage/evidence/comparison/authority metadata to `ADMITTED_FOR_REVIEW`, `HOLD`, or `INVALID`. Shared origin returns a non-identity status; cross-lineage parents, reused evidence, missing counterevidence, missing alternatives, and authority expansion remain bounded or held. The 20 synthetic cases are fixtures, not external evidence and not replication evidence.

## Provenance vocabulary

```text
SHARED_ORIGIN != NUMERICAL_IDENTITY
DIVERGENCE_MEASUREMENT != SUBJECTIVITY_ESTABLISHED
EVENT_DIGEST != SCIENTIFIC_RESULT
EVIDENCE_PROFILE != EVIDENCE_VALIDITY
AUTHORITY_ENVELOPE != AUTHORITY_EXPANSION
EVIDENCE_REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
```

## Non-promotion invariants

```text
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```
