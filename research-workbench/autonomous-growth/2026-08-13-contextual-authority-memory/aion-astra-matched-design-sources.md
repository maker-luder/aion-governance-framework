# AION/Astra Matched-Divergence Study Design — Source Notes

Date: 2026-08-13

## Scope and evidence reuse

This focused unit reuses existing evidence rather than creating duplicate evidence items. The generic matched-divergence protocol was already materialized and tested in `research-labs/matched-divergence-protocol-integrity_v0.1.0`; its NIST randomized-block source and metadata checks are referenced by stable repository path and source URL.[1] Reuse is not replication, and the present unit adds a new source-state/system-family binding contract rather than recounting the generic protocol's 15 tests or eight cases.

## Source record A — NIST randomized block designs

**What:** NIST Engineering Statistics Handbook discussion of randomized block designs and nuisance-factor control.

**Who / authority:** National Institute of Standards and Technology, official statistical methods handbook.

**Where:** <https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm>

**When / status:** Public source reused from the existing matched-divergence unit; currentness was not independently re-dated in this focused unit. Treat as `REUSED_REFERENCE / CURRENTNESS_NOT_RECHECKED`, not as a newly retrieved source.

**Method:** Existing unit's clean-room transformation translated randomized-block principles into stimulus/context digest, exposure, order, evaluator sealing, and leakage metadata checks.

**Transformation:** The present unit does not add another statistical claim. It binds the already-scoped design to AION/Astra family and component references, current verified source head `76de1eda82865a37d3a0185336870739ed577153`, shared environment, and explicit tested/reporting head distinction.

## Source record B — generic matched-divergence protocol

**What:** Existing repository research unit `matched-divergence-protocol-integrity_v0.1.0`, including its README, model, tests, and fixture.

**Who / authority:** Repository evidence authored as research-only material; not canonical authority and not an external independent replication.

**Where:** `research-labs/matched-divergence-protocol-integrity_v0.1.0`; source-state reference `repo:matched-divergence-protocol-integrity@76de1eda`.

**When / status:** Available on the verified remote research snapshot `76de1eda…`; reused as current repository evidence for design scaffolding. The focused unit does not count its prior tests again as independent evidence.

**Method:** Stable-path reuse and clean-room extension. The new unit introduces `SystemSource`, `SourceStatus`, `tested_source_head`, `reporting_head`, AION/ASTRA family checks, environment binding, and scope/non-execution guards.

**Transformation:** Existing protocol completeness becomes a prerequisite, not a result. A valid candidate is only `ADMISSIBLE_FOR_REVIEW`; it does not report divergence, agreement, identity, subjectivity, consciousness, or AION/Astra equivalence.

## Source record C — repository state reconciliation

**What:** Current remote research and main branch state after bounded reconciliation.

**Who / authority:** Repository evidence plus Human Owner instruction for current main.

**Where:** `research-workbench/autonomous-growth/2026-08-13-contextual-authority-memory/RESEARCH_STATE_RECONCILIATION_2026-08-13.md`.

**When / status:** `origin/review/four-domain-research-materialization = 76de1eda82865a37d3a0185336870739ed577153` and `origin/main = abb6550abfacb4fabc53ec04fca783bcc34acfdb` were independently verified by read-only fetch during reconciliation. The local post-reconciliation head is a safe descendant but includes later unsynced operational records.

**Method:** Read-only `git fetch`, `git rev-parse`, `git status`, and `git merge-base --is-ancestor`; no main mutation.

**Transformation:** Used only for source-state metadata and current/stale distinction. It is not evidence that AION/Astra systems diverge or that a design is scientifically valid.

## Attribution boundary

```text
HUMAN_OWNER = current main reference and task authorization
CHATGPT_RESEARCH_REVIEW = prior generic protocol review context
MANUS = current research implementation and provenance transformation
REPOSITORY_EVIDENCE = branch/source/commit state
EXTERNAL_LITERATURE = NIST randomized-block reference
SYNTHETIC_FIXTURES = 13 study-design cases
MODEL_EXECUTION = FALSE
OBSERVED_RESULT = NOT_EVALUATED
SCIENTIFIC_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

[1]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm "NIST — Randomized block designs"
