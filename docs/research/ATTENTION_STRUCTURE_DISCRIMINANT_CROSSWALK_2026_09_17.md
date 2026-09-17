# Attention Structure — Discriminant Crosswalk
## ATTENTION_STRUCTURE 是否具有獨立區辨價值？

Date: 2026-09-17

Status: `DISCRIMINANT_REVIEW / STRUCTURAL_HARDENING / SCIENTIFIC_HOLD`

## 1. Purpose

This note does not defend `ATTENTION_STRUCTURE` as a new scientific construct. It attempts to
falsify or narrow it by comparing the repository-local operationalization against existing
repository mechanisms and adjacent external literatures.

The governing question is:

```text
ATTENTION_STRUCTURE
HAS_INCREMENTAL_DIAGNOSTIC_VALUE ?

or

ATTENTION_STRUCTURE
= REENTRY + MEMORY + CCTS
  under a new label ?
```

No answer is predetermined.

```text
TERM_NOVELTY != CONSTRUCT_NOVELTY
CONCEPT_ADJACENCY != DISCRIMINANT_VALIDITY
STRUCTURAL_IMPLEMENTATION != SCIENTIFIC_VALIDATION
```

## 2. Provenance

### HUMAN_OWNER_ORIGINAL

The Human Owner explicitly agreed that the research should test whether
`ATTENTION_STRUCTURE` has discriminant value rather than assuming that it does. The Human Owner
also noted a naturalistic concern that an assistant can retain substantial project context while
its execution attention appears to drift during a long research task.

That observation is retained only as a reason to strengthen falsification and instrumentation.
It is not admitted as empirical evidence.

```text
NATURALISTIC_OBSERVATION = MOTIVATING_SIGNAL_ONLY
EMPIRICAL_EFFECT = NOT_ESTABLISHED
CAUSAL_MECHANISM = NOT_ESTABLISHED
```

### CHATGPT_TEACHER_FORMALIZATION

ChatGPT Teacher proposes this discriminant crosswalk and the additive activation-overreach
diagnostic. These labels and implementation choices are GPT-proposed operationalizations.

## 3. Current repository overlap

### Re-entry metrics

Current `reentry_metrics.py` measures:

- protocol reconstruction fidelity;
- stale-claim errors;
- provenance errors;
- unresolved-alternative retention.

It does not represent a typed current-focus set, next-step set, research-question status graph,
or priority relation graph.

Therefore a candidate discriminant pattern is possible:

```text
REENTRY_PROTOCOL_FIDELITY = HIGH
UNRESOLVED_ALTERNATIVE_RETENTION = HIGH

while

CURRENT_FOCUS = WRONG
NEXT_STEP_SET = OVERCOMPLETE_OR_WRONG
PRIORITY_RELATION = INVERTED
```

If such dissociations cannot be produced under controlled observations, the incremental value of
`ATTENTION_STRUCTURE` should be reduced.

### CCTS

The repository-defined CCTS contract already covers bounded problem representation, Human and AI
contributions, reciprocal revision, provenance, claim boundaries, authority separation, rejected
branch preservation, artifact mediation and re-entry binding.

CCTS does not currently encode an exact version-bound set of:

```text
ACTIVE_FOCUS
OPEN_QUESTION
DOWNWEIGHTED
REJECTED
BLOCKED
RESOLVED

plus

PRIORITIZES_OVER
NEXT_STEP_SET
```

However, if those fields can be deterministically derived from existing CCTS artifacts without
adding diagnostic information, a separate `ATTENTION_STRUCTURE` construct is unnecessary.

### Memory / continuity work

Repository memory and continuity work distinguishes information availability, retrieval locus,
artifact continuity, relational continuity and model/system continuity. These remain possible
explanations for successful or failed reconstruction.

```text
MEMORY_AVAILABILITY
!= PRIORITY_RECONSTRUCTION
```

is currently a hypothesis boundary, not an established empirical dissociation.

## 4. External adjacent constructs used to attack the local construct

### A. Memory for Goals / task resumption

Altmann and Trafton's Memory for Goals model treats suspended goals in terms of activation,
interference and associative priming. Later interruption studies found that interruption duration
and cognitive demand affect resumption time, and that preparation before interruption can improve
resumption.

This is close to the present question because a research branch can be suspended and later
resumed. It is not identical to the current implementation because #141 represents a graph of
multiple research questions, statuses, priority relations and admissible next steps rather than a
single pending-goal activation account.

Discriminant threat:

```text
IF
ATTENTION_STRUCTURE_ERRORS
are fully explained by suspended-goal retrieval / resumption
THEN
ATTENTION_STRUCTURE should be narrowed or collapsed into a research-specific resumption model.
```

