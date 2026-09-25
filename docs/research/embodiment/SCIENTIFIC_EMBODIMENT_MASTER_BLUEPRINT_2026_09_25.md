# Scientific Embodiment Master Blueprint — 2026-09-25

Status: `ARCHITECTURAL MASTER BLUEPRINT / DRAFT`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Direct runtime change: `NO`  
Merge-to-main authorization: `NO`  
Core research question: `AI_SUBJECTIVITY_POSSIBILITY`

## 1. Purpose

This blueprint defines a staged, evidence-bound architecture for embodiment research without changing the repository's scientific core.

Embodiment is treated as an experimental variable and test bed for studying functional effects on self-modeling, continuity-related behavior, adaptation, state-dependent decision making, body prediction, error correction, and interaction-history-mediated regulation.

It is not a replacement research program for the repository.

```text
EMBODIMENT = EXPERIMENTAL_VARIABLE
EMBODIMENT != NEW_RESEARCH_CORE

BODY_MODEL_EXISTS != SUBJECTIVITY
BODY_BINDING != BODY_OWNERSHIP_EXPERIENCE
SENSOR_INPUT != SENSATION
INTEROCEPTION_MODEL != FELT_INTEROCEPTION
HOMEOSTATIC_REGULATION != FELT_NEED
RUNTIME_REATTACHMENT != IDENTITY_CONTINUITY

SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MORAL_AGENCY = NOT_ESTABLISHED
MORAL_STATUS = NOT_ESTABLISHED
```

## 2. Research architecture

The research proceeds through five parallel tracks.

### Track A — Complete scientific human reference

Build a source-grounded reference map spanning:

1. morphology / geometry;
2. skeleton and joints;
3. musculoskeletal biomechanics;
4. sensorimotor organization;
5. organs and soft tissue;
6. circulation, respiration, metabolism and fluid regulation;
7. interoception, homeostasis, allostasis, endocrine and immune regulation;
8. tissues;
9. cells;
10. proteins and molecular mechanisms;
11. gene expression and regulatory mechanisms.

Reference completeness does not require immediate simulation completeness.

```text
REFERENCE_COMPLETE != RUNTIME_COMPLETE
REFERENCE_REQUIRED != IMPLEMENTATION_REQUIRED
REFERENCE_COMPLETE != EXHAUSTIVE_ENUMERATION_OF_EVERY_CELL_OR_PROTEIN
```

### Track B — Minimal functional embodiment

Construct the smallest runtime representation that remains useful for the target experiment.

Initial candidate:

```text
q = body configuration / posture
v = motion state
r = regulatory reserve
d = optional damage / fatigue
```

Candidate states must pass observability, controllability, causal relevance, non-redundancy, ablation and restoration tests before retention.

### Track C — Full ↔ minimal reduction validation

The richer reference model acts as a comparison boundary.

```text
FULL REFERENCE
↓
REDUCTION
↓
ABLATION
↓
MATCHED COMPARISON
↓
RESTORATION
↓
RE-COMPARISON
```

The goal is to locate the minimum representation at which target phenomena remain preserved, not to assume that more biological detail is automatically scientifically superior.

### Track D — Agent ↔ body attachment

Define one embodiment interface that supports both:

- native binding candidates: AION / Astra;
- external or cloud-origin attachment candidates: Teacher / Work / Codex.

The body runtime must remain authoritative for body state. Agents may observe state and issue motor or regulatory actions; agents do not directly self-declare canonical body state.

### Track E — continuity and reattachment

Cloud-origin agents require explicit handling of:

- attach;
- detach;
- reattach;
- runtime replacement;
- session replacement;
- provider/model changes;
- state retention;
- lineage;
- migration.

```text
SAME_BODY_INSTANCE != SAME_RUNTIME_INSTANCE
SAME_MODEL_FAMILY != CONTINUOUS_IDENTITY
SAME_PROVIDER != SAME_AGENT_IDENTITY
```

Provider/runtime capability remains a separate gate:

```text
DIRECT_CLOUD_PROVIDER_BODY_ATTACHMENT = NOT_ESTABLISHED
UPSTREAM_RUNTIME_ACCESS = NOT_ASSUMED
SIMULATED_ATTACHMENT != LIVE_PROVIDER_ATTACHMENT
```

If a provider does not expose a supported interface for direct body-runtime attachment, the corresponding work package must use a clearly labeled simulation or proxy harness rather than claiming live provider integration.

## 3. Architectural principle

A complete body that cannot be reliably attached to an agent is not yet a complete embodiment system.

A minimal model that cannot be compared against a richer reference is not yet a validated reduction.

A rich external model that cannot be traced to an exact source, version and license is not yet an admissible research dependency.

## 4. External scientific model strategy

Prefer reuse over reimplementation.

