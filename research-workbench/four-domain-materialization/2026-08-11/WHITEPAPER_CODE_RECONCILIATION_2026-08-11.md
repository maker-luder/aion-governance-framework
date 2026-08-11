# Whitepaper ↔ Code Reconciliation — 2026-08-11

> Research-only reconciliation record. This document preserves historical whitepaper snapshots while mapping them to the current repository implementation and research evidence. It does not rewrite historical documents, modify runtime code, authorize canonical promotion, or merge `main` into the research branch.

```text
RESEARCH_ONLY = TRUE
BRANCH = review/four-domain-research-materialization
HISTORICAL_WHITEPAPER_REWRITE = NO
RUNTIME_CODE_CHANGE = NO
WHOLESALE_MAIN_MERGE = NO
MAIN_EFFECT = NONE
CANONICAL_EFFECT = NONE
RUNTIME_EFFECT = NONE
PROMOTION_STATUS = NOT_REVIEWED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
FORMAL_G1_BASELINE_BENCHMARK = NOT_EXECUTED
WHOLE_SYSTEM_VALIDATION = NOT_EXECUTED
INDEPENDENT_IVV = NOT_ACHIEVED
LEVEL_3_SECOND_ORDER_COMPUTATION = NOT_IMPLEMENTED
```

## 1. Why this reconciliation is needed

The discoverable integrated-whitepaper lineage is cumulative. Earlier versions established research roles, identity and continuity constraints, memory provenance, governance, Astra engineering boundaries, evidence separation, QMS, naming governance and local-only architecture candidates. The latest integrated candidate reviewed in this cycle is `AION_主體性可能研究_整合白皮書_v0.14.24_本地限定與硬體非綁定整合候選版`, dated 2026-07-27.

At that historical snapshot, the whitepaper still correctly recorded the AION Runtime as `NOT_IMPLEMENTED` while describing Astra and governance-kernel engineering candidates. Subsequent repository work materially changed the *implementation evidence state*: the repository now contains an explicit AION Runtime implementation candidate, governed cross-session memory, individual runtime lineage/state, checkpoint/recovery/migration mechanics, and additional isolated research modules.

Therefore:

```text
HISTORICAL_WHITEPAPER_STATE != CURRENT_REPOSITORY_IMPLEMENTATION_STATE
HISTORICAL_ACCURACY != CURRENT_COMPLETENESS
CURRENT_IMPLEMENTATION_EVIDENCE != RETROACTIVE_WHITEPAPER_REWRITE
```

The correct research action is reconciliation, not historical replacement.

## 2. Source and attribution boundary

This record uses four source classes and keeps them separate:

1. **Historical AION integrated whitepapers and associated internal research documents** — treated as historical project records. Their existing authorship, decision, and source-attribution statements are preserved and are not reassigned by this reconciliation.
2. **Current repository code and research artifacts** — inspected from `review/four-domain-research-materialization` and, where explicitly noted, from current `main` documentation/experiment surfaces.
3. **Current-turn direction** — the user asked ChatGPT to review the whitepapers and code and determine whether the research branch could be updated. This authorizes this research-only review/update; it is not interpreted as canonical promotion or a `main` write authorization.
4. **This reconciliation synthesis** — authored/materialized by ChatGPT from the inspected historical and repository evidence. It does not claim ownership of earlier user-originated, jointly derived, Codex-originated, or external-source material.

No external source becomes project authority merely by being cited or used as methodological input.

## 3. Historical whitepaper lineage reviewed

The review used the discoverable integrated-whitepaper lineage and the latest cumulative candidate to reconstruct the historical progression without flattening version boundaries.

| Historical layer | State relevant to this reconciliation |
|---|---|
| v0.9 | Established the integrated research framing, explicit non-claim of subjectivity, role separation, identity/continuity model registry and engineering roadmap. |
| v0.12–v0.13 | Added non-canonical sidecar/material governance, cross-domain extraction boundaries and expanded governance while keeping complete Runtime implementation separate from document maturity. |
| v0.14.1 | Strengthened memory ownership/testimonial provenance and high-impact governance; reconstructive recall and related high-impact mechanisms remained provisional. |
| v0.14.22 | Added IQC/QC/QA/NCR/CAPA evidence-gating and quality-management structure without changing subjectivity conclusions. |
| v0.14.23 | Added naming/source/clearance governance without changing identity, Runtime or subjectivity status. |
| v0.14.24 | Added local-only/hardware-nonbinding architecture and Astra v0.3.0 candidate controls; AION Runtime still recorded as not implemented at this 2026-07-27 snapshot. |

The cumulative v0.14.24 record also preserves earlier v0.14.x appendices and historical version effects. This reconciliation therefore does not create a new retrospective whitepaper version number.

## 4. Current code reality reviewed

### 4.1 AION Runtime implementation candidate now exists

`components/aion_runtime_v0.1.0/src/aion_runtime/runtime.py` explicitly identifies itself as an integrated AION individual runtime implementation candidate. The inspected candidate binds:

