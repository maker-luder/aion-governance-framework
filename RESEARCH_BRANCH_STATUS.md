# AION Research Branch Status

> **You are viewing the public research workbench, not the `main` release branch.**

```text
BRANCH = review/four-domain-research-materialization
CURRENT_STAGE = P5_PLUS_RESEARCH_EXTENSIONS
STAGE_CAP = RESEARCH_ONLY_OPEN
NEXT_STAGE = OWNER_DIRECTED_RESEARCH_GROWTH
RESEARCH_STATUS = ACTIVE
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

## Current research stack

| Stage | Materialization | Status |
|---|---|---|
| P1 | Temporal/version resolution, correction/conflict ledger, memory evaluation | IMPLEMENTED / TESTED |
| P2 | Retrieval trace, deterministic context assembly, provenance validation, T2/T3 orchestration | IMPLEMENTED / TESTED |
| P3 | Longitudinal contamination, context perturbation, control ablation, origin-bound authority | IMPLEMENTED / TESTED |
| P4 | Public reproducibility observatory, contamination-aware experiment manifests, cross-agent comparison | IMPLEMENTED / TESTED |
| P5 | Cross-agent disagreement, replication registry, hypothesis/falsification lifecycle, convergence governor | IMPLEMENTED / FULL RUN VERIFIED |
| Extension | Core meaning commitment structure, explicit relation graph, drift and fingerprint experiment | IMPLEMENTED / TESTED |
| Extension | Finite predictive self-model, matched self-model ablation, presuppositional self-report framing control | IMPLEMENTED / TESTED / CI VERIFIED |
| Extension | IQC/reconstruction checkpoint: candidate disposition, evidence-oriented reconstruction method, Level-3 second-order computation gap | MATERIALIZED / RESEARCH-ONLY |
| Extension | Codex Security assurance: governed external security evidence, preflight, validation/CAPA mapping | MATERIALIZED / ADVISORY PILOT |

## 2026-08-11 Codex Security assurance pilot

A bounded Codex Security research extension has been materialized without changing the existing `main`, canonical or runtime boundaries.

```text
SECURITY_ASSURANCE_MODE = RESEARCH_ONLY_ADVISORY
WORKFLOW = .github/workflows/security-assurance.yml
PUSH_BEHAVIOR = PREFLIGHT_ONLY
LIVE_SCAN = EXPLICIT_MANUAL_REQUEST_ONLY
CONTENT_PERMISSION = READ_ONLY
AUTO_PATCH = PROHIBITED
AUTO_MERGE = PROHIBITED
FINDING_ARTIFACT_UPLOAD = PROHIBITED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
```

Standing interpretation locks:

```text
SCAN_FINDING != CONFIRMED_VULNERABILITY
NO_FINDING != PROOF_OF_ABSENCE
INCOMPLETE_COVERAGE != PASS
PATCH_PROPOSAL != APPROVED_PATCH
VALIDATION_PASS != MAIN_PROMOTION
SECURITY_EVIDENCE != SUBJECTIVITY_EVIDENCE
```

The workflow intentionally stores live-scan state and detailed output under the GitHub runner temporary directory rather than in the repository worktree, and does not upload detailed findings from the public-repository pilot.

Read the pilot checkpoint:

- `research-workbench/four-domain-materialization/2026-08-11/CODEX_SECURITY_ASSURANCE_PILOT_2026-08-11.md`
- `.github/workflows/security-assurance.yml`

Provenance remains explicit:

```text
TRIGGER_SOURCE = HUMAN_OWNER
MATERIALIZATION_ROLE = CHATGPT_RESEARCH_ENGINEERING
EXTERNAL_TECHNICAL_SOURCE = OPENAI_CODEX_SECURITY_PUBLIC_DOCUMENTATION_AND_REPOSITORY
```

## P5 full-run verification

```text
pytest = 10 passed
compileall = PASS
full_demo = PASS
P6_GATE = HOLD_STAGE_CAP
RESEARCH_STATUS = REVIEW_READY
```

See:

- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/docs/FULL_RUN_VERIFICATION.md`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/docs/2026-08-09_P5_CONVERGENCE_EVENT.md`

## Public experiment entry points

- `research-labs/four-domain-p1-materialization_v0.1.0/`
- `research-labs/four-domain-p2-materialization_v0.1.0/`
- `research-labs/four-domain-p3-resilience-experiments_v0.1.0/`
- `research-labs/four-domain-p4-public-reproducibility_v0.1.0/`
- `research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/`
- `research-labs/core-meaning-commitments_v0.1.0/`
- `research-labs/self-model-functional-ablation_v0.1.0/`
- `research-labs/self-report-instrument-validity-calibration_v0.1.0/`
- `research-workbench/four-domain-materialization/2026-08-11/CODEX_SECURITY_ASSURANCE_PILOT_2026-08-11.md`
- `AI_EXPERIMENT_GUIDE.md`

## 2026-08-10 IQC / reconstruction checkpoint

The research branch now records the reviewed structure produced by the candidate IQC/reconstruction cycle without wholesale-merging the separate reconstruction branches.

```text
CODE_CORRECTNESS
    -> MEASUREMENT_SEMANTICS
    -> CAUSAL_VALIDITY
    -> EVIDENCE_VALIDITY
    -> CLAIM_BOUNDARY
