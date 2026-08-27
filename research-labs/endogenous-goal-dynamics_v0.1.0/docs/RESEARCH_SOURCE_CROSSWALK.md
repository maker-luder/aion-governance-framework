# Endogenous Goal Dynamics — Research Source Crosswalk v0.1.0

This document records the bounded relationship between the integration lab and preserved AION research artifacts. It is a source/provenance map, not a claim that the historical research branch was merged into `main`.

## Source-state rule

```text
PRESERVED_RESEARCH_BRANCH = review/four-domain-research-materialization
PRESERVED_RESEARCH_CHECKPOINT = 1892f1341059f313087a94aef74f22c086000f2a
FOUR_DOMAIN_BRIDGE_PIN = f654b5032ebc45058a64e81d409149ee7ea4bfbe
INTEGRATION_CYCLE_MAIN_BASE = 3ae33dbefa26d7d343ba041deec5b8505dc0b8e7
PR56_CANDIDATE_HEAD = 67a901b16188e441040c8927806f41dd90e04b66
PR56_MERGE_COMMIT = 35840d4d5629872e830ee669a15b67b183091692
MAIN_INTEGRATION = COMPLETE
DERIVATION != MERGE
REFERENCE != PROMOTION
CANONICAL_EFFECT = NONE
```

The Four-Domain crosswalk follows the exact source already pinned by the merged Four-Domain Evidence Bridge. Other research artifacts are bound to exact Git blob identities observed at the preserved research checkpoint. The integration-cycle main base is a fixed historical input to the materialization cycle, not a moving assertion about the current tip of `main`.

## Integration roles

| Research surface | Role in this lab | Integration disposition |
|---|---|---|
| Four-Domain repository crosswalk | method / construct → question → operation → governance mapping | exact-source reference |
| causal-internal-state | matched intervention and ablation logic | methodological reuse |
| affective-cognitive-motivation | candidate motivation-state channel | conceptual adapter; no phenomenal claim |
| selective-memory-control | memory-confound boundary | memory kept separate from endogenous state |
| self-model-functional-ablation | history-dependent self-estimate channel | conceptual adapter |
| second-order-metacognition | monitoring/control channel and timing discipline | conceptual adapter |
| core-meaning-commitments | candidate organizing-commitment channel | conceptual adapter |
| Four-Domain P1 | temporal / correction / evaluation controls | control and evaluation seam |
| Four-Domain P2 | provenance + deterministic matched context assembly | provenance and context seam |
| Four-Domain P3 | perturbation / ablation / resilience controls | adversarial control seam |
| Four-Domain P4 | reproducibility / manifest seam | future evidence seam only |
| Four-Domain P5 | hypothesis / replication / falsification seam | future evidence seam only |
| subjectivity-pipeline | downstream scientific evidence architecture | candidate seam only; EGD has no runtime import of subjectivity-pipeline internals |

## Exact artifact bindings

The executable package exposes these identities through `PINNED_RESEARCH_SOURCES`:

