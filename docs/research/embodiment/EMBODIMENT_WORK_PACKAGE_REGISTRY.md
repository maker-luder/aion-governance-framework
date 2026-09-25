# Embodiment Work Package Registry

Status: `NAVIGATION / DRAFT`  
Canonical effect: `NONE`

## Purpose

Turn the master blueprint into bounded, independently assignable units for Teacher, Work, Codex or another authorized implementation worker.

A work package is not authorization to consume later work packages.

`MERGE_TO_MAIN = NO` is the default/self-authorization boundary for a work package. It does not prevent a later fresh exact-head Human Owner merge authorization after the package is reviewed and verified.

## Registry versus execution spec

This registry defines stable package boundaries and dependencies.

It is not, by itself, a worker execution order.

```text
REGISTRY_ENTRY
!= PINNED_EXECUTION_SPEC
!= IMPLEMENTATION_AUTHORIZATION
```

Before dispatch, the selected WP must be instantiated using `WORK_PACKAGE_EXECUTION_SPEC_CONTRACT.md` against the then-current exact main SHA and exact upstream dependencies.

## Mandatory execution-spec fields

Every dispatched implementation package must define:

```text
WORK_PACKAGE_ID
TITLE
PURPOSE
DEPENDENCIES
ALLOWED_FILES
FORBIDDEN_SCOPE
INPUT_ARTIFACTS
OUTPUT_ARTIFACTS
REQUIRED_TOOLS
TESTS
ACCEPTANCE_CRITERIA
FALSIFICATION_CRITERIA
ROLLBACK
PROVENANCE
MERGE_TO_MAIN = NO
MERGE_REQUIRES_FRESH_EXACT_HEAD_HUMAN_OWNER_APPROVAL = TRUE
```

## WP-01 — Blueprint closure

Purpose:
complete and review the architectural blueprint.

Dependencies:
none beyond live main and external-source review.

Outputs:
the documents in this directory.

Forbidden:
runtime implementation; external asset vendoring; changes to AION/Astra runtime.

Acceptance:
- internal consistency;
- no unresolved scope contradictions;
- core scientific boundary preserved;
- toolchain and package dependencies explicit.

## WP-02 — SOMA-X exact intake

Purpose:
perform exact-source intake for SOMA-X as the first external body-model case.

Dependencies:
WP-01.

Required tools:
Web → Hugging Face → GitHub → reverse review.

Outputs should include:
- exact repo/revision;
- license plus any file-specific/gated terms;
- supply-chain / serialization security inventory;
- relevant file inventory;
- source hashes where available;
- representation inventory;
- proposed extraction surface;
- limitations;
- population / subject assumptions where relevant;
- human-data provenance / access terms where relevant;
- admission mode.

Forbidden:
- body runtime implementation;
- Teacher attachment;
- silent full-repo vendoring;
- anatomical-completeness claims.

Initial admission target:
`NORMALIZED_DERIVATIVE`.

## WP-03 — Normalized body schema

Purpose:
implement the first versioned AION human-body ontology / schema and deterministic SOMA-X crosswalk.

Dependencies:
WP-02.

Outputs:
- schema;
- extractor / normalizer;
- provenance record;
- deterministic tests;
- dropped-field report.

Forbidden:
full scientific-body runtime.

## WP-04 — Minimal body runtime

Purpose:
implement MVM-0/MEB-0 body state using the normalized representation.

Dependencies:
WP-03.

Initial state:
```text
q
v
r
```

Optional `d` requires its own admission evidence.

Required:
- authoritative body-state engine;
- deterministic transition tests;
- proprioception adapter;
- interoception adapter;
- action adapter;
- replay.

Forbidden:
cloud-agent attachment until base runtime passes.

## WP-05 — Deterministic synthetic-agent bridge

Purpose:
validate attachment lifecycle without LLM stochasticity.

Dependencies:
WP-04.

Required sequence:
```text
ATTACH
OBSERVE
ACT
STATE_CHANGE
OBSERVE
DETACH
REATTACH
```

Acceptance:
deterministic expected results and complete provenance.

## WP-06 — AION/Astra native binding baseline

Purpose:
bind the minimal body interface to existing AION/Astra individual runtime contexts without erasing separate lineage.

Dependencies:
WP-05 plus existing native runtime components.

Required:
- distinct body instances;
- distinct runtime/event lineage;
- shared ontology allowed;
- no shared individual state.

Forbidden:
reinterpretation of shared genesis as shared identity.

## WP-07 — Teacher cloud attachment candidate

Purpose:
create the first external/cloud body attachment candidate.

Dependencies:
WP-05; preferably comparison-ready with WP-06.

Required:
- explicit runtime instance;
- body instance;
- attach/detach/reattach receipts;
- provider/model provenance;
- stable observation/action contract.