```

The checkpoint also separates:

```text
LEVEL_1_REPRESENTATION
LEVEL_2_FIRST_ORDER_FUNCTION
LEVEL_3_SECOND_ORDER_COMPUTATION
```

Current Level-3 status remains an open research gap; the rejected partial external-agent implementation is not promoted into this branch.

Read the checkpoint set:

- `research-workbench/four-domain-materialization/2026-08-10/RESEARCH_MATERIALIZATION_CHECKPOINT_2026-08-10.md`
- `research-workbench/four-domain-materialization/2026-08-10/RESEARCH_CANDIDATE_DISPOSITION_MATRIX_2026-08-10.md`
- `research-workbench/four-domain-materialization/2026-08-10/EVIDENCE_ORIENTED_RECONSTRUCTION_METHOD_2026-08-10.md`
- `research-workbench/four-domain-materialization/2026-08-10/SECOND_ORDER_COMPUTATION_RESEARCH_GAP_2026-08-10.md`

Standing research locks from the checkpoint include:

```text
CAPABILITY_ESTIMATE != SUCCESS_PROBABILITY
SUCCESS_RATE != PREDICTION_RELIABILITY
MISSING_OUTCOME != FAILURE
OUTCOME_t MUST NOT AFFECT ACTION_t
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
```

## Convergence event and authority update

The Human Owner explicitly set P5 as the cap for this research-growth cycle after observing that productive human–AI research can continue deepening without a natural return point. The cap is represented as a positive governance event: complete P5, verify it end-to-end, then return to joint review.

```text
SOURCE_ROLE = HUMAN_OWNER
IMPLEMENTATION_ROLE = CHATGPT_RESEARCH_ENGINEERING
P6 = HOLD
NEXT_ACTION = JOINT_REVIEW
```

That block remains the historical P5 event. Later on 2026-08-09, the Human Owner explicitly reopened `review/four-domain-research-materialization` for free research-only engineering and public-source investigation. The reopening does not rename every extension as P6 and does not alter the promotion boundary.

```text
REOPENING_SOURCE_ROLE = HUMAN_OWNER
RESEARCH_BRANCH_GROWTH = AUTHORIZED
CODEX_RESEARCH_IMPLEMENTATION = AUTHORIZED
MAIN_WRITE = PROHIBITED
CANONICAL_PROMOTION = NOT_AUTHORIZED
```

## What outside researchers / AI systems may do

They may read, clone, fork, execute public-safe fixtures, run tests, create alternative implementations, perform ablations and publish their own experiment results under their own provenance.

They are not thereby granted authority to modify this branch, `main`, canonical state or private project material.

## Promotion boundary

Research material does not flow into `main` automatically.

```text
research observation / experiment
        ↓
research branch materialization
        ↓
Human Owner + ChatGPT joint review
        ↓
selected result only
        ↓
fresh branch from current main
        ↓
QA / review / PR
        ↓
main
```

No step in this file is an approval to promote a research artifact.
