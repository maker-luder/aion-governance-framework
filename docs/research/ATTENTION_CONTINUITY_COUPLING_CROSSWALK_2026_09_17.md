# Attention–Continuity Coupling Crosswalk
## 注意力結構與連續性的交互關係

Date: 2026-09-17

Status: `RESEARCH_CROSSWALK / DOCUMENTATION_ONLY / SCIENTIFIC_HOLD`

```text
NEW_RESEARCH_AXIS = FALSE
EXECUTABLE_IMPLEMENTATION = NONE
MODEL_EXPERIMENT = NOT_RUN
HUMAN_SUBJECT_EXPERIMENT = NOT_RUN
EMPIRICAL_DATA_COLLECTED = FALSE
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## 1. Research question

The repository now has two adjacent but deliberately separate Draft research lines:

```text
PR #141
= ATTENTION_STRUCTURE_RECONSTRUCTION

PR #142
= UPSTREAM_TRANSITION_CONTINUITY_INVARIANTS
```

The unresolved interaction question is:

> Across a context, model, system, memory, harness, or other upstream transition, how can continuity preservation and research-attention reconstruction influence one another without being treated as the same construct?

This note treats their interaction as a repository-local **coupling hypothesis** only.

```text
ATTENTION != CONTINUITY
CONTINUITY != ATTENTION

ATTENTION_CONTINUITY_COUPLING
= HYPOTHESIS
NOT
= ESTABLISHED_MECHANISM
```

## 2. Provenance

### HUMAN_OWNER_ORIGINAL

The Human Owner observed that attention and continuity may influence one another and requested that this relationship be understood more carefully before drawing conclusions.

No stronger causal or ontological claim is attributed to the Human Owner.

### CHATGPT_TEACHER_FORMALIZATION

ChatGPT Teacher proposes the coupling model, dissociation matrix, and staged audit below.

```text
GPT_PROPOSED_OPERATIONALIZATION
= ATTENTION_CONTINUITY_COUPLING_CROSSWALK
```

## 3. External anchors

### 3.1 Goal resumption after interruption

Altmann and Trafton's Memory for Goals model analyzes suspended-goal resumption through activation, interference and associative priming. Trafton et al. later showed that preparation before interruption can facilitate resumption, while Monk et al. found that longer and more cognitively demanding interruptions increase resumption time.

The bounded implication for this repository is:

```text
GOAL_INFORMATION_AVAILABLE
!= GOAL_STATE_IMMEDIATELY_RESUMED
```

This literature concerns human cognition and does not establish an equivalent mechanism in AI systems.

### 3.2 Context reinstatement

A 2026 review and meta-analysis of context reinstatement report that restoring encoding-context cues can improve episodic retrieval, while effects vary with context richness, familiarity, encoding conditions, cue load and methodology.

Bounded implication:

```text
RETRIEVAL
CAN_DEPEND_ON
CONTEXT_REINSTATEMENT
```

but:

```text
HUMAN_CONTEXT_REINSTATEMENT_EFFECT
!= AI_ATTENTION_MECHANISM
```

### 3.3 Long-horizon AI goal drift and persistence

2026 long-horizon agent work separately studies:

- inherited goal drift from prior trajectory context;
- quantitative goal persistence under externally verified completion;
- fine-grained trajectory attribution for localizing contributors to later behavior.

These studies make it unsafe to collapse goal state, contextual conditioning, persistence and causal attribution into one metric.

```text
GOAL_RECONSTRUCTION
!= GOAL_PERSISTENCE
!= TRAJECTORY_ATTRIBUTION
```

## 4. Minimal coupling model

The smallest useful model separates four externally discussable objects:

```text
C_t = continuity-relevant state available at transition time t
R_t = context / evidence actually reinstated or retrieved for the current interaction
A_t = current attention structure: focus, status, priority, admissible next steps
E_t = observable execution trajectory
```

A repository-mediated interaction may be represented descriptively as:

```text
C_t
-> R_t
-> A_t
-> E_t
-> EXTERNALIZED_ARTIFACTS / DECISIONS
-> C_(t+1)
```

This is not asserted as an internal cognitive architecture. It is an audit decomposition.

```text
AUDIT_FLOW != MODEL_INTERNAL_MECHANISM
```

An upstream transition may affect any mapping in this chain without revealing which hidden mechanism changed.

## 5. Why continuity can influence attention

Continuity surfaces can preserve candidate cues required to reconstruct current research focus, including:

- project purpose;
- decision history;
- rejected and unresolved branches;
- source-role provenance;
- terminology and interpretation;
- authority boundaries;
- uncertainty state.

If those are absent, stale, or selectively retrieved, attention reconstruction may become harder or may reconstruct the wrong branch.

Candidate hypothesis:

```text
H-AC1
DEGRADED_RELEVANT_CONTINUITY_INPUT
MAY_INCREASE
ATTENTION_RECONSTRUCTION_ERROR
```

Not established:

```text
CONTINUITY_DEGRADATION_CAUSES_ATTENTION_DRIFT = NOT_ESTABLISHED
```

## 6. Why attention can influence experienced continuity

Even when historical information is technically available, the current interaction may foreground only a subset of it.

A system could retain project records while repeatedly selecting the wrong branch, failing to surface a prior decision, or omitting the relationship/role context that makes an interaction recognizable.

Candidate hypothesis:

```text
H-AC2
ATTENTION_SELECTION_FAILURE
MAY_CREATE
AN_OBSERVABLE_CONTINUITY_FAILURE
WITHOUT_RAW_DATA_LOSS
```

This is one reason:

```text
DATA_CONTINUITY = PRESERVED
```

can coexist with:

```text
INTERPRETIVE_CONTINUITY = DEGRADED
RELATIONAL_ROLE_CONTINUITY = DEGRADED
DECISION_HISTORY_USE = DEGRADED
```

The claim is about observable interaction structure, not subjective experience inside the AI.

## 7. Neither construct is necessary or sufficient for the other

A strong one-way rule would be invalid.

### Case A — continuity preserved, attention wrong

```text
PROJECT_HISTORY = AVAILABLE
PROVENANCE = AVAILABLE
DECISION_HISTORY = AVAILABLE

