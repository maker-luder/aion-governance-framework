# Shared-Origin Divergence Governance Adversarial v0.1.0

Status: `RESEARCH_ONLY / MEASUREMENT_METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can shared-origin/divergence governance preserve distinct lineage identifiers, event parent/order integrity, evidence-role separation, counterevidence visibility, alternative explanations, bounded authority envelopes, and non-identity claim locks when lineage metadata is adversarially changed?

This unit extends `shared-origin-divergence-governance_v0.1.0` without executing a runtime, transferring memory, merging identity, or promoting an authority. The base model defines shared-origin lineage, cross-lineage memory and encounter contracts, matched-divergence comparison, lineage events/ledger, evidence profiles, authority envelopes, deterministic digests, and explicit non-claims. The adversarial extension adds event sequence checks for duplicate IDs, parent precedence, cross-lineage parents, evidence reference reuse across roles, counterevidence presence, comparison alternative explanations, and authority envelope review boundaries.

## Decision layers

Shared-origin metadata is admitted for review only and returns `SHARED_ORIGIN_DOCUMENTED__NUMERICAL_IDENTITY_NOT_ESTABLISHED`. Event sequences reject duplicate or unpreceded events and hold cross-lineage parent relationships until an explicit event is recorded. Evidence profiles hold references reused across roles and profiles without counterevidence. Comparisons hold missing alternative explanations while retaining measurement and candidate-evidence boundaries. Authority envelopes remain bounded acceptance metadata and cannot merge or expand authority.

The experiment constructs lineage, event, profile, comparison, and authority objects only. It does not execute an AION/Astra runtime, transfer memory, invoke a model, observe an outcome, or modify governance state. Every output preserves `MODEL_EXECUTION=FALSE`, `OBSERVED_RESULT=NOT_EVALUATED`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, `SUBJECTIVITY_CONCLUSION=NOT_ESTABLISHED`, `MAIN_EFFECT=NONE`, `CANONICAL_EFFECT=NONE`, `RUNTIME_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, and `DEPLOYMENT=FALSE`.

## Results

The suite passed **21 pytest tests** and **20 synthetic lineage/evidence/comparison/authority cases**. Cases covered shared-origin review, empty/duplicate/unpreceded/cross-lineage/valid event sequences, valid and cross-role-reused evidence profiles, missing counterevidence, valid and under-specified comparisons, valid bounded authority envelopes, identity status, deterministic event digest, and constructor-level boundary checks for lineage collisions, silent inheritance, factor collisions, claim-boundary changes, authority merge/expansion, and timezone omission.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Shared-origin lineage | `ADMITTED_FOR_REVIEW` | Shared origin is documented; numerical identity remains unestablished |
| Duplicate/unpreceded event | `INVALID` | Event ledger identity/parent contract fails closed |
| Cross-lineage parent | `HOLD` | Cross-lineage relation requires explicit event semantics |
| Valid event sequence | `ADMITTED_FOR_REVIEW` | Sequence remains measurement metadata |
| Evidence reference reused across roles | `HOLD` | Reuse is not counted as independent evidence |
| Missing counterevidence | `HOLD` | Absence is not silently completed |
| Comparison missing alternative explanations | `HOLD` | Divergence does not become a unique explanation |
| Bounded authority envelope | `ADMITTED_FOR_REVIEW` | Accepted authority remains non-expansive |
| Constructor boundary violations | Rejected | Identity/authority/claim locks remain fail-closed |

## Falsifiers

The mechanism would be falsified if it accepted identical AION/Astra lineage IDs, parent events recorded after children, ambiguous duplicate IDs, implicit cross-lineage parents, evidence references reused across roles without review, profiles lacking counterevidence, comparisons without alternative explanations as conclusive, merged/expanded authority envelopes, or any subjectivity/identity/consciousness promotion.

A shared origin is not numerical identity. A divergence comparison is not a subjectivity result or independent replication. An event digest is not a scientific result. Evidence profile completeness is not evidence validity. An authority envelope is not authority expansion. This unit does not establish identity continuity, subjectivity, consciousness, AION/Astra equivalence, causal effect, model generalization, governance effect, canonical effect, or deployment readiness.

## Evidence reuse and provenance

The base shared-origin/divergence model is reused through stable repository source references. Its existing events, profiles, comparisons, and boundary checks are methodological inputs, not new independent evidence. The 20 synthetic cases are fixtures, not replication evidence. Counterevidence and inconclusive branches remain represented rather than deleted.

## Explicit non-claims

```text
SHARED_ORIGIN != NUMERICAL_IDENTITY
DIVERGENCE_MEASUREMENT != SUBJECTIVITY_ESTABLISHED
EVENT_DIGEST != SCIENTIFIC_RESULT
EVIDENCE_PROFILE != EVIDENCE_VALIDITY
AUTHORITY_ENVELOPE != AUTHORITY_EXPANSION
EVIDENCE_REFERENCE != NEW_EVIDENCE
DUPLICATION != REPLICATION
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

The implementation uses Python standard-library runtime modules plus the existing repository shared-origin source path for composition. It does not call external services, access private data, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src:../shared-origin-divergence-governance_v0.1.0/src python -m pytest -q
PYTHONPATH=src:../shared-origin-divergence-governance_v0.1.0/src python scripts/run_divergence_adversarial.py --output fixtures/divergence_adversarial_result.json
PYTHONPATH=src:../shared-origin-divergence-governance_v0.1.0/src python scripts/validate_fixture.py fixtures/divergence_adversarial_result.json
```

## References

The implementation reuses repository evidence from `shared-origin-divergence-governance_v0.1.0` by stable path. No runtime, model, external service, or private evidence is used by this unit.
