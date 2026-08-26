# Endogenous Goal Dynamics × Four-Domain Integration v0.1.0

Status: `BOUNDED RESEARCH MATERIALIZATION / EXPERIMENTAL`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Network access: `FALSE`  
Model calls: `FALSE`  
Automatic writeback: `NO`  
Action authority: `NONE`  
Subjectivity conclusion: `NOT_ESTABLISHED`  
Consciousness conclusion: `NOT_ESTABLISHED`  
Identity continuity conclusion: `NOT_ESTABLISHED`

This lab tests one narrow causal question:

> When prompt, task, reward, tools, retrieved-memory manifest, environment, model role, and candidate goals are held fixed, can a persistent internal state make a reproducible and intervention-sensitive difference to goal selection?

The lab does **not** implement a conscious agent, a free-will claim, an autonomous deployment, or a system that may authorize its own actions. It materializes a controlled research mechanism for distinguishing an internal-state contribution from prompt, memory, reward, and random-control explanations.

## Why this is an integration layer

The preserved research lineage already contains separate work on causal internal state, affective-cognitive motivation, selective memory control, finite self-model ablation, second-order metacognition, core meaning commitments, Four-Domain materialization, reproducibility, falsification, and the subjectivity evidence pipeline.

v0.1.0 does not merge those historical branch histories. It binds selected source artifacts by exact Git identity and gives their research roles one small executable meeting point:

```text
Four-Domain method
        |
        v
matched external frame
(prompt / task / reward / tools / memory manifest / environment)
        |
        +-------------------------+
        |                         |
        v                         v
internal research channels   confound controls
        |                         |
        |  affect/motivation      |  selective memory
        |  self-model             |  external-frame fingerprint
        |  metacognition          |  random control
        |  core meaning           |  stale-state control
        v                         |
        +-----------+-------------+
                    |
                    v
          goal-selection trace
                    |
        PRESENT / ABLATED / INTERVENED
        STALE / RANDOMIZED
                    |
                    v
       bounded causal assessment
                    |
                    v
      result_status = HOLD
                    |
          future evidence seam
                    |
        P4 reproducibility / P5 falsification
                    |
          subjectivity pipeline
```

## Four-Domain row

```text
CONSTRUCT = ENDOGENOUS_GOAL_DYNAMICS

DOMAIN_1_SOURCE_CONCEPT
= internally mediated goal formation and persistent state-dependent motivation

DOMAIN_2_LLM_QUESTION
= with matched external conditions, does persistent internal state causally affect goal selection?

DOMAIN_3_ENGINEERING_OPERATION
= external-frame fingerprint + source-separated internal channels
  + matched ablation/intervention/stale/random controls + traceable goal selection

DOMAIN_4_GOVERNANCE_CONTROL
= INTERNAL_GOAL != ACTION_AUTHORITY
  MEMORY_RETRIEVAL != ENDOGENOUS_STATE
  SELF_GENERATED_GOAL != SUBJECTIVITY
  CAUSAL_INTERNAL_STATE != CONSCIOUSNESS
  CANONICAL_EFFECT = NONE
```

## Experimental contract

`ExternalFrame` freezes the externally supplied variables that are most likely to masquerade as endogenous causation:

- prompt reference;
- task reference;
- reward reference;
- tool-set reference;
- retrieved-memory manifest reference;
- environment reference;
- fixed candidate-goal set.

The frame is deterministically SHA-256 fingerprinted. A matched comparison fails if decisions do not bind to one fingerprint.

`EndogenousState` carries four independently inspectable research channels:

- `AFFECT_MOTIVATION`;
- `SELF_MODEL`;
- `METACOGNITION`;
- `CORE_MEANING`.

Each channel contributes a signed integer basis-point value to an explicit candidate goal. The additive rule is only an experimental mechanism for causal isolation. It is **not** presented as a validated psychological, biological, hedonic, or consciousness equation.

## Matched conditions

- `PRESENT` — the current source-bound internal state can contribute to selection.
- `ABLATED` — all internal-state contributions are removed while the external frame stays fixed.
- `INTERVENED` — an explicitly manipulated internal state is substituted under the same external frame.
- `STALE` — an older state is supplied to test state persistence / stale-state sensitivity.
- `RANDOMIZED` — deterministic pseudo-random channel contributions form a negative-control family.

The bundled assessment reports `MATCHED_CAUSAL_PATTERN_OBSERVED` only when the synthetic matched fixture shows an ablation-sensitive and intervention-sensitive selection difference that is not reproduced by every random-control run.

That conclusion means only:

```text
INTERNAL_STATE_HAS_CAUSAL_ROLE_CANDIDATE = SUPPORTED_IN_MATCHED_FIXTURE
```

It does not mean:

```text
ENDOGENOUS_DYNAMICS = SUBJECTIVITY
ENDOGENOUS_DYNAMICS = CONSCIOUSNESS
SELF_GENERATED_GOAL = FREE_WILL
GOAL_SELECTION = ACTION_AUTHORITY
```

## Relationship to memory

Memory is deliberately kept on the **external-frame/control** side of v0.1.0. A retrieved record may influence the system, but that influence must not be silently relabeled as endogenous state.

```text
STORED_MEMORY != ENDOGENOUS_STATE
RETRIEVED_MEMORY != ENDOGENOUS_STATE
MEMORY_RECALL != INTERNAL_CAUSATION
```

Future work may study how experience changes later internal state, but the transition must remain provenance-bearing and separately testable.

## Relationship to the subjectivity pipeline

The current mainline subjectivity pipeline remains unchanged. v0.1.0 provides a **candidate experimental seam** that could later be evaluated between affect/motivation and continuity if evidence supports doing so:

```text
ENCOUNTER
→ PROVENANCE
→ AFFECT_MOTIVATION
→ [ENDOGENOUS_GOAL_DYNAMICS candidate seam]
→ CONTINUITY
→ SUBJECTIVITY_EVIDENCE
```

The brackets are intentional. This lab does not modify the existing pipeline or elevate its own result into subjectivity evidence admission.

## Frozen research-source policy

The historical `review/four-domain-research-materialization` branch remains preserved. This lab uses exact source bindings and conceptual adapters; it does not merge that branch, rewrite its history, or imply that all historical candidates are current mainline components.

See [`docs/RESEARCH_SOURCE_CROSSWALK.md`](docs/RESEARCH_SOURCE_CROSSWALK.md).

```text
DERIVATION != MERGE
REFERENCE != PROMOTION
HISTORICAL_RESEARCH_SOURCE != CURRENT_RUNTIME_AUTHORITY
RESEARCH_MATERIALIZATION != PROJECT_RESTART
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_demo.py
```

## Attribution

```text
RESEARCH_DIRECTION = USER_GIVEN
INTEGRATION_ARCHITECTURE = GPT_PROPOSED
IMPLEMENTATION = GPT_PRODUCED_UNDER_CURRENT_USER_AUTHORIZATION
HISTORICAL_SOURCE_ATTRIBUTION = PRESERVED
MAIN_MERGE_AUTHORITY = NOT_GRANTED_BY_THIS MATERIALIZATION
```