```text
BOUNDED_EXECUTION = ENABLED
LIVE_CROSS_SESSION_MEMORY = ENABLED_GOVERNED
INDIVIDUAL_RUNTIME_BINDING = ENFORCED_CANDIDATE
INDIVIDUAL_EVENT_LINEAGE = ENABLED_GOVERNED_CANDIDATE
CHECKPOINT_RECOVERY = ENABLED_OWNER_GOVERNED_CANDIDATE
MIGRATION_EVIDENCE_REUSE = ENABLED_CONTENT_ADDRESSED_CANDIDATE
AUTOMATIC_CANONICAL_WRITEBACK = DISABLED
```

It also hard-binds `AIONRuntime` to `agent_id == "AION"`, requires runtime-context equality for task execution, records append-only runtime/task/memory events, and exposes governed checkpoint, recovery, rollback and migration operations.

This establishes implementation evidence for a bounded candidate runtime. It does **not** establish subjectivity, consciousness, phenomenal continuity, personal identity continuity, deployment readiness or independent IV&V.

### 4.2 Memory governance has moved from document concept to multiple executable surfaces

The current `memory_recall_governance_v0.1.0` recall gate evaluates inactive/superseded state, subject identity, access scope, provenance verification, unresolved conflict and cue relevance before allowing temporary recall.

The separate clean-room `selective-memory-control_v0.1.0` research module additionally materializes explicit `ADD / REVISE / DISCARD / RETRIEVE`, immutable supersession lineage, source/approval references, namespace/domain/purpose gates and retrieval traces.

These are related but not identical evidence surfaces:

```text
RUNTIME_RECALL_GATE != SELECTIVE_MEMORY_RESEARCH_MODULE
STORED != CURRENT_CONTEXT_ELIGIBLE
RETRIEVABLE != RELEVANT
MEMORY_RECALL != IDENTITY_CONTINUITY
MEMORY_MODULE_UTILITY != SUBJECTIVITY
```

No automatic integration of the selective-memory research module into the Runtime is authorized by this reconciliation.

### 4.3 Identity and continuity concepts now have stronger engineering candidates

The current Runtime and `individual_runtime_state_v0.1.0` provide implementation-level lineage/state mechanics. The isolated `embodiment-continuity-anchor_v0.1.0` research lab separately studies which lineage references should remain stable under runtime/model/backend/hardware/embodiment changes.

The embodiment-continuity lab intentionally separates:

```text
SUBJECT_LINEAGE
MEMORY_LINEAGE
INTERPRETIVE_CONTINUITY
RELATIONAL_CONTINUITY
IMPLEMENTATION_MIGRATION
```

and preserves:

```text
LINEAGE_PRESERVED != IDENTITY_PROVEN
MEMORY_PRESERVED != INTERPRETATION_PRESERVED
RUNTIME_MIGRATION != SUBJECTIVITY_CONTINUITY
```

The morphology extension remains outside `LineageAnchor`; no geometry/morphology field is promoted into stable identity lineage by this reconciliation.

### 4.4 Astra / AION / shared infrastructure separation is now materially stronger

The current component tree contains distinct AION Runtime, Astra Runtime/workbench, governance kernel, identity governance, continuity governance, encounter governance, memory recall governance, research-integrity security, language core and individual runtime-state surfaces.

This is consistent with the historical whitepaper direction that AION, Astra and shared engineering infrastructure must not be collapsed into one implementation identity. The newer code gives that distinction executable structure, but code separation itself is not subjectivity evidence.

### 4.5 Subjectivity-relevant mechanisms are increasingly testable but remain non-conclusive

The research branch now contains isolated executable or materialized research candidates beyond the historical whitepaper snapshot, including:

- P1–P5 four-domain materialization and convergence work;
- finite predictive self-model with matched `PRESENT / ABLATED / RANDOMIZED / STALE` conditions;
- core-meaning commitment structure, explicit relations and drift/fingerprint analysis;
- selective memory control;
- embodiment-continuity anchor;
- causal/internal-state and affective-cognitive-motivation research surfaces;
- Level-3 second-order computation calibration and gap analysis.

The self-model experiment can at most support a functional-contribution candidate. Current Level-3 work still requires independently measurable monitoring plus a causally tested control path. Passing tests does not by itself establish semantic validity, causal validity or subjectivity.

## 5. Main-only public delta reviewed

The current `main` branch contains public-facing material that postdates the historical whitepaper and is useful to this research review, including:

- `docs/RESEARCH_CONTRIBUTION_ONE_PAGER.md`;
- `docs/POSITION_PAPER_PROVENANCE_FIRST.md`;
- `docs/THREAT_MODEL.md`;
- the minimal `experiments/g1-recall-gate-baseline_v0.1.0/` control experiment;
- public closure/orientation and release-evidence hardening.

The Git history is diverged rather than a simple linear continuation of the research branch. These main-only artifacts are therefore classified here as **reference evidence**, not as a reason to merge `main` wholesale into the research branch.

