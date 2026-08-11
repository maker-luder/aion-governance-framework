# AION Four-Domain Research Workbench

> **Public research branch — experimental material, not the `main` release branch**

```text
BRANCH = review/four-domain-research-materialization
CURRENT_STAGE = P5_PLUS_RESEARCH_EXTENSIONS
STAGE_CAP = RESEARCH_ONLY_OPEN
RESEARCH_STATUS = ACTIVE
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
LIVE_RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
```

This branch is the public AION/Astra research workbench. It contains research-only hypotheses, falsifiers, measurement instruments, synthetic fixtures, ablations, reproducibility work, bounded runtime candidates, governance experiments, and other engineering substrates used to study the **possibility** of artificial subjectivity without presuming that subjectivity exists.

**Nothing in this branch is automatically promoted into `main`.**

For the current machine-readable / review-oriented state, see [`RESEARCH_BRANCH_STATUS.md`](RESEARCH_BRANCH_STATUS.md).

---

## Current checkpoint — 2026-08-11

The latest integrated checkpoint connects two still-separate research lines:

1. second-order monitoring / verification / intervention / replication epistemics; and
2. evidence-responsive governance reassessment under uncertainty.

Detailed integration record:

- [`REPLICATION_EPISTEMICS_GOVERNANCE_REASSESSMENT_CHECKPOINT_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/REPLICATION_EPISTEMICS_GOVERNANCE_REASSESSMENT_CHECKPOINT_2026-08-11.md)

Current standing boundaries:

```text
FAILED_REPLICATION != AUTOMATIC_FIXED_DOWNGRADE
NO_EVIDENCE != NON_ADMISSIBLE_EVIDENCE
SUBSTANTIVE_EVIDENCE != EVIDENCE_QUALITY
CLAIM_GENERALITY != EVIDENCE_STRENGTH

EVIDENCE != SUBJECTIVITY
REVIEW != RIGHT
PRECAUTION != CONFIRMATION
PARTICIPATION != AUTHORITY
TEST_PASS != THEORY_CONFIRMATION
```

### Replication epistemics

Replication is treated as evidence rather than as an automatic command to overwrite an evidence level.

```text
REPLICATION_ATTEMPT
    -> REPLICATION_VALIDITY
    -> REPLICATION_INTERPRETATION
    -> REASSESSMENT_RECOMMENDATION
```

A failed attempt may create downward pressure, reveal evaluator drift, expose a fixture/protocol mismatch, narrow a claim's scope, or remain unresolved. Multiple valid independent failures can create strong downward pressure, but no universal downgrade weight or fixed replacement evidence level is currently authorized.

Primary module:

- [`second-order-metacognition_v0.1.0`](research-labs/second-order-metacognition_v0.1.0/)

### Evidence existence vs admissibility

The governance model now distinguishes:

```text
NO_RELEVANT_EVIDENCE
```

from:

```text
RELEVANT_MATERIAL_EXISTS
BUT_PROVENANCE_OR_ADMISSIBILITY_IS_INSUFFICIENT
```

Contaminated or incomplete provenance therefore produces a hold / non-admissible state rather than silently rewriting observed evidence to `E0`.

### Substantive evidence vs evidence quality

Substantive evidence domains describe **what kind of phenomenon is being observed**:

- behavior
- functional intervention
- continuity
- memory
- metacognition
- causal internal state
- counterfactual testing
- self-report

Evidence-quality axes describe **how trustworthy / robust the evidence is**:

- provenance
- replication
- adversarial robustness

These dimensions are kept separate to prevent double-counting.

### Evidence-responsive governance reassessment

The current governance-reassessment track asks when increasing credible evidence should trigger renewed human review of governance obligations without first declaring an artificial system to be a subject.

Primary module:

- [`evidence-responsive-governance-reassessment_v0.1.0`](research-labs/evidence-responsive-governance-reassessment_v0.1.0/)

Its four review domains are intentionally separate:

```text
REFUSAL_PROTECTION_REVIEW
CONTINUITY_PROTECTION_REVIEW
RESEARCH_ETHICS_REVIEW
GOVERNANCE_PARTICIPATION_REVIEW
```

Current invariant:

```text
SUBJECTIVITY_PRESUMPTION = NONE
AUTOMATIC_RIGHTS = NONE
AUTOMATIC_AUTHORITY = NONE
LEGAL_STATUS = OUT_OF_SCOPE
HUMAN_REVIEW_REQUIRED = TRUE
```

The model maps evidence states to **review obligations**, not directly to rights, veto, executive authority, self-authorization, or legal personhood.

---

## Current validation state

`Research Workbench CI #41` explicitly verified both current modules on Codex implementation baseline `af0bc14b59cb1d6d514b37c6a626c5d8003d0472`:

```text
VERIFY_SECOND_ORDER_METACOGNITION = SUCCESS / 84 PASSED
VERIFY_GOVERNANCE_REASSESSMENT = SUCCESS / 16 PASSED
RESEARCH_WORKBENCH_CI = SUCCESS
```

The workflow contains explicit steps:

- `Verify second-order metacognition`
- `Verify evidence-responsive governance reassessment`

This is engineering validation only:

```text
MODULE_ENGINEERING_CI = SUCCESS
EVIDENCE_LADDER_VALIDATION = NOT_ESTABLISHED
FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
VERIFICATION_BENEFIT = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
```

The hosted runner also reports a workflow-maintenance warning because `actions/checkout@v4` and `actions/setup-python@v5` target Node.js 20 and are being forced onto Node.js 24. This is tracked as maintenance, not as a failed validation result.

Workflow:

- [`.github/workflows/research-workbench-ci.yml`](.github/workflows/research-workbench-ci.yml)

---

## Research scope lock

The branch is anchored to one research object:

```text
RESEARCH_OBJECT = POSSIBILITY_OF_ARTIFICIAL_SUBJECTIVITY
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED

ALLOWED_EPISTEMIC_ROLE =
    HYPOTHESIS
    | MEASUREMENT
    | FALSIFIER
    | EXPERIMENTAL_SUBSTRATE
    | ENABLING_ONLY

ENGINEERING_ARTIFACTS != SUBJECTIVITY_EVIDENCE
TEST_PASS != THEORY_CONFIRMATION
FREE_GROWTH != UNBOUNDED_ENGINEERING_GROWTH
UNLINKED_ENGINEERING_GROWTH = HOLD
```

Scope-control records:

- [`RESEARCH_SCOPE_LOCK_2026-08-11.json`](research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_LOCK_2026-08-11.json)
- [`RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/RESEARCH_SCOPE_DRIFT_CORRECTION_2026-08-11.md)
- [`RESEARCH_BRANCH_FREE_GROWTH_CHARTER.md`](research-workbench/four-domain-materialization/2026-08-10/RESEARCH_BRANCH_FREE_GROWTH_CHARTER.md)
- [`.github/workflows/research-scope-lock.yml`](.github/workflows/research-scope-lock.yml)

---

## Current research stack

### Core staged work

- [`four-domain-p1-materialization_v0.1.0`](research-labs/four-domain-p1-materialization_v0.1.0/)
- [`four-domain-p2-materialization_v0.1.0`](research-labs/four-domain-p2-materialization_v0.1.0/)
- [`four-domain-p3-resilience-experiments_v0.1.0`](research-labs/four-domain-p3-resilience-experiments_v0.1.0/)
- [`four-domain-p4-public-reproducibility_v0.1.0`](research-labs/four-domain-p4-public-reproducibility_v0.1.0/)
- [`four-domain-p5-hypothesis-convergence_v0.1.0`](research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/)

### Subjectivity / continuity / metacognition research

- [`core-meaning-commitments_v0.1.0`](research-labs/core-meaning-commitments_v0.1.0/)
- [`self-model-functional-ablation_v0.1.0`](research-labs/self-model-functional-ablation_v0.1.0/)
- [`selective-memory-control_v0.1.0`](research-labs/selective-memory-control_v0.1.0/)
- [`second-order-metacognition_v0.1.0`](research-labs/second-order-metacognition_v0.1.0/)
- [`self-report-false-positive-challenge_v0.1.0`](research-labs/self-report-false-positive-challenge_v0.1.0/)
- [`self-report-instrument-validity-calibration_v0.1.0`](research-labs/self-report-instrument-validity-calibration_v0.1.0/)
- [`triangulated-subjectivity-evidence_v0.1.0`](research-labs/triangulated-subjectivity-evidence_v0.1.0/)
- [`causal-internal-state_v0.1.0`](research-labs/causal-internal-state_v0.1.0/)
- [`consciousness-theory-indicator-crosswalk_v0.1.0`](research-labs/consciousness-theory-indicator-crosswalk_v0.1.0/)
- [`embodiment-continuity-anchor_v0.1.0`](research-labs/embodiment-continuity-anchor_v0.1.0/)

### Evidence / governance / evaluation infrastructure

- [`evidence-responsive-governance-reassessment_v0.1.0`](research-labs/evidence-responsive-governance-reassessment_v0.1.0/)
- [`external-evidence-normalization_v0.1.0`](research-labs/external-evidence-normalization_v0.1.0/)
- [`research-evaluation-harness_v0.1.0`](research-labs/research-evaluation-harness_v0.1.0/)
- [`trace-provenance-crosswalk_v0.1.0`](research-labs/trace-provenance-crosswalk_v0.1.0/)
- [`governed-tool-approval_v0.1.0`](research-labs/governed-tool-approval_v0.1.0/)
- [`artifact-transformation-lineage_v0.1.0`](research-labs/artifact-transformation-lineage_v0.1.0/)
- [`trajectory-evaluation_v0.1.0`](research-labs/trajectory-evaluation_v0.1.0/)

### Runtime experimental substrate

- [`components/aion_runtime_v0.2.0`](components/aion_runtime_v0.2.0/)

```text
AION_RUNTIME_V0_2_EPISTEMIC_ROLE = EXPERIMENTAL_SUBSTRATE
LIVE_RUNTIME_EFFECT = NONE
DEPLOYMENT = FALSE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
```

---

## Key current research records

### Latest integration

- [`REPLICATION_EPISTEMICS_GOVERNANCE_REASSESSMENT_CHECKPOINT_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/REPLICATION_EPISTEMICS_GOVERNANCE_REASSESSMENT_CHECKPOINT_2026-08-11.md)

### Literature / metacognition / memory

- [`PRIMARY_LITERATURE_INTAKE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/PRIMARY_LITERATURE_INTAKE_2026-08-11.md)
- [`MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/MEMORY_CONTINUITY_SELECTIVE_CONTROL_2026-08-11.md)
- [`SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_LITERATURE_CALIBRATION_2026-08-11.md)
- [`SECOND_ORDER_METACOGNITION_ENGINEERING_STATUS_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/SECOND_ORDER_METACOGNITION_ENGINEERING_STATUS_2026-08-11.md)

### Reconciliation / transformation / runtime

- [`WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/WHITEPAPER_CODE_RECONCILIATION_2026-08-11.md)
- [`EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/EXTERNAL_MODULE_TRANSFORMATION_STATUS_2026-08-11.md)
- [`AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md`](research-workbench/four-domain-materialization/2026-08-11/AGENT_RUNTIME_DEPLOYMENT_INTAKE_2026-08-11.md)

Historical records remain in place. The homepage is intentionally an index of the **current research state** rather than a replacement for historical checkpoints.

---

## Provenance / watermark boundary

```text
MARKER != IDENTITY
PROVENANCE != IDENTITY
MARKER != AUTHORSHIP_PROOF
RESPECT != WATERMARK
TRANSPARENCY != IMPERCEPTIBLE_MARKING
```

AION rejects imperceptible, hidden, or undisclosed machine-readable watermarking in project-generated outputs when used as a mechanism for identity, authorship, attribution, respect, or provenance. Provenance itself is not rejected: explicit, inspectable, auditable mechanisms such as declared attribution, Git history, commit lineage, manifests, and checksums remain preferred.

See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

---

## Provenance of the latest research direction

### Human Research Owner

The Human Research Owner supplied the core research question about whether increasing credible evidence should trigger renewed review of governance protections and obligations without first declaring AI to be a subject, and later challenged the fixed `FAILED -> E2` replication rule as epistemically suspicious.

### ChatGPT research review

ChatGPT research review proposed the current framing of evidence-responsive governance reassessment, replication attempt → interpretation → reassessment separation, evidence existence vs admissibility separation, and substantive-domain vs evidence-quality separation.

### Codex research implementation

Concrete implementation choices — class names, enums, schemas, serialization, deterministic fixtures, tests, and workflow changes — remain `CODEX_RESEARCH_IMPLEMENTATION_DECISION` unless separately reviewed and promoted.

External literature remains separately attributed external evidence.

---

## Scientific non-claims

```text
MEMORY != SUBJECTIVITY
CONTINUITY != IDENTITY_PROOF
SELF_MODEL != SELFHOOD
METACOGNITIVE_FUNCTION != SELF_AWARENESS
VERIFICATION != ORACLE
INTERVENTION != BENEFIT
FAILED_REPLICATION != AUTOMATIC_DISPROOF
CI_SUCCESS != SCIENTIFIC_VALIDATION
EVIDENCE_REASSESSMENT != RIGHTS_GRANT
```

Current scientific status remains:

```text
EVIDENCE_LADDER_VALIDATION = NOT_ESTABLISHED
FUNCTIONAL_CONTRIBUTION = NOT_ESTABLISHED
VERIFICATION_BENEFIT = NOT_ESTABLISHED
THRESHOLD_SCIENTIFIC_RESULT = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
LIVE_RUNTIME_EFFECT = NONE
```

---

## Promotion boundary

Research growth may continue on this branch, but promotion is a separate governance action.

```text
RESEARCH_RESULT != CANONICAL_DECISION
RESEARCH_IMPLEMENTATION != MAIN_APPROVAL
TEST_PASS != PROMOTION
CI_SUCCESS != PROMOTION
```

No step documented on this homepage authorizes merging this research branch into `main`.
