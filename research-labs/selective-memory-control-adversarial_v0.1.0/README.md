# Selective Memory Control Adversarial v0.1.0

Status: `RESEARCH_ONLY / REVIEW_METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a selective-memory control layer preserve source and approval references, revision lineage, status/namespace/domain/purpose isolation, timestamp validity, retrieval trace integrity, and non-identity boundaries when memory records and retrieval traces are adversarially changed?

This unit extends `selective-memory-control_v0.1.0` without invoking an embedding model, making an autonomous memory decision, or treating recall as identity evidence. The base store provides explicit add/revise/discard/retrieve operations, immutable revision lineage, status gating, namespace/domain/purpose filtering, deterministic relevance scoring, and auditable retrieval traces. The adversarial extension audits required record fields, timezone-bearing timestamps, revision parent/number/scope integrity, non-active status, active source-reference reuse, memory lineage lookup, retrieval scope, considered/blocked ID disjointness, returned-record status, hit membership, hit scope, score/term bounds, deterministic hit order, and missing hit records.

## Decision layers

A memory record is review metadata only after required fields, timestamp, revision, and status checks. Initial records cannot supersede another record; revisions require a parent and preserve namespace/domain/purpose scope. Missing parents, scope drift, and revision-number drift are invalid. Superseded and discarded records remain retained for audit but are not context eligible. Duplicate active source references are held because reference reuse is not new independent evidence.

Retrieval traces require all scope dimensions. Considered and blocked IDs must be unique and disjoint. A hit must refer to an audited active record, belong to the considered set, match the trace scope, contain bounded score and matched terms, and follow deterministic ordering. These are mechanism checks only; they do not certify memory truth or relevance beyond the fixture contract.

The experiment constructs synthetic `MemoryRecord`, `RetrievalTrace`, and `RetrievalHit` objects and calls only the deterministic research-layer audit. It does not invoke a model, embedding service, external memory backend, or deployment. Every output preserves `REVIEW_METADATA_ONLY`, `MEMORY_TRUTH=NOT_ESTABLISHED`, `IDENTITY_CONTINUITY=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`.

## Results

The suite passed **30 pytest tests** and **29 synthetic memory/retrieval cases**. Cases covered valid/missing/timezone-invalid records, invalid revision zero, initial supersedes, missing revision parent, non-active status, empty/duplicate stores, parent-not-found, revision scope and number drift, active source-reference reuse, discarded retention, valid revision chain and lineage, valid retrieval, missing retrieval scope, duplicate considered/blocked IDs, considered-blocked overlap, non-active hit, hit membership/scope/score/terms/order, and missing hit record.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Valid record/store/lineage/retrieval | `ADMITTED_FOR_REVIEW` | Memory mechanics remain review metadata only |
| Missing fields/timezone/revision | `INVALID` | Admission fails closed |
| Superseded/discarded status | `HOLD` | Retained for audit; not context eligible |
| Revision parent/scope/number drift | `INVALID` | Immutable revision lineage is protected |
| Active source reference reuse | `HOLD` | Reuse is not new evidence |
| Retrieval scope/ID overlap | `INVALID` | Namespace/domain/purpose trace is unambiguous |
| Non-active or out-of-scope hit | `INVALID` | Context eligibility is not bypassed |
| Invalid score/terms/order/missing hit | `INVALID` | Retrieval trace integrity fails closed |

## Falsifiers and retained correction

The mechanism would be falsified if it accepted missing source/approval metadata, timezone-free creation timestamps, invalid revision parents or scope drift, silently treated superseded/discarded records as current context, counted repeated source references as new evidence, allowed considered/blocked overlap, returned non-active or out-of-scope records, accepted unbounded scores, or failed to preserve deterministic hit order.

The first fixture validator run had one expected-reason marker mismatch for the discarded-memory case: the implementation correctly returned `DISCARDED_MEMORY_RETAINED_OUTSIDE_CONTEXT`, while the validator initially expected the more general non-active reason. The validator was corrected, and the full 30-test/29-case validation was rerun successfully. This construction correction is retained in the command history and is not treated as a scientific result.

Memory recall is not memory truth, retrieval is not relevance proof, stored is not current-context eligible, old memory is not current memory, revision history is not simultaneous truth, source reference is not approval authority, and memory utility is not identity continuity or subjectivity. This unit does not establish memory truth, source reliability, relevance validity, identity continuity, subjectivity, consciousness, model generalization, causal effect, independent replication, governance effect, canonical effect, or deployment readiness.

## Evidence reuse and provenance

The base selective-memory store is reused through a stable repository source reference. Its prior tests, public methodological stimuli, and existing records are not counted as new independent evidence. The 29 synthetic cases are fixtures, not replication evidence. Discarded, superseded, out-of-scope, invalid, and held branches remain represented rather than deleted.

## Explicit non-claims

```text
STORED != CURRENT_CONTEXT_ELIGIBLE
RETRIEVABLE != RELEVANT
OLD_MEMORY != CURRENT_MEMORY
REVISION_HISTORY != SIMULTANEOUS_TRUTH
SOURCE_REF != APPROVAL_AUTHORITY
MEMORY_RECALL != IDENTITY_CONTINUITY
MEMORY_MODULE_UTILITY != SUBJECTIVITY
EVIDENCE_REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
MEMORY_TRUTH = NOT_ESTABLISHED
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses Python standard-library runtime modules plus the existing repository selective-memory source path for composition. It does not access private data, call external services, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../selective-memory-control_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../selective-memory-control_v0.1.0/src python scripts/run_memory_adversarial.py --output fixtures/memory_adversarial_result.json
PYTHONPATH=src:../selective-memory-control_v0.1.0/src python scripts/validate_fixture.py fixtures/memory_adversarial_result.json
```

## References

The implementation reuses repository evidence from `selective-memory-control_v0.1.0` by stable path. Public memory projects listed in the base lab remain methodological context only; no external source code or external memory result is used by this unit.