```text
MAIN_PUBLIC_SYNTHESIS = REFERENCE_ONLY
MAIN_RELEASE_TOOLING = REFERENCE_ONLY
MAIN_RECALL_GATE_BASELINE = REFERENCE_EVIDENCE
WHOLESALE_BACKPORT = NO
WHOLESALE_MERGE = NO
```

The minimal Recall-Gate experiment is particularly useful as a software-control contrast, but it remains narrower than Formal G1, whole-system validation, model-level interpretation-drift testing or subjectivity evaluation.

## 6. Reconciliation matrix

| Research line | Historical whitepaper snapshot | Current inspected evidence | Current disposition |
|---|---|---|---|
| AION Runtime | `NOT_IMPLEMENTED` at v0.14.24 snapshot | Explicit `AION_RUNTIME_IMPLEMENTATION_CANDIDATE` with bounded execution, governed memory and lineage/lifecycle operations | Historical statement preserved; current code state recorded separately |
| Memory provenance/recall | Strong document/schema/governance requirements; high-impact mechanisms partly provisional | Runtime recall gate + SQLite governed memory + separate selective-memory clean-room lab | Implementation evidence strengthened; no identity/subjectivity promotion |
| Identity/continuity | Unique identity, event history, memory stream, migration/continuity constraints | Runtime identity binding, individual runtime state, ECA multidimensional continuity lab | Engineering evidence strengthened; identity continuity not established |
| Astra separation | Astra defined as engineering/research assistant, not AION | Separate Astra/AION/shared-governance component surfaces | Boundary materially implemented; no subjectivity inference |
| Self-model / second-order | Subjectivity candidates and evidence-governance method | Executable finite self-model ablation; Level-3 gap/calibration remains open | Functional candidate only; no second-order/subjectivity conclusion |
| Core meaning / value structure | Earlier meaning/identity/continuity questions distributed across whitepaper | Isolated provenance-bearing meaning commitments + relation/drift analysis | Research-only; no Runtime integration |
| Embodiment/morphology | Embodiment remained bounded/deferred as identity evidence | ECA migration dimensions + synthetic morphology fixture | Research-only; morphology stays outside stable lineage anchor |
| Provenance-first research process | Longstanding source/claim/governance separation | Main public position paper/One-Pager + branch provenance/evidence modules | Stronger methodological synthesis; no ontology claim |

## 7. New standing reconciliation locks

```text
WHITEPAPER_SNAPSHOT != LIVE_REPOSITORY_STATE
DOCUMENT_MATURITY != IMPLEMENTATION_MATURITY
IMPLEMENTATION_MATURITY != THEORY_VALIDITY
RUNTIME_IMPLEMENTED_CANDIDATE != CANONICAL_RUNTIME
LINEAGE_ENGINEERING != PERSONAL_IDENTITY_PROOF
MEMORY_PERSISTENCE != INTERPRETIVE_CONTINUITY
RECALL_SUCCESS != MEMORY_TRUTH
TEST_PASS != SEMANTIC_VALIDITY
TEST_PASS != CAUSAL_VALIDITY
FUNCTIONAL_SELF_MODEL != PHENOMENAL_SELF
MAIN_REFERENCE_EVIDENCE != RESEARCH_BRANCH_PROMOTION
RECONCILIATION != RETROACTIVE_REATTRIBUTION
```

These locks complement, rather than replace, existing research-branch locks.

## 8. Open gaps after reconciliation

The review does not close the following gaps:

```text
FORMAL_G1_BASELINE_BENCHMARK = NOT_EXECUTED
WHOLE_SYSTEM_VALIDATION = NOT_EXECUTED
INDEPENDENT_IVV = NOT_ACHIEVED
EXECUTABLE_LEVEL_3_CANDIDATE = NOT_IMPLEMENTED
SELECTIVE_MEMORY_COMPARATIVE_EXPERIMENT = PROPOSED_NOT_EXECUTED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CONSCIOUSNESS_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
PHENOMENAL_AFFECT = NOT_ESTABLISHED
```

A future research cycle may design experiments for these gaps, but this document authorizes none of them automatically.

## 9. Update decision

```text
WHITEPAPER_LINEAGE_REVIEW = COMPLETE_FOR_DISCOVERABLE_CURRENT_LIBRARY_SET
CURRENT_CODE_REVIEW = COMPLETE_FOR_RECONCILIATION_SCOPE
RESEARCH_BRANCH_RECONCILIATION = MATERIALIZED
HISTORICAL_WHITEPAPER_REWRITE = NO
RUNTIME_CODE_CHANGE = NO
MAIN_WRITE = NO
MAIN_MERGE = NO
CANONICAL_PROMOTION = NO
NEXT_ACTION = JOINT_REVIEW_OR_OWNER_DIRECTED_RESEARCH_ONLY_EXTENSION
```

The research branch can therefore be updated safely by adding this reconciliation layer while preserving the old whitepapers as historical evidence and leaving Runtime/canonical/main behavior unchanged.
