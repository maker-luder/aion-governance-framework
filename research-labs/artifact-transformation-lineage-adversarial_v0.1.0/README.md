# Artifact Transformation Lineage Adversarial v0.1.0

Status: `RESEARCH_ONLY / METADATA_ONLY / MODEL_EXECUTION=FALSE / CANONICAL_EFFECT=NONE`

## Research question

Can a transformation-lineage audit preserve the distinction between a declared transformation record and a verified output artifact when event order, run identity, job identity, provenance references, artifact paths, digests, environment secrets, parent lineage, and boundary-effect fields are adversarially changed?

This unit extends `artifact-transformation-lineage_v0.1.0` rather than replacing it. The prior module provides artifact references, SHA-256 verification, design-time transformation plans, start/complete/fail events, secret-like environment redaction, and a record-only ledger. The adversarial extension adds a separate audit projection that validates a complete event sequence and returns review/hold/invalid metadata without executing a command or promoting an artifact.

## Decision layers

The audit first checks the expected run scope, event uniqueness, contiguous sequence indexes, redacted environment metadata, and start/terminal cardinality. It then checks job identity, source and approval references, artifact path/provenance completeness, self-parent lineage, and terminal semantics. A complete run without supplied output bytes is held; a path-set mismatch is invalid; a digest mismatch is held; a failed run is recorded as a valid failure trace without promotion; and a verified complete output is `VALID` metadata only.

All audit decisions preserve `CANONICAL_EFFECT=NONE`, `GOVERNANCE_EFFECT=NONE`, `DEPLOYMENT=FALSE`, `SCIENTIFIC_CONCLUSION=NOT_ESTABLISHED`, and `OBSERVED_RESULT=NOT_EVALUATED`.

## Results

The corrected suite passed **20 pytest tests** and **15 synthetic cases**. One initial state-order test used a duplicate event identifier and therefore exercised the earlier duplicate-ID guard. That fixture-construction defect is preserved in `artifact-lineage-adversarial-initial-failure.md`; the corrected case uses unique IDs and contiguous indexes and returns `RUN_STATE_ORDER_INVALID`.

| Case family | Decision | Mechanism meaning |
|---|---|---|
| Complete run with matching output digest | `VALID` | Declared metadata and supplied bytes match; no promotion follows |
| Failed run | `VALID / FAILED_RUN_RECORDED` | Failure trace retained without products or promotion |
| Empty or scope-mismatched lineage | `HOLD` / `INVALID` | Audit cannot interpret an unscoped sequence |
| Duplicate IDs or non-contiguous indexes | `INVALID` | Event identity/order contract fails closed |
| State order, job, or self-parent drift | `INVALID` | Temporal/job/lineage contract fails closed |
| Unredacted secret-like environment | `INVALID` | Sensitive metadata must remain redacted |
| Provenance or artifact-source gaps | `HOLD` | Missing attribution cannot be silently completed |
| Output path mismatch | `INVALID` | Declared product set differs from supplied output set |
| Output digest mismatch | `HOLD` | Bytes do not establish the declared artifact digest |

## Falsifiers

The mechanism would be falsified if it accepted duplicate event identifiers or non-contiguous indexes, treated a terminal event as valid without a prior start, accepted job or provenance drift without a hold/invalid decision, allowed an unredacted secret-like field, accepted a self-parent relation, silently filled missing artifact provenance, treated a mismatched digest as verified, or emitted a canonical, governance, or deployment effect.

A matching SHA-256 digest is only a byte-level integrity check. It is not proof that a transformation was scientifically valid, that a source was authoritative, that a method was appropriate, that an output should be published, or that a real system produced the bytes.

## Evidence reuse and provenance

The prior artifact-lineage module is reused by stable repository reference. Existing digest and redaction concepts are method inputs, not new evidence. This extension does not count repeated fixtures as independent replication and does not make the repository artifact a release or canonical artifact.

The initial duplicate-ID observation is retained as a mechanism/test-contract failure, not silently deleted and not interpreted as a scientific result.

## Explicit non-claims

```text
DIGEST_MATCH != SCIENTIFIC_VALIDITY
LINEAGE_VALID != REPLICATION
FAILED_RUN_RECORDED != FAILURE_CAUSE_ESTABLISHED
REVIEW_METADATA != GOVERNANCE_DECISION
ARTIFACT_OUTPUT != CANONICAL_ARTIFACT
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
GOVERNANCE_EFFECT = NONE
DEPLOYMENT = FALSE
```

The implementation uses only Python standard-library runtime modules. It does not execute shell commands, call private services, inspect private data, modify `main`, write canonical state, or deploy.

## Reproduction

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_artifact_lineage_adversarial.py --output fixtures/artifact_lineage_adversarial_result.json
```

## References

The implementation reuses repository evidence from `artifact-transformation-lineage_v0.1.0` by stable path and provenance reference. The existing module's external source crosswalk remains methodological context; no external source code or runtime dependency is imported by this unit.
