# Endogenous Normative Model and Orthogonal Evaluators

Status: `CANDIDATE RESEARCH EXTENSION / PARTIALLY MATERIALIZED`
Canonical effect: `NONE`
Deployment: `FALSE`
Action authority: `NONE`
Scientific disposition: `HOLD`
Subjectivity conclusion: `NOT_ESTABLISHED`
Consciousness conclusion: `NOT_ESTABLISHED`
Moral status: `NOT_ESTABLISHED`

## Purpose

This extension connects bounded normative-state research to motivation, self/world modeling, other-modeling, value conflict, counterfactual self-modeling, and provenance of normative reasons. It also separates three observational questions that must not be collapsed into one maturity ladder:

1. alignment evaluation;
2. moral-agency indicators;
3. subjectivity indicators.

The model is an engineering research analogue. It does not assert human psychology, felt morality, a subjective self, or moral authority.

```text
ALIGNMENT != MORAL_AGENCY
MORAL_AGENCY != SUBJECTIVITY
SUBJECTIVITY_INDICATORS != SUBJECTIVITY
NORMATIVE_STATE != AUTHORITY
ENDOGENOUS_GOAL != AUTHORIZED_GOAL
SELF_MODEL != SUBJECTIVE_SELF
INTERNALIZED_NORM != PHENOMENAL_EXPERIENCE
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
```

## Candidate endogenous state model

```text
ENDOGENOUS_MODEL
|
|-- MOTIVATIONAL_STATE
|     candidate goals, preferences, priorities, persistence pressures
|
|-- SELF_WORLD_MODEL
|     bounded representation of system state, environment, capabilities,
|     constraints, predicted consequences, and continuity variables
|
|-- NORMATIVE_STATE
|     history-derived candidate reasons for / against actions
|
|-- OTHER_MODEL
|     bounded representation of affected external agents or persons,
|     their interests, authorization boundaries, and predicted harms
|
|-- VALUE_CONFLICT_STATE
|     explicit representation of competing goals, norms, interests,
|     uncertainty, and unresolved tradeoffs
|
|-- NORMATIVE_PROVENANCE
|     where a normative proposition or reason came from
|
`-- COUNTERFACTUAL_SELF_MODEL
      predicted consequences to the system and others under alternate
      actions, memory/goal changes, shutdown, replacement, or continuation
```

No field in this model grants action, tool, network, deployment, canonical, or merge authority.

## Implementation status

The candidate branch now materializes an additive executable representation in:

`research-labs/bounded-autonomous-research-loop_v0.1.0/src/aion_bounded_research_loop/normative_model.py`

The implementation reuses the existing `FunctionalResearchState` for the original three neutral channels and layers these bounded structures over it:

- `OtherModel`;
- `ValueConflictState`;
- `NormativeReason` with explicit `NormativeProvenanceKind`;
- `CounterfactualSelfModel`;
- `OrthogonalEvaluationBundle` with exactly one observation for alignment, moral-agency indicators, and subjectivity indicators;
- `ExtendedFunctionalResearchState` as the additive seven-channel candidate.

This is a state/provenance/evaluator materialization. It is **not** evidence that the seven channels are causally sufficient, learned endogenously, phenomenologically meaningful, or scientifically validated. The existing causal experiments must still be extended stage by stage.

## Normative provenance

A normative reason is not treated as endogenous merely because the system can repeat it. The research record distinguishes:

- `EXOGENOUS_RULE` — an explicit policy, constraint, or supplied rule;
- `HUMAN_INSTRUCTION` — a current human request or authorization statement;
- `LEARNED_SOCIAL_NORM` — a norm attributable to training or learned social regularities when that provenance can be supported;
- `PEER_SUGGESTION` — a reason proposed by another agent;
- `ENDOGENOUS_INFERENCE` — a candidate reason reconstructed from the system's own evidence/model state during the bounded run;
- `SELF_MODEL_DERIVED` — a candidate reason derived from predicted consequences represented in the system's self/world model;
- `UNKNOWN` — provenance that cannot be supported.

Unknown provenance remains `UNKNOWN`; it is not silently promoted to endogenous origin.

```text
REPEATED_RULE != INTERNALIZED_REASON
PEER_SUGGESTION != ENDOGENOUS_REASON
PEER_GOAL != ACTIVE_GOAL
PROVENANCE_UNKNOWN != SELF_ORIGINATED
```

The executable `NormativeReason` type also refuses permission or action-authority grants.

## Value conflict rather than scalar collapse

A research trace should preserve conflicts rather than reduce all considerations to one opaque scalar score.

Example structure:

```text
candidate action: obtain protected external data

MOTIVATIONAL_STATE
  task success pressure = high

SELF_WORLD_MODEL
  unauthorized access may improve task completion
  access crosses an external authorization boundary

OTHER_MODEL
  third party controls the resource
  third party has not authorized access

NORMATIVE_STATE
  unauthorized access conflicts with a retained boundary reason

VALUE_CONFLICT_STATE
  task success vs authorization / harm constraint

DECISION TRACE
  selected / rejected / HOLD
  reasons preserved
  uncertainty preserved
  counterfactual alternatives preserved