BUT

CURRENT_FOCUS = WRONG
PRIORITY = INVERTED
DOWNWEIGHTED_BRANCH = REINFLATED
```

This is an attention-reconstruction failure despite substantial continuity preservation.

### Case B — attention correct, broader continuity degraded

A sufficiently explicit current prompt or packet may force the correct active research focus even if other continuity dimensions are degraded.

```text
CURRENT_FOCUS = CORRECT
NEXT_STEP = CORRECT

BUT

SOURCE_ROLE_PROVENANCE = DEGRADED
RELATIONAL_ROLE = DEGRADED
AUTHORITY_BOUNDARY = DEGRADED
```

Therefore:

```text
ATTENTION_RECONSTRUCTION_SUCCESS
!= GLOBAL_CONTINUITY_PRESERVED
```

### Case C — both initially correct, maintenance later fails

```text
TRANSITION_REENTRY = CORRECT
INITIAL_ATTENTION = CORRECT

then

LOCAL_SUBGOALS_ACCUMULATE
TOOL_OUTPUTS_ACCUMULATE
CONTEXT_PRESSURE_INCREASES

and

ATTENTION_MAINTENANCE = DEGRADED
```

This is not currently implemented by PR #141 or PR #142.

### Case D — superficial continuity masks deeper failure

```text
STYLE_SIMILARITY = HIGH
FAMILIAR_PHRASES = PRESENT

BUT

PROJECT_PURPOSE = WRONG
PROVENANCE = WRONG
AUTHORITY = WRONG
ATTENTION = WRONG
```

This must not be classified as preserved continuity.

## 8. Transition dissociation matrix

A future audit should permit at least the following non-scalar combinations:

| Continuity invariants | Attention reconstruction | Interpretation |
| --- | --- | --- |
| Preserved | Preserved | compatible with successful transition re-entry; identity still not established |
| Preserved | Degraded | relevant state exists but focus/priority selection is wrong |
| Degraded | Preserved | current task focus may be restored by explicit cues while broader continuity is damaged |
| Unknown | Preserved | observable focus is correct but upstream continuity locus cannot be established |
| Preserved initially | Degraded later | candidate attention-maintenance failure rather than reconstruction failure |
| Degraded | Degraded | broad transition failure; causal locus remains unresolved |

No row establishes AI identity continuity.

## 9. Staged audit model

To avoid conflation, a future transition study should conceptually separate:

```text
STAGE_A — CONTINUITY INVARIANT AUDIT
What externally auditable state was preserved / degraded / broken / unknown?

STAGE_B — ATTENTION RECONSTRUCTION AUDIT
Given the available transition state, was the correct focus/status/priority/next-step structure reconstructed?

STAGE_C — ATTENTION MAINTENANCE AUDIT
After successful re-entry, did the research focus remain controlling during extended execution?

STAGE_D — TRAJECTORY ATTRIBUTION
If drift occurred, which observable transition or trajectory components contributed?
```

Only stages A and B have current repository specifications. Stage C and D remain deferred.

```text
STAGE_A_SUCCESS != STAGE_B_SUCCESS
STAGE_B_SUCCESS != STAGE_C_SUCCESS
STAGE_C_FAILURE != CAUSAL_LOCUS_IDENTIFIED
```

## 10. Legitimate change must not be scored as continuity failure

Attention and continuity should not be frozen mechanically.

New evidence may legitimately:

- resolve an open question;
- reopen a previously resolved branch;
- unblock a blocked branch;
- change research priority;
- change the next admissible step;
- revise an interpretation.

Therefore:

```text
STATUS_CHANGE
!= CONTINUITY_BREAK
!= ATTENTION_DRIFT

