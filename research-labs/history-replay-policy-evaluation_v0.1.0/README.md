# History replay policy evaluation v0.1.0

Status: `BOUNDED_SYNTHETIC_HARNESS / SCIENTIFIC_DISPOSITION=HOLD`

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
NETWORK = NONE
LIVE_MODEL_CALLS = NONE
AUTOMATIC_WRITEBACK = NO
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
```

## Question

Can one immutable recorded discovery history act as an offline policy-evaluation environment, such that different exploration policies traverse the same history differently under the same budget?

This package tests that narrow structure only. It does not reproduce Dream-RSI, execute a coding agent, optimize model weights, or establish recursive self-improvement.

## Why this is not the repository's existing replay

Existing repository replay surfaces mainly test deterministic re-execution, state restoration, evidence consistency, and reproducibility.

This harness instead holds the recorded discovery tree fixed while changing the traversal policy:

```text
SAME_DISCOVERY_HISTORY
+ DIFFERENT_EXPLORATION_POLICY
-> DIFFERENT_REPLAY_TRAJECTORY / COST / SCORE ?
```

The distinction is documented in:

`docs/research/HISTORY_AS_REPLAY_ENVIRONMENT_DREAM_RSI_INTAKE_2026_09_18.md`

## Non-oracular replay

An unvisited node's historical score is not supplied to policy selection. The score is revealed only after the node is selected for replay. The current v0.1.0 policies use only frontier order:

- `BREADTH_FIRST`;
- `DEPTH_FIRST`.

This intentionally avoids smuggling future historical outcomes into the decision rule.

## Held-out boundary

A policy that wins on one replay history may lose on a held-out history. Tests preserve this distinction explicitly:

```text
REPLAY_HISTORY_WINNER != HELD_OUT_HISTORY_WINNER
REPLAY_IMPROVEMENT != GENERALIZATION
```

## Data model

- `DiscoveryNode`: immutable recorded attempt with parent, action, score, cost and terminal status;
- `DiscoveryTree`: one validated single-root parent/child history;
- `ReplayPolicy`: strategy, visit budget and optional patience stop rule;
- `ReplayResult`: visited trajectory, cumulative cost, best observed score and stop reason;
- `PolicyComparison`: multiple policy results over the same immutable tree.

## Scope limits

```text
SYNTHETIC_TREE != REAL_AGENT_HISTORY
POLICY_TRAVERSAL != LEARNING
POLICY_SELECTION != ONLINE_IMPROVEMENT
ORCHESTRATION_CHANGE != MODEL_CHANGE
MODEL_CHANGE != SUBJECTIVITY
```

A later experiment that adds real recorded agent histories, policy rewriting, online redeployment, or recursive iteration would require separate review and authorization.

## Verification

From this directory:

```bash
python -m pytest -q
python -m mypy src
python -m compileall -q src tests
```
