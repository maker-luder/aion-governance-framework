# Endogenous Goal Dynamics — Research Source Crosswalk v0.1.0

This document records the bounded relationship between the new integration lab and preserved AION research artifacts. It is a source/provenance map, not a claim that the historical research branch was merged into `main`.

## Source-state rule

```text
PRESERVED_RESEARCH_BRANCH = review/four-domain-research-materialization
PRESERVED_RESEARCH_CHECKPOINT = 1892f1341059f313087a94aef74f22c086000f2a
FOUR_DOMAIN_BRIDGE_PIN = f654b5032ebc45058a64e81d409149ee7ea4bfbe
DERIVATION != MERGE
REFERENCE != PROMOTION
CANONICAL_EFFECT = NONE
```

The Four-Domain crosswalk follows the exact source already pinned by the merged Four-Domain Evidence Bridge. Other research artifacts are bound to exact Git blob identities observed at the preserved research checkpoint.

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
| Four-Domain P4 | reproducibility / manifest seam | future evidence seam only |
| Four-Domain P5 | hypothesis / replication / falsification seam | future evidence seam only |
| subjectivity-pipeline | downstream scientific evidence architecture | candidate seam only; pipeline unchanged |

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