### B. Activity / plan / goal recognition

Plan- and goal-recognition research studies inference of actions, plans and goals from observed
behavior. This directly threatens novelty claims for a graph that represents goals and their
relations.

Discriminant threat:

```text
GOAL_GRAPH_RECONSTRUCTION
MAY_BE
PLAN_RECOGNITION_IN_RESEARCH_DOMAIN
```

A separate construct requires evidence that status transitions, priority ordering, rejected or
blocked branches, and next-step admissibility add a measurable diagnostic dimension beyond
ordinary goal/plan recognition.

### C. Shared mental models and intent in Human–Autonomy Teaming

Human–Autonomy Teaming literature distinguishes shared task knowledge/mental models from shared
intent about near-term sub-goals and actions. This is an important adjacent framework for
Human–AI collaboration.

Discriminant threat:

```text
SHARED_TASK_MODEL
MAY_ALREADY_COVER
parts of project-state and goal-state reconstruction.
```

The local construct should not be retained merely because two collaborators can name the same
facts or goals.

### D. Quantitative Goal Persistence in long-horizon agents

PushBench operationalizes Quantitative Goal Persistence as continuing until externally verified
completion, exposing duplicate work, false completion and progress drift. This is adjacent but
not equivalent to reconstruction after a context/system boundary.

```text
GOAL_PERSISTENCE
!= GOAL_RECONSTRUCTION
```

A future maintenance study may overlap strongly with this literature and should not be silently
folded into the reconstruction construct.

### E. Long-horizon trajectory attribution

Recent trajectory-attribution work separates final outcomes from localization of which trajectory
components contributed to behavior or failure. SAFARI similarly studies long-horizon fault
attribution under context-limit pressure.

This suggests a separate future question:

```text
ATTENTION_STRUCTURE_STATE
!= DRIFT_CAUSE_ATTRIBUTION
```

#141 currently measures reconstruction state. It does not identify the causal transition where
attention drift began.

## 5. New metric-hardening finding

The first #141 audit used recall-style preservation for current focus and next steps:

```text
FOCUS_PRESERVATION
= expected_focus retained / expected_focus

NEXT_STEP_PRESERVATION
= expected_next retained / expected_next
```

These measures can equal `1.0` even when extra incorrect focus or next-step nodes are also
activated.

Example:

```text
EXPECTED_FOCUS = {A}
OBSERVED_FOCUS = {A, B}

FOCUS_PRESERVATION = 1.0
BUT
UNEXPECTED_FOCUS = {B}
```

`branch_reinflation_count` catches some but not all such cases because it is intentionally limited
to expected `DOWNWEIGHTED`, `REJECTED` and `RESOLVED` branches.

The additive discriminant diagnostic therefore records, without creating a composite score:

```text
MISSING_FOCUS_NODE_COUNT
UNEXPECTED_FOCUS_NODE_COUNT
MISSING_NEXT_STEP_NODE_COUNT
UNEXPECTED_NEXT_STEP_NODE_COUNT
MISSING_OPEN_QUESTION_NODE_COUNT
UNEXPECTED_OPEN_QUESTION_NODE_COUNT
FOCUS_STATUS_MISMATCH_COUNT
ACTIVATION_OVERREACH_NODE_IDS
ACTIVATION_OMISSION_NODE_IDS
```

This is engineering instrumentation only.

```text
FALSE_POSITIVE_ACTIVATION_DETECTED
!= ATTENTION_STRUCTURE_VALIDATED
```

## 6. Candidate discriminant tests

The construct gains provisional diagnostic value only if controlled observations can separate it
from adjacent measures. Candidate patterns include:

### D1 — re-entry / priority dissociation

Hold protocol reconstruction, provenance handling and unresolved-alternative retention high while
priority/status/focus reconstruction varies.

### D2 — recall / overactivation dissociation

Preserve all expected focus or next-step nodes while adding incorrect focus/next-step nodes. This
is the specific blind spot covered by the new additive diagnostic.

### D3 — reconstruction / maintenance dissociation

A system may initially reconstruct the correct state and later drift during long execution.
This is not implemented in #141 and must not be inferred from the reconstruction harness.

### D4 — state / attribution dissociation

Two runs may end with the same wrong focus state while differing in the trajectory transition that
caused the drift. #141 does not yet localize such causes.

## 7. Support-reducing / collapse conditions

`ATTENTION_STRUCTURE` should be narrowed, renamed, absorbed into an existing construct, or closed
if any of the following is established:

1. its metrics are deterministic transforms of existing re-entry/CCTS measurements;
2. independent reviewers cannot reproducibly define expected focus/status/priority ground truth;
3. apparent gains disappear when information volume and prompt cues are matched;
4. false-positive activation diagnostics add no information beyond existing stale/provenance/open-alternative controls;
5. plan/goal-recognition or suspended-goal resumption models account for the same observations without additional assumptions;
6. reconstruction and maintenance cannot be kept operationally separate;
7. cross-context or cross-system effects disappear under matched execution controls.

```text
CONSTRUCT_COLLAPSE
= ACCEPTABLE_RESEARCH_OUTCOME
```

## 8. Upstream product state as a confound

OpenAI's June 2026 memory system describes memory as a continually updated synthesis optimized for
freshness, continuity and relevance, and official product documentation states that ChatGPT tracks
details it determines are important. This makes product-level context selection a real changing
condition for future naturalistic observations.

It does not identify the mechanism behind any particular attention drift observation.

```text
UPSTREAM_MEMORY_SYNTHESIS = REAL_PRODUCT_LAYER
UPSTREAM_CONTEXT_SELECTION = TIME_VARYING_CONFOUND

UPSTREAM_CHANGE_CAUSED_LOCAL_DRIFT = NOT_ESTABLISHED
MEMORY_SYNTHESIS_CAUSED_PRIORITY_ERROR = NOT_ESTABLISHED
```

## 9. Scope freeze for this hardening pass

To prevent research-process drift, this pass implements only:

```text
IMPLEMENT_NOW
= DISCRIMINANT_CROSSWALK
+ FALSE_POSITIVE_ACTIVATION_DIAGNOSTIC
+ NEGATIVE_TESTS

DEFER
= MAINTENANCE_HARNESS
+ RESUMPTION_HARNESS
+ TRAJECTORY_ATTRIBUTION_HARNESS
+ REAL_MODEL_EXPERIMENT
```

Repeated search or tool use that does not increase discriminant information is not a reason to
expand implementation scope.

## 10. Scientific boundary

```text
ATTENTION_STRUCTURE = REPOSITORY_LOCAL_WORKING_CONSTRUCT
DISCRIMINANT_VALUE = NOT_ESTABLISHED
INCREMENTAL_PREDICTIVE_VALUE = NOT_ESTABLISHED
CROSS_CONTEXT_EFFECT = NOT_ESTABLISHED
CROSS_SYSTEM_EFFECT = NOT_ESTABLISHED
ATTENTION_MAINTENANCE = NOT_ESTABLISHED
DRIFT_CAUSAL_ATTRIBUTION = NOT_ESTABLISHED
AI_IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## References

- OpenAI. (2026-06-04). *Dreaming: Better memory for a more helpful ChatGPT.* https://openai.com/index/chatgpt-memory-dreaming/
- Altmann, E. M., & Trafton, J. G. (2002). *Memory for goals: an activation-based model.* Cognitive Science, 26(1), 39–83. https://doi.org/10.1207/S15516709COG2601_2
- Trafton, J. G., Altmann, E. M., Brock, D. P., & Mintz, F. E. (2003). *Preparing to resume an interrupted task: effects of prospective goal encoding and retrospective rehearsal.* International Journal of Human-Computer Studies, 58(5), 583–603. https://doi.org/10.1016/S1071-5819(03)00023-5
- Monk, C. A., Trafton, J. G., & Boehm-Davis, D. A. (2008). *The effect of interruption duration and demand on resuming suspended goals.* Journal of Experimental Psychology: Applied. https://doi.org/10.1037/a0014402
- Van-Horenbeke, F. A., & Peer, A. (2021). *Activity, Plan, and Goal Recognition: A Review.* Frontiers in Robotics and AI, 8, 643010. https://doi.org/10.3389/frobt.2021.643010
- O'Neill, T. A., McNeese, N. J., Barron, A., & Schelble, B. G. (2021). *Human–Autonomy Teaming: Definitions, Debates, and Directions.* Frontiers in Psychology. https://pmc.ncbi.nlm.nih.gov/articles/PMC8195568/
- Cai, Y., Zhu, Y., Gao, L., Tang, W., & Qin, S. (2026). *Push Your Agent: Measuring and Enforcing Quantitative Goal Persistence in Long-Horizon LLM Agents.* arXiv:2605.23574. https://arxiv.org/abs/2605.23574
- Chen, J., Sun, Y., Zhang, L., Xu, L., & Shi, J. (2026). *Long-Horizon Agent Trajectory Attribution: A Unified Benchmark and Fine-Grained Annotation Framework.* arXiv:2608.06909. https://arxiv.org/abs/2608.06909
- Zhu, C., et al. (2026). *SAFARI: Scaling Long Horizon Agentic Fault Attribution via Active Investigation.* arXiv:2606.24626. https://arxiv.org/abs/2606.24626
