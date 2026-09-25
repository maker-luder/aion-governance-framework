# Embodiment Work Package Registry

Status: `NAVIGATION / DRAFT`  
Canonical effect: `NONE`

## Purpose

Turn the master blueprint into bounded, independently assignable units for Teacher, Work, Codex or another authorized implementation worker.

A work package is not authorization to consume later work packages.

## Mandatory work-package fields

Every implementation package must define:

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
- license;
- relevant file inventory;
- source hashes where available;
- representation inventory;
- proposed extraction surface;
- limitations;
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

This work package may be split into:
- WP-09A anatomy;
- WP-09B biomechanics;
- WP-09C dynamics;
- WP-09D organ/soft tissue;
- WP-09E regulatory physiology;
- WP-09F tissue/cell/molecular reference.

## WP-10 — Full ↔ minimal validation

Purpose:
execute matched reduction, ablation, restoration, replay and transfer experiments.

Dependencies:
a minimal runtime plus at least one richer comparison layer.

Required:
- pre-registered metrics;
- matched external conditions;
- alternative hypotheses;
- restoration where feasible;
- provenance-bound results.

Output:
bounded conclusions only.

## Dependency overview

```text
WP-01
├─ WP-02 → WP-03 → WP-04 → WP-05
│                         ├─ WP-06
│                         └─ WP-07 → WP-08
└─ WP-09 ------------------------┐
                                ↓
                              WP-10
```

## Worker dispatch rule

A worker receives one explicit package.

Example:

```text
EXECUTE = WP-02
DO_NOT_EXECUTE = WP-03..WP-10
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