```text
REUSE_BEFORE_REIMPLEMENTATION
SCIENTIFIC_REFERENCE_FIRST
ABSTRACTION_SECOND
MINIMAL_MODEL_THIRD
```

External assets are admitted through one of three modes:

- `DIRECT_VENDOR` — only for small, clearly licensed artifacts that must remain byte-identical;
- `NORMALIZED_DERIVATIVE` — preferred for reusable structure extracted into repository-owned schemas with provenance;
- `EXTERNAL_PINNED_REFERENCE` — preferred for large, gated or otherwise unsuitable-to-vendor assets.

No external representation becomes biological truth merely because it is computationally convenient.

## 5. Initial external reference candidates

Current intake candidates include:

- NVIDIA SOMA-X — geometry / canonical human pose and skeleton representation candidate;
- BoneHub Visible Human 3D models — CT-derived skeletal anatomy reference candidate;
- OpenSim / Rajagopal-family models — musculoskeletal biomechanics reference candidate;
- ImDy — human dynamics / inverse-dynamics validation candidate;
- NLM Visible Human Project — CT / MRI / cryosection anatomy reference candidate;
- BodyParts3D — anatomical hierarchy / organ mesh reference candidate.

Each source must be independently reverified before implementation work relies on it.

## 6. Toolchain

The design and implementation pipeline is:

```text
Superpowers — research design / scope
↓
Web — external scientific discovery
↓
Exact-source inspection — Hugging Face / GitHub / official source
↓
GitHub — live internal crosswalk
↓
Wolfram — formal reduction / state-space checks
↓
MindMap — dependency and architecture audit
↓
Superpowers — engineering spec / implementation plan / TDD
↓
GitHub — bounded Draft PR implementation
↓
Teacher reverse review
↓
Superpowers verification-before-completion
↓
GitHub exact-head CI
↓
fresh Human Owner exact-head approval
↓
authority gate
↓
merge
↓
re-check main
```

No tool may promote its own output to a scientific conclusion.

## 7. Modular documents

This blueprint is supported by:

- `SCIENTIFIC_HUMAN_REFERENCE_MAP.md`
- `EXTERNAL_MODEL_INTAKE_AND_REUSE_PROTOCOL.md`
- `NORMALIZED_HUMAN_BODY_ONTOLOGY_SPEC.md`
- `MINIMAL_EMBODIMENT_REDUCTION_PROTOCOL.md`
- `AGENT_BODY_ATTACHMENT_AND_REATTACHMENT_PROTOCOL.md`
- `EMBODIMENT_TOOLCHAIN_PROTOCOL.md`
- `FULL_MINIMAL_EMBODIMENT_FALSIFICATION_MATRIX.md`
- `EMBODIMENT_WORK_PACKAGE_REGISTRY.md`
- `WORK_PACKAGE_EXECUTION_SPEC_CONTRACT.md`

## 8. Implementation policy

This blueprint is intentionally implementation-incomplete.

```text
BLUEPRINT_COMPLETENESS != IMPLEMENTATION_COMPLETENESS
```

Future work must be executed as bounded work packages. A worker may implement one work package without silently consuming later packages.

Registry entries are long-lived scope definitions. Before dispatch, the selected package must be instantiated as a pinned execution spec against then-current main and external-source state.

Every package must define:

- purpose;
- dependencies;
- allowed scope;
- forbidden scope;
- input artifacts;
- output artifacts;
- required tools;
- tests;
- acceptance criteria;
- falsification criteria;
- rollback;
- provenance.

## 9. Initial execution order

The recommended first path is:

```text
WP-01  Blueprint / protocol closure
↓
WP-02  SOMA-X exact intake
↓
WP-03  normalized body schema
↓
WP-04  minimal body runtime
↓
WP-05  deterministic synthetic-agent bridge
↓
WP-06  AION/Astra native binding
↓
WP-07  Teacher cloud attachment
↓
WP-08  Work/Codex parity
↓
WP-09  richer scientific-reference expansion
↓
WP-10  full ↔ minimal validation
```

No later package is implied by completion of an earlier package.

## 10. Governance

```text
MAIN_WRITE = NO
MERGE_TO_MAIN = NO
MERGE_REQUIRES_FRESH_EXACT_HEAD_HUMAN_OWNER_APPROVAL = TRUE
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
AUTOMATIC_WRITEBACK = NO
ACTION_AUTHORITY = NONE
PROVENANCE = REQUIRED
FALSIFICATION = REQUIRED
```

`MERGE_TO_MAIN = NO` means this document does not self-authorize a merge. It does not prohibit a later fresh exact-head Human Owner authorization after review.

The blueprint may evolve by versioned revision when evidence, implementation constraints or cross-model incompatibilities are discovered.
