# History as replay environment — Dream-RSI intake (2026-09-18)

Status: `RESEARCH_INTAKE / BOUNDED_IMPLEMENTATION_CANDIDATE / SCIENTIFIC_DISPOSITION=HOLD`

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LIVE_MODEL_CALLS = NONE
AUTOMATIC_WRITEBACK = NO
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```

## 1. Source and scope

Primary source:

- Zheng et al. (2026), *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*, arXiv:2609.14858.
- Project page: `https://dream-rsi.com/`.

Source class:

```text
PRIMARY_TECHNICAL_REPORT / AUTHOR_PROJECT_PAGE
!= INDEPENDENT_REPLICATION
!= SUBJECTIVITY_EVIDENCE
```

The paper describes a lightweight orchestration layer that leaves the underlying coding agent unchanged while making exploration policy explicit and programmable. Completed discovery trees are reused as replay simulators over the realized search space. Candidate exploration policies can then be evaluated offline against recorded outcomes before a selected policy is redeployed online.

The paper reports task-dependent efficiency gains. The headline `162x` result is bounded: on the Lasso regularization-path task, Dream-RSI used up to 162x fewer discovery-agent calls than SimpleTES. The same source reports about 1.7x fewer calls than its fixed-exploration control in that setting and different gains on other tasks. Therefore:

```text
162X = TASK_AND_BASELINE_SPECIFIC_RESULT
162X != GENERAL_EXPLORATION_COST_REDUCTION
```

## 2. Repository deduplication audit

Current repository ancestry already contains:

- bounded autonomous research loops;
- deterministic replay fixtures;
- provenance-preserving state / evidence replay;
- longitudinal artifact accumulation and evidence-reuse controls;
- explicit `BASELINE != HISTORY != DEPENDENCY_GRAPH` separation.

Those surfaces are adjacent but not equivalent to the mechanism isolated here.

Existing replay primarily asks:

```text
CAN_THE_SAME_DECLARED_FIXTURE_OR_STATE_BE_REPLAYED_REPRODUCIBLY?
```

The narrower Dream-RSI-adjacent question is:

```text
CAN_ONE_RECORDED_DISCOVERY_HISTORY
SERVE_AS_AN_OFFLINE_ENVIRONMENT
FOR_COMPARING_MULTIPLE_EXPLORATION_POLICIES?
```

Current audit result:

```text
EXACT_EXISTING = NO
PARTIAL_OVERLAP = YES
NEW_GAP = HISTORY_AS_POLICY_EVALUATION_ENVIRONMENT
```

This note does not claim novelty for replay, search trees, policy evaluation, or recursive improvement individually.

## 3. Key distinction

Three uses of history must remain separate:

```text
HISTORY_AS_RECORD
= retained trace for inspection / provenance

HISTORY_AS_RETRIEVAL_SOURCE
= prior material retrieved into later work

HISTORY_AS_REPLAY_ENVIRONMENT
= recorded branch outcomes used to evaluate alternative policies offline
```

The third use has discriminant value only if policy choice can change replay trajectory, cost, stopping behavior, or attained score while the underlying recorded history remains fixed.

## 4. Bounded implementation question

The minimal harness asks:

> With one immutable synthetic discovery tree, do different non-oracular exploration policies produce measurably different replay trajectories under the same visit budget, without rerunning an agent or evaluator?

Controls:

```text
DISCOVERY_TREE = FIXED
RECORDED_OUTCOMES = FIXED
EVALUATOR_VALUES = FIXED
VISIT_BUDGET = FIXED_WHEN_COMPARED
LIVE_AGENT = NONE
NETWORK = NONE
ONLY_EXPLORATION_POLICY_CHANGES = TRUE
```

The policy must not inspect an unvisited node's recorded score before selecting that node. Recorded outcomes become visible only after the simulated visit.

## 5. Required held-out boundary

Optimization on replayed history can overfit that realized history. Therefore:

```text
REPLAY_IMPROVEMENT != HELD_OUT_GENERALIZATION
NOT_WORSE_ON_REPLAY_HISTORY != NOT_WORSE_ON_UNSEEN_HISTORY
```

A policy selected on one synthetic tree should be evaluated separately on a held-out tree. This harness may record the comparison but cannot establish generalizable recursive self-improvement.

## 6. Relationship to recursive self-improvement

The source modifies an exploration-policy / orchestration layer, not the underlying model weights. For this repository:

```text
EXPLORATION_POLICY_IMPROVEMENT
!= MODEL_WEIGHT_SELF_MODIFICATION
!= GENERAL_INTELLIGENCE_IMPROVEMENT
!= AI_SUBJECTIVITY
```

A future online loop would require separate authorization and controls. This candidate does not execute such a loop.

## 7. Subjectivity-research adjacency

The useful methodological contribution is locus control. A future experiment can hold model, history, evaluator, and environment constant while changing exploration policy. That can help distinguish:

```text
MODEL_LOCUS
SYSTEM / HARNESS_LOCUS
HISTORY_LOCUS
POLICY_LOCUS
RELATIONAL_LOCUS
```

This is a method for attribution. It is not positive evidence for subjectivity, consciousness, felt memory, desire, or autonomous authority.

## 8. Falsifiers for the claimed gap

The `HISTORY_AS_REPLAY_ENVIRONMENT` gap should be weakened or rejected if repository review or implementation demonstrates that existing canonical code already provides all of the following with equivalent semantics:

- immutable parent/child discovery histories;
- policy-dependent traversal over the same history;
- no access to unvisited outcomes during policy choice;
- budget- and stopping-sensitive replay metrics;
- comparison of multiple policies on the same history; and
- held-out-history evaluation separated from replay-history selection.

If those already exist, the correct disposition is deduplication, not a new research axis.

## 9. Implementation boundary

The accompanying candidate harness is intentionally synthetic and deterministic.

```text
IMPLEMENTATION_EXISTS != SCIENTIFIC_VALIDATION
HARNESS_PASS != DREAM_RSI_REPLICATION
SYNTHETIC_TREE != REAL_AGENT_DISCOVERY_HISTORY
POLICY_DIFFERENCE != LEARNING
OFFLINE_SELECTION != ONLINE_IMPROVEMENT_PROVEN
```