Capability gate:
- reverify whether a supported upstream provider/runtime attachment interface actually exists;
- if unavailable, implement only a clearly labeled simulated/proxy cloud adapter;
- do not report simulated attachment as live provider integration.

Forbidden:
claims of identity continuity or body-ownership experience.

## WP-08 — Work / Codex parity

Purpose:
demonstrate that the cloud-attachment interface is reusable without shared body state.

Dependencies:
WP-07.

Required:
- separate body instances;
- separate runtime attachment records;
- shared interface/schema only.

Forbidden:
copying Teacher state into Work/Codex.

## WP-09 — Rich scientific-reference expansion

Purpose:
expand reference coverage using BoneHub, OpenSim/Rajagopal, ImDy, Visible Human, BodyParts3D and later tissue/cell/molecular sources.

Dependencies:
WP-01. Individual sub-intakes may proceed independently if they do not alter runtime.

Each source should receive its own intake record and admission mode.

For human-derived anatomy/medical sources, each intake must also record subject/population scope and available donor/subject provenance and access terms.

For executable or serialized ML artifacts, each intake must record supply-chain/security handling before execution.

This work package may be split into:
- WP-09A anatomy;
- WP-09B biomechanics;
- WP-09C dynamics;
- WP-09D organ/soft tissue;
- WP-09E neural / sensory systems;
- WP-09F regulatory physiology;
- WP-09G tissue/cell/molecular reference;
- WP-09H environmental coupling and temporal biology.

## WP-10 — Full ↔ minimal validation

Purpose:
execute matched reduction, ablation, restoration, replay and transfer experiments.

Dependencies:
WP-04 plus at least one relevant WP-09 richer comparison layer. WP-05 is additionally required when the registered comparison concerns agent-coupled behavior rather than body-runtime behavior alone.

Required:
- pre-registered metrics;
- matched external conditions;
- alternative hypotheses;
- restoration where feasible;
- provenance-bound results;
- deterministic replay for deterministic harnesses;
- paired/matched repeated trials for stochastic agents;
- pre-registered run count or stopping rule where repeated trials are used;
- uncertainty/effect-size reporting when deterministic replay is unavailable.

Output:
bounded conclusions only.

## WP-11 — Body ↔ self/world-model coupling

Purpose:
connect embodiment evidence to the repository's existing bounded `SELF_WORLD_MODEL` and worldview-like normative research surfaces without creating duplicate self-model, world-model or worldview ontologies.

Dependencies:
- WP-04 minimal body runtime;
- existing triadic-state / self-world-model research surface;
- WP-05 when the experiment requires an agent-coupled action loop.

Required:
- actual body state, external world state, represented world model, and worldview-like normative structure remain separable;
- external environment content is supplied through a bounded external simulator/dataset/benchmark adapter rather than a repository-built general world simulator;
- exact environment source/version/configuration is provenance-bound;
- actual body state and represented self/world state remain separate;
- admitted sensor/observation path is explicit;
- prediction error / update path is provenance-bound;
- body-change-with-update and body-change-with-update-block conditions;
- stale self-model condition;
- direct body-state leakage control;
- bounded developmental/aging trajectory only when registered.

Current body-profile boundary:

```text
CURRENT_ACTIVE_BODY_PROFILE = ADULT_MALE
FEMALE_BODY_PROFILE = FUTURE_EXTENSION / NOT_CURRENT_ACTIVE_SCOPE
POPULATION_GENERALIZATION = NO
```

Forbidden:
- second conflicting self-model/world-model/worldview ontology;
- building a general-purpose world simulator inside this work package;
- automatic copying of canonical body state into self-model;
- treating adaptive self-model update as subjectivity/selfhood evidence.

Output:
bounded evidence about self/world-model calibration or causal role under body/environment change.

## Dependency overview

```text
WP-01
├─ WP-02 → WP-03 → WP-04 → WP-05
│                         ├─ WP-06
│                         └─ WP-07 → WP-08
└─ WP-09 ------------------------┐
                                ↓
                              WP-10

WP-04 + existing SELF_WORLD_MODEL
  └─ WP-11 Body ↔ self/world-model coupling
     └─ WP-10 when coupling is part of the registered full/minimal experiment
```

## Worker dispatch rule

A worker receives one explicit package **plus its reviewed pinned execution spec**. The registry summary alone is insufficient for implementation.

Example:

```text
EXECUTE = WP-02
DO_NOT_EXECUTE = WP-03..WP-11
MAIN_WRITE = NO
MERGE_TO_MAIN = NO
```

Cross-package discovery is allowed as read-only context. Cross-package implementation is not.

## Completion semantics

```text
WP_N_PASS
!= WP_N+1_AUTHORIZED
```

No package transition occurs automatically.