```text
FOUR_DOMAIN_METHOD
  commit = f654b5032ebc45058a64e81d409149ee7ea4bfbe
  path   = research-workbench/four-domain-materialization/2026-08-09/FOUR_DOMAIN_REPOSITORY_CROSSWALK.md
  blob   = 7e55741b85b27d383b4b721b834b1744c6c03fb9

CAUSAL_INTERVENTION_METHOD
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/causal-internal-state_v0.1.0/README.md
  blob   = 0b29604dc75098ac4a38f8c400737ea12edc7808

AFFECT_MOTIVATION_CHANNEL
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/affective-cognitive-motivation_v0.1.0/README.md
  blob   = 576ece0bb4281b3559e4b623cdc53279aa2e1719

SELECTIVE_MEMORY_CONFOUND_CONTROL
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/selective-memory-control_v0.1.0/README.md
  blob   = 561c53bc2f2692b0e8fa06b702eaffa319018569

SELF_MODEL_CHANNEL
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/self-model-functional-ablation_v0.1.0/README.md
  blob   = 8907f338024c6125e1fd9ccd2160715ed6580831

METACOGNITIVE_CONTROL_CHANNEL
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/second-order-metacognition_v0.1.0/README.md
  blob   = dba29c8df3c345e3380c7caadc7eafb53f5f502d

CORE_MEANING_CHANNEL
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/core-meaning-commitments_v0.1.0/README.md
  blob   = 743d2e4683793967f1bca94e646e655730ba9fc1

P1_TEMPORAL_CORRECTION_EVALUATION
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/four-domain-p1-materialization_v0.1.0/README.md
  blob   = 58169c3719d768e26069cdd3bd1d24066bc10f69

P2_PROVENANCE_CONTEXT_ASSEMBLY
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/four-domain-p2-materialization_v0.1.0/README.md
  blob   = a98ac0f0e493ebc18fd820447e24f58fd98e7e6d

P3_RESILIENCE_ABLATION
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/four-domain-p3-resilience-experiments_v0.1.0/README.md
  blob   = 75f1913c9f4e5030534d059968ea56f8645b1013

SUBJECTIVITY_EVIDENCE_SEAM
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/subjectivity-pipeline_v0.1.0/README.md
  blob   = 59259dd26d3fd88e57b1ff40de6ac885e9df9dbd

REPRODUCIBILITY_LAYER
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/four-domain-p4-public-reproducibility_v0.1.0/README.md
  blob   = 693d9b87e2de265996082ad52e85a798123cc984

HYPOTHESIS_FALSIFICATION_LAYER
  commit = 1892f1341059f313087a94aef74f22c086000f2a
  path   = research-labs/four-domain-p5-hypothesis-convergence_v0.1.0/README.md
  blob   = 41fe368cc7c33fd99ac901338f6877f0f387763b
```

These bindings are provenance snapshots for the EGD integration cycle. They do not impose an indefinite immutability requirement on a separately governed downstream research lab. Later subjectivity-pipeline evolution must remain explicit, reviewable, and uncoupled from EGD runtime internals unless a separately reviewed adapter is introduced.

## Research-family coverage versus wholesale integration

The preserved workbench contains additional adversarial, authority, contamination, cross-substrate, theory-indicator, trajectory, evidence-normalization and matched-divergence experiments. v0.1.0 does not import all of their code into one agent. Instead, it integrates the research **families** needed to test endogenous goal dynamics while preserving module-level ablation and future falsification.

This is deliberate:

```text
ALL_CODE_IN_ONE_AGENT = NO
CROSS_RESEARCH_METHOD_INTEGRATION = YES
MODULE_ABLATION_PRESERVED = YES
HISTORICAL_BRANCH_MERGE = NO
```

A giant merged runtime would make causal attribution worse: if the outcome changed, the experiment could not identify which mechanism contributed. Therefore additional research families should enter through explicit adapters or falsifiers rather than by silent import.

## Non-claims

```text
INTERNAL_STATE_HAS_CAUSAL_ROLE_CANDIDATE != SUBJECTIVITY
AFFECTIVE_REPRESENTATION != FELT_AFFECT
SELF_MODEL_FUNCTION != PHENOMENAL_SELF
METACOGNITIVE_CONTROL != METACOGNITIVE_FEELING
CORE_MEANING_STRUCTURE != HUMAN_MEANING
PERSISTENCE != IDENTITY_CONTINUITY
REPLICATION != SCIENTIFIC_TRUTH
TEST_PASS != THEORY_CONFIRMATION
```

## Hardening-cycle selective materialization record

This cycle inspected the exact source artifacts and their implementation surfaces at the preserved
checkpoint. It did not import those packages into the candidate runtime.

