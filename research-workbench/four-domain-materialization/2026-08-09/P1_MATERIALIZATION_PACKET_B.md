# Four-Domain P1 Materialization — Packet B

## Status

```text
PACKET_STATUS = IMPLEMENTED_RESEARCH_CANDIDATE
TARGET_BRANCH = review/four-domain-research-materialization
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
DEPLOYMENT_EFFECT = NONE
FORMAL_EXPERIMENT_RESULT = NONE
```

## 1. Purpose

Packet B materializes the first engineering-ready gaps identified in the existing four-domain workbench without altering existing application services or claiming production integration.

## 2. Materialized targets

| PRIOR GAP | NEW RESEARCH IMPLEMENTATION | CURRENT CAPABILITY | STILL NOT AUTHORIZED |
|---|---|---|---|
| Temporal/version resolution incomplete | `research-labs/four-domain-p1-materialization_v0.1.0/src/aion_four_domain_p1/temporal.py` | append-only version records; `as_was`; `current_as_of`; revision lineage; retrospective annotations | production current-state projection; persistent storage; runtime binding |
| Correction transition provenance incomplete | `.../correction.py` | evidence-bound transition ledger; conflict persistence; approval-before-supersession | production resolver authority; memory-store flag mutation; canonical correction |
| T0-T4 metrics only partially defined | `.../evaluation.py` | deterministic fixture metrics for retrieval, attribution, temporal resolution, correction recovery, abstention, provenance, unsupported inference and stale-memory influence | formal T0-T4 experiment; model runner; threshold claims; benchmark conformance |

## 3. New invariants made executable

1. A version cannot enter a historical `as_was` view before its own `recorded_at`, even when later evidence assigns an earlier `valid_from`.
2. Stream and case subject/namespace bindings do not silently change.
3. Retrospective interpretation remains a separate object from the historical record it interprets.
4. Every correction/conflict transition requires explicit actor, role, time and evidence references.
5. `SUPERSEDED` requires a prior `CORRECTION_APPROVED` transition for the same source/target pair.
6. A detected conflict remains unresolved until a separate explicit resolution transition exists.
7. Missing fixture ground truth yields an undefined metric (`None`) rather than a synthetic zero or pass.
8. Stale corrected records and unsupported answer claims are separately measurable.

## 4. Validation evidence

Local isolated validation before repository materialization:

```text
python -m pytest -q
12 passed
```

The validation is unit-level research validation only. It is not whole-system validation, independent IV&V, a formal benchmark run, or evidence of subjectivity/identity continuity.

## 5. Relationship to prior Codex work

The earlier Codex-authored repository workbench identified the missing temporal fields, incomplete correction transition provenance, absent end-to-end experiment runner, and missing metric definitions. Packet B implements bounded research candidates for those gaps while preserving the earlier stop boundaries around runtime integration, canonical writeback, MCP transport and Teacher binding.

## 6. Next research candidates enabled by Packet B

Packet B supplies reusable material for later research on:

- retrieval trace and deterministic context assembly manifests;
- provenance completeness validation across retrieval-to-output;
- temporal/conflict/correction synthetic fixture generators;
- T2/T3 condition orchestration;
- explicit importance/confidence calibration;
- stale-memory influence and correction-recovery ablations.

None of these follow-on candidates are promoted by this packet.

## 7. Attribution

- **Human Owner:** authorized the current implementation work on the isolated research branch.
- **Codex:** authored the prior repository fact extraction and gap maps used as engineering input.
- **ChatGPT:** designed, implemented and locally validated Packet B and the P1 research package.