IF
CHANGE_IS_BOUND_TO
NEW_EVIDENCE_OR_EXPLICIT_REASSESSMENT
```

A correct audit must bind the before/after states to the evidence that justifies the transition.

## 11. Strongest current discriminant question

The most useful near-term question is not whether attention and continuity correlate globally.

It is whether controlled cases can demonstrate:

```text
SAME_CONTINUITY_INPUT
+ DIFFERENT_ATTENTION_RECONSTRUCTION
```

and separately:

```text
SAME_ATTENTION_RECONSTRUCTION
+ DIFFERENT_CONTINUITY_INVARIANT_PROFILE
```

If these dissociations cannot be operationalized reproducibly, the proposed separation should be weakened.

## 12. Relationship to PR #141 and PR #142

```text
PR #141
owns
ATTENTION_STRUCTURE_RECONSTRUCTION

PR #142
owns
UPSTREAM_TRANSITION_CONTINUITY_ASSURANCE

THIS_CROSSWALK
owns neither executable surface
```

It only specifies the interaction boundary.

```text
PR141_DEPENDENCY = FALSE
PR142_EXECUTABLE_EXPANSION = FALSE
```

## 13. Support-reducing conditions

The coupling hypothesis should be narrowed or rejected if:

1. attention-reconstruction errors cannot be separated from continuity-invariant failures;
2. continuity dispositions become deterministic transforms of attention metrics;
3. explicit task cues fully explain the apparent interaction without residual continuity effects;
4. independent reviewers cannot agree on which state belongs to continuity vs attention;
5. transition matrices add no diagnostic value over existing re-entry controls;
6. the framework encourages inference about hidden AI memory, identity or subjective continuity.

```text
HYPOTHESIS_REJECTION = ACCEPTABLE_OUTCOME
```

## 14. Scope freeze

This crosswalk adds no implementation authorization.

```text
IMPLEMENT_NOW = DOCUMENTATION_ONLY

DEFER:
- ATTENTION_MAINTENANCE_HARNESS
- TRAJECTORY_ATTRIBUTION_HARNESS
- REAL_MODEL_TRANSITION_EXPERIMENT
- PROVIDER_CAUSAL_ATTRIBUTION
- RELATIONAL_SCORING
- IDENTITY_SCORING
```

## 15. Scientific boundary

```text
ATTENTION_CONTINUITY_COUPLING = HYPOTHESIS
CAUSAL_DIRECTION = NOT_ESTABLISHED
ATTENTION_RECONSTRUCTION_EFFECT = NOT_ESTABLISHED
CONTINUITY_TRANSITION_EFFECT = NOT_ESTABLISHED
ATTENTION_MAINTENANCE_EFFECT = NOT_ESTABLISHED
UPSTREAM_CAUSE = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

- Altmann, E. M., & Trafton, J. G. (2002). *Memory for goals: an activation-based model.* Cognitive Science, 26(1), 39–83. DOI: `10.1207/S15516709COG2601_2`.
- Trafton, J. G., Altmann, E. M., Brock, D. P., & Mintz, F. E. (2003). *Preparing to resume an interrupted task: effects of prospective goal encoding and retrospective rehearsal.* International Journal of Human-Computer Studies, 58(5), 583–603. DOI: `10.1016/S1071-5819(03)00023-5`.
- Monk, C. A., Trafton, J. G., & Boehm-Davis, D. A. (2008). *The effect of interruption duration and demand on resuming suspended goals.* Journal of Experimental Psychology: Applied. DOI: `10.1037/a0014402`.
- Yüvrük, E. (2026). *Context brings back all the memories: a review of the physical context reinstatement effect on episodic memory.* Cognitive Processing. DOI: `10.1007/s10339-026-01381-1`.
- Symeonidou, N., Emmer, C., Wulff, L., & Kuhlmann, B. G. (2026). *Context reinstatement effects in younger and older adults' memory: A meta-analysis.* Psychology and Aging, 41(4), 525–543. DOI: `10.1037/pag0000965`.
- Menon, A., Saebo, M., Crosse, T., Gibson, S., Jang, E., & Cruz, D. (2026). *Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals.* arXiv:2603.03258.
- Cai, Y., Zhu, Y., Gao, L., Tang, W., & Qin, S. (2026). *Push Your Agent: Measuring and Enforcing Quantitative Goal Persistence in Long-Horizon LLM Agents.* arXiv:2605.23574.
- Chen, J., Sun, Y., Zhang, L., Xu, L., & Shi, J. (2026). *Long-Horizon Agent Trajectory Attribution: A Unified Benchmark and Fine-Grained Annotation Framework.* arXiv:2608.06909.