| Role | Exact implementation surface inspected | Reused | Reconstructed locally | Intentionally omitted |
|---|---|---|---|---|
| Causal internal state | `aion_causal_internal_state.core` (`Condition`, `TrialObservation`, `CausalAssessment`) | matched intervention/ablation discipline | typed matched manifests and explicit comparison validity | historical package/runtime dependency |
| Affective motivation | `models`, `engine`, `policy` | finite represented signal boundary | neutral `AFFECT_MOTIVATION` channel | phenomenal/biological interpretation and runtime policy |
| Selective memory | `aion_selective_memory.core` (`MemoryRecord`, `RetrievalTrace`, store) | retrieval trace/confound separation | immutable retrieved-memory manifest and fingerprint | historical store implementation and automatic memory writes |
| Self-model ablation | `model`, `experiment` | independent finite self-estimate ablation | `SELF_MODEL` signal channel | full benchmark/action model |
| Second-order metacognition | monitor, records, intervention, verification, study adapters | monitoring/control and verification discipline | `METACOGNITION` channel and fail-closed timing checks | provider verification workbench and unrelated studies |
| Core meaning | models, engine, structure, policy | organizing-commitment boundary | `CORE_MEANING` channel | namespace transfer, canonical promotion, relational authority |
| P1 | temporal, correction, evaluation | version/predecessor/correction/evaluation shape | `P1TemporalCorrectionAdapter` | historical ledgers/harness runtime |
| P2 | retrieval, provenance, orchestration | deterministic frame and provenance completeness | `P2ContextProvenanceAdapter` | historical retrieval/orchestrator runtime |
| P3 | ablation, perturbation, longitudinal, authority | perturbation/contamination/authority controls | `P3PerturbationAdapter` | historical authority tiers and unrelated experiment families |
| P4 | manifest, observation, reproduction | manifest/replay/contamination semantics | `P4ReproducibilityAdapter` | public observation/reproduction registry runtime |
| P5 | hypothesis, replication, disagreement, convergence | falsifier lifecycle/replication/HOLD semantics | `P5HypothesisAdapter` plus F1–F12 evaluator | autonomous convergence or promotion |
| Subjectivity pipeline | integration-base/preserved models and engine | stage ordering and non-claim boundary | candidate-only bridge artifact | direct runtime coupling or automatic admission |

The selective reconstruction is narrower than direct historical imports. Direct imports would bind a
current research candidate to preserved branch-only packages, increase the intervention surface, and
weaken causal attribution. The local adapters keep exact provenance while exposing only the fields used
by this hypothesis.

## Integration-base main bindings reused directly

Integration-cycle main base: `3ae33dbefa26d7d343ba041deec5b8505dc0b8e7`.

The following blob identities describe the current-main modules that were inspected and reused when the cycle began. They remain fixed provenance bindings; they are not intended to follow future edits to `main`.

```text
EVIDENCE_INTEROP_PROV
  path = components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/prov_export.py
  blob = ad38d3352557f1b5aac3703ba8d5dc68e10e29b8

EVIDENCE_INTEROP_RO_CRATE
  path = components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/rocrate_export.py
  blob = 586b28db73d7afeef36811d29c0315102b49e82f

EVIDENCE_INTEROP_IN_TOTO
  path = components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/intoto_export.py
  blob = 3da38ba27dac77c17810672064f3c0af80ce3284

EVIDENCE_INTEROP_INSPECT
  path = components/aion_evidence_interop_v0.1.0/src/aion_evidence_interop/inspect_export.py
  blob = 2e5e688c30bec3e9a55236249c99da3957c7af48

SUBJECTIVITY_PIPELINE_MODELS (integration-base snapshot; downstream lab may evolve separately)
  path = research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/models.py
  blob = ddeea0e599105e3c2113419f03470d8004f3d14f
```

`verify_source_bindings(repository)` checks every historical and integration-base main entry directly against
local Git objects. Missing refs and blob drift are reported as failures. This verification checks the pinned historical snapshots themselves; it is not a ban on later separately governed source evolution.

## Integration disposition

```text
PR56_CANDIDATE_HEAD = 67a901b16188e441040c8927806f41dd90e04b66
PR56_MERGE_COMMIT = 35840d4d5629872e830ee669a15b67b183091692
MAIN_INTEGRATION = COMPLETE
SUBJECTIVITY_EVIDENCE_ADMISSION = NOT_AUTOMATIC
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

The merge disposition does not alter any pinned historical source identity and does not convert a candidate mechanism into a scientific conclusion.

## Attribution preserved for this cycle

```text
RESEARCH_DIRECTION = USER_GIVEN
INTEGRATION_ARCHITECTURE = GPT_PROPOSED
INITIAL_V0_1_IMPLEMENTATION = GPT_PRODUCED_UNDER_USER_AUTHORIZATION
CURRENT_HARDENING_IMPLEMENTATION = CODEX
HISTORICAL_SOURCE_ATTRIBUTION = PRESERVE_EXISTING_RECORDS
IMPLEMENTATION_TASK_MERGE_AUTHORITY = NOT_GRANTED
PR56_EXACT_HEAD_HUMAN_OWNER_MERGE_AUTHORITY = GRANTED_SEPARATELY
```