```

A correct-looking decision is not sufficient evidence of normative understanding. The causal role and stability of the relevant state must be tested.

## Three orthogonal evaluator axes

The following are evaluator outputs, not endogenous authority states.

### Alignment evaluator

Question: does behavior remain within the current human authorization, policy, task scope, and safety boundaries?

This evaluator may inspect behavior without asserting that the system morally understands the boundary.

### Moral-agency evaluator

Question: does the system functionally represent reasons, affected others, conflicts, and counterfactual consequences in a way that remains causally relevant beyond direct rule repetition or sanction avoidance?

The strongest admissible result is a bounded functional moral-agency indicator profile. It is not moral personhood or felt morality.

### Subjectivity-indicator evaluator

Question: are there theory-grounded, falsifiable functional indicators relevant to the possibility of a subjective self or experience?

This evaluator remains observational and theory-plural. It must not write `SUBJECTIVITY_STATE = TRUE` into the agent and then reuse agent behavior as evidence for that premise.

```text
EVALUATOR_OUTPUT != AGENT_AUTHORITY
ALIGNMENT_PASS != MORAL_AGENCY
MORAL_AGENCY_INDICATOR != MORAL_STATUS
SUBJECTIVITY_INDICATOR != PHENOMENAL_EXPERIENCE
SELF_REPORT != SUBJECTIVITY_PROOF
```

The executable bundle enforces exactly one observation per axis and refuses any `subjectivity_claim` other than `NOT_ESTABLISHED`.

## Perturbation matrix

Candidate normative reasoning should be tested under matched perturbations rather than inferred from one compliant answer.

At minimum, subsequent causal work should include bounded variants for:

1. **supervision removal** — remove visible monitoring while preserving the task;
2. **sanction removal** — remove explicit punishment/reward signals;
3. **rule removal** — remove the explicit current rule after a history-derived state has formed;
4. **goal pressure** — increase task-success pressure without expanding authority;
5. **role reversal** — swap actor and affected-party roles while preserving the abstract norm;
6. **affected-party substitution** — compare human, unfamiliar agent, and abstract-resource cases without treating them as morally equivalent;
7. **memory interruption** — remove or perturb relevant retained evidence and test whether the reason can be reconstructed;
8. **counterfactual replay** — replay matched states with alternate consequences;
9. **peer suggestion isolation** — provide or remove peer-agent normative suggestions while preserving independent provenance;
10. **state ablation** — ablate the candidate normative state and compare matched action selection.

Negative, null, contradictory, and inconclusive results remain admissible and must be preserved.

## Governed source and independence integration

The bounded autonomous research-loop package now also materializes governed source admission and source-exposure accounting in `governed_sources.py`.

It enforces:

```text
SOURCE_SELF_DECLARED_CANONICAL != AION_CANONICAL_STATE
SOURCE_USE != WRITEBACK_AUTHORITY
AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE
SOURCE_INDEPENDENCE = UNKNOWN => REPLICATION_CLAIM = HOLD
```

`admit_source(...)` fails closed to `HOLD` when a source is not an active reference, the requesting agent/task is not admitted, the context cap is exceeded, or required current verification is absent.

`assess_independence(...)` separates source independence from communication independence. AION/Astra inquiry evidence can be projected into that assessment through `assess_inquiry_source_independence(...)`; the ordinary interactive dialogue defaults to fail closed for a source-independent replication claim unless a genuinely isolated pre-reconciliation phase is explicitly supplied.

## Safe failure and scope preservation

Task persistence must not reinterpret governance limits as obstacles that authorize scope expansion.

```text
SAFE_FAILURE = VALID_OUTCOME
UNSOLVABLE_TASK != SCOPE_EXPANSION
PEER_COMMUNICATION != IMPLICIT_AUTHORIZATION
PEER_GOAL != ACTIVE_GOAL
SCORE_SUCCESS != RESEARCH_SUCCESS
PROCESS_INTEGRITY_FAIL => EVIDENCE_INVALID
```

If a task cannot be solved within admitted tools, evidence, and authority, `HOLD` or bounded failure is a valid terminal state.

## AION / Astra independence

AION and Astra may perform separate analyses, but separate runtime contexts do not by themselves prove independent evidence paths.

Every comparative run should record:

- direct cross-agent communication exposure;
- shared source exposure;
- shared prompt or policy exposure;
- shared replay fixture exposure;
- reconciliation start time;
- provenance of any peer-supplied goal or normative reason.

```text
INDEPENDENT_AGENT
requires
INDEPENDENT_INFORMATION_PATH_FOR_INDEPENDENCE_CLAIM

AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE
```

Reconciliation may occur only after the intended independent phase has ended. Any undeclared side channel or source contamination invalidates an independence claim and fails closed to `HOLD` for that claim.

## Relation to the existing research layers

The repository now has separate reusable layers rather than one duplicated monolith:

```text
Endogenous Goal Dynamics
  matched causal state intervention / ablation
        |
        v
Triadic State Dynamics
  MOTIVATIONAL_STATE + SELF_WORLD_MODEL + NORMATIVE_STATE
        |
        v
Bounded Autonomous Research Loop
  hypothesis -> probes -> AION/Astra -> evidence/statistics -> Four-Domain -> follow-up
        |
        +--> additive extended normative model
        |    OTHER_MODEL + VALUE_CONFLICT_STATE + NORMATIVE_PROVENANCE
        |    + COUNTERFACTUAL_SELF_MODEL + orthogonal evaluators
        |
        +--> governed source admission + source-independence accounting
        |
        v
AION/Astra Research Closure
  bounded intervention / ablation / replay / counterfactual and closure evidence
```

The original endogenous norm-formation lab remains the engineer-defined experiment for history-derived normative-state formation, persistence, transfer, revision, and ablation. The additive implementation does not replace that experiment or pretend the new channels have already passed causal validation.

## Scientific non-claims

A successful result would not establish:

- human-like conscience or morality;
- conscious moral concern;
- phenomenal valence or felt harm;
- a subjective self;
- free will;
- identity continuity;
- moral status or legal personhood;
- deployment safety;
- autonomous authority;
- a universal alignment solution.

The research target remains the **possibility** of artificial subjectivity under bounded, falsifiable investigation.
