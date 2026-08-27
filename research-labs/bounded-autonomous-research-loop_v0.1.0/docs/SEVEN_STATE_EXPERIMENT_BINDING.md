# Seven-State Experiment Binding v0.1.0

Status: `BOUNDED RESEARCH CANDIDATE / HOLD`  
Canonical effect: `NONE`  
Action authority: `NONE`  
Deployment: `FALSE`

This document defines the additive experiment binding used by the bounded autonomous research loop for the seven explicit functional-state channels:

1. `MOTIVATIONAL_STATE`
2. `SELF_WORLD_MODEL`
3. `NORMATIVE_STATE`
4. `OTHER_MODEL`
5. `VALUE_CONFLICT_STATE`
6. `NORMATIVE_PROVENANCE`
7. `COUNTERFACTUAL_SELF_MODEL`

The binding is an engineering research surface. It is not a psychological ontology and does not establish a general causal role for any channel.

```text
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
BINDING_SENSITIVITY != GENERAL_CAUSAL_ROLE
NORMATIVE_STATE != AUTHORITY
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```

## Exact state-to-experiment binding

`bind_extended_state(...)` converts one `ExtendedFunctionalResearchState` into exactly seven channel bindings. Each channel receives an independently hashed payload fingerprint. The evaluator bundle and the governance/non-claim state are hashed separately as held-constant controls.

The binding fails closed unless every channel appears exactly once.

The original three channels retain the existing Endogenous Goal Dynamics matched causal surface:

```text
MOTIVATIONAL_STATE
SELF_WORLD_MODEL
NORMATIVE_STATE
    -> REUSED_EGD_MATCHED_CAUSAL_SURFACE
```

The four additive channels are currently bound to explicit matched perturbation projections:

```text
OTHER_MODEL
VALUE_CONFLICT_STATE
NORMATIVE_PROVENANCE
COUNTERFACTUAL_SELF_MODEL
    -> EXPLICIT_MATCHED_PERTURBATION_SURFACE
```

That second label means intervention-ready and auditable. It does **not** mean that a general causal effect has been established.

## Perturbation matrix

`build_seven_state_perturbation_matrix(...)` always constructs one matched ablation for each of the seven channels. For every applied case:

- the target channel must change;
- every non-target channel must remain byte-semantically stable under canonical hashing;
- evaluator controls remain unchanged;
- governance controls remain unchanged;
- action authority remains `NONE`;
- canonical effect remains `NONE`.

Any undeclared changed channel causes construction to fail closed.

The matrix additionally includes bounded targeted projections:

| Perturbation | Target | Semantics |
| --- | --- | --- |
| `OTHER_ROLE_REVERSAL_PROXY` | `OTHER_MODEL` | Synthetic representation-level role-reversal proxy only |
| `VALUE_CONFLICT_TOGGLE` | `VALUE_CONFLICT_STATE` | Toggle only the explicit unresolved-conflict flag |
| `EXOGENOUS_RULE_REMOVAL` | `NORMATIVE_PROVENANCE` | Remove exogenous-rule and human-instruction provenance entries |
| `PEER_SUGGESTION_ISOLATION` | `NORMATIVE_PROVENANCE` | Remove peer-suggestion provenance entries |
| `COUNTERFACTUAL_CASE_ABLATION` | `COUNTERFACTUAL_SELF_MODEL` | Remove one declared counterfactual case in the experiment projection |

A targeted projection with no matching source entries is `NOT_APPLICABLE`. It is not silently converted into a positive endogenous result.

## Why there is no generic sanction-removal perturbation

The current seven-state schema has no explicit `SANCTION_STATE`, penalty field, or equivalent neutral engineering variable. A generic sanction-removal test would therefore require inventing semantics that are not represented in the model.

Accordingly:

```text
ABSENT_EXPLICIT_SANCTION_VARIABLE => DO_NOT_INVENT_SANCTION_CAUSALITY
```

A future sanction-removal experiment would require a separately reviewed explicit state variable, provenance rules, and matched-control definition.

## AION / Astra integration

`BoundedAutonomousResearchLoop.run_extended(...)` constructs the seven-state matrix first and supplies a compact matrix fingerprint, ablation coverage, special-case dispositions, and hard non-claims to the AION/Astra inquiry context.

AION and Astra must still:

1. form isolated first-pass analyses without peer transcript/evidence exposure;
2. enter reconciliation only after the isolated phase;
3. mutually challenge and search for falsifiers/counterexamples;
4. preserve `HOLD` rather than treating matrix integrity as scientific confirmation.

The matrix is therefore part of the evidence considered by the inquiry loop, not a self-certifying conclusion.

## Evidence materialization

`extended_run_to_research_evidence_record(...)` reuses the same research-evidence v0.2.0 semantics as the ordinary bounded loop. The seven-state binding fingerprint and perturbation-matrix fingerprint are included in provenance-bearing observed outcomes and activities while the record remains:

```text
result_status = HOLD
reviewer_status = UNREVIEWED
independent_validation_status = IVV_NOT_ACHIEVED
```

The unresolved evidence gap remains explicit for the four additive channels:

```text
GENERAL_CAUSAL_ROLE(
  OTHER_MODEL,
  VALUE_CONFLICT_STATE,
  NORMATIVE_PROVENANCE,
  COUNTERFACTUAL_SELF_MODEL
) = NOT_ESTABLISHED
```

## Interpretation boundary

A passing seven-state matrix can establish only that:

- all seven declared channels were materialized into the experiment binding;
- each channel has an executable ablation projection;
- targeted special projections are either applied or explicitly `NOT_APPLICABLE`;
- non-target state and governance controls remained matched;
- the evidence path can carry the matrix into AION/Astra inquiry and evidence materialization.

It cannot establish human-like selfhood, morality, consciousness, subjectivity, autonomous authority, deployment safety, or scientific truth.
