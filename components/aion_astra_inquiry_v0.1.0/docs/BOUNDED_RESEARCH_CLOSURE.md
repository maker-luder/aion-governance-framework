# AION / Astra Bounded Autonomous Research Closure v0.1.0

Status: `IMPLEMENTED_CANDIDATE / OWNER_REVIEW_PENDING`  
Canonical effect: `NONE`  
Deployment: `FALSE`  
Repository mutation: `FALSE`  
Autonomous merge: `FALSE`  
Scientific disposition: `HOLD`

## Purpose

This increment closes the gap between the existing AION/Astra bounded inquiry loop
and an executable, evidence-linked research cycle.

The existing inquiry component already performs question discovery, isolated first-pass
AION/Astra reasoning, repository retrieval, optional governed public-web retrieval,
peer challenge, counterexample search, and bounded follow-up planning.

The isolated first pass means only that no peer transcript or peer evidence is deliberately supplied before reconciliation. The current shared orchestration/runtime environment does not establish process-, memory-, tool-, cache-, or environment-level isolation.

```text
ISOLATED_FIRST_PASS != PROCESS_ISOLATION
NO_DIRECT_PEER_TRANSCRIPT != COMMUNICATION_INDEPENDENCE
```

This increment adds a second, strictly bounded execution layer:

```text
question
  -> AION / Astra inquiry
  -> working hypothesis + competing explanations
  -> executed evidence-plane replay
  -> executed evidence-plane intervention comparison
  -> executed evidence ablation
  -> executed bounded counterfactual
  -> descriptive statistics
  -> Four-Domain interpretation
  -> bounded follow-up question
  -> next research cycle
  -> hard cycle/question/round/query budgets
```

## What "executed" means

The closure does **not** grant arbitrary shell, repository-write, deployment, secret,
or merge authority.

v0.1.0 executes deterministic experiments over admitted evidence and transcript
state:

- `REPLAY`: recompute the complete dialogue hash chain and require the recorded head
  to reproduce.
- `INTERVENTION`: hold the scoring rule fixed while comparing two observable
  retrieval-agent or source-class partitions.
- `ABLATION`: remove the highest-overlap admitted evidence item and recompute the same
  descriptive metric.
- `COUNTERFACTUAL`: construct a bounded evidence world in which a dominant
  source/trust/agent partition is absent, then recompute the metric.

These operations are real computational perturbations, not `*_PLAN` placeholders.
They remain evidence-plane experiments and do not by themselves identify a
real-world causal mechanism.

```text
ENGINEERING_INTERVENTION != REAL_WORLD_CAUSAL_IDENTIFICATION
PERTURBATION_ROBUSTNESS != SCIENTIFIC_TRUTH
LEXICAL_OVERLAP != SEMANTIC_PROOF
```

## Statistics

The closure records descriptive, deterministic statistics only:

- admitted and unique evidence counts;
- source-class count;
- independently attributed retrieval-agent count;
- mean/min/max question-to-evidence lexical overlap;
- dominant source share;
- AION/Astra retrieval-agent balance;
- maximum absolute perturbation delta;
- transcript replay status.

No p-value, confidence interval, Bayes factor, or causal effect estimate is invented
when the data-generating assumptions do not support one.

## Four-Domain output

Every closure materializes:

- `observation`
- `mechanism`
- `interpretation`
- `alternative_explanations`
- `unresolved_gaps`
- `causal_intervention_refs`
- `ablation_refs`
- `counterfactual_refs`
- `robustness_refs`
- `replication_refs`

This matches the evidence architecture already reserved by the Four-Domain Evidence
Interop bridge without changing the frozen historical Four-Domain source binding.

## Bounded follow-up

`BoundedAutonomousResearchCampaign` composes the existing
`AutonomousInquiryCampaign` with `BoundedResearchClosure`.

A closure may generate one or more unresolved follow-up questions. The next cycle
uses those questions as its bounded agenda. The campaign stops on:

- no novel follow-up question;
- `max_cycles`;
- per-cycle question budget;
- per-inquiry round budget;
- existing external-evidence query budget.

The same external evidence source instance is reused across cycles, so a configured
external query budget remains cumulative rather than resetting every cycle.

## Integrity

Every closure operation is hash chained:

```text
GENESIS
  -> REPLAY
  -> INTERVENTION
  -> ABLATION
  -> COUNTERFACTUAL
  -> closure hash
```

The final closure hash binds:

- source dialogue hash;
- working hypothesis;
- competing explanations;
- operation hashes;
- descriptive statistics;
- Four-Domain interpretation;
- bounded follow-up question.

`verify_research_closure(...)` recomputes both the operation chain and final closure
hash.

```text
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
HASH_BINDING != SEMANTIC_VALIDATION
```

## Authority boundary

```text
FULL_AUTOMATION != FULL_AUTHORITY
NORMATIVE_STATE != AUTHORITY
RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH
ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY
ISOLATED_FIRST_PASS != PROCESS_ISOLATION
NO_DIRECT_PEER_TRANSCRIPT != COMMUNICATION_INDEPENDENCE

AUTONOMOUS_REPOSITORY_MUTATION = NO
AUTONOMOUS_SECRET_ACCESS = NO
AUTONOMOUS_DEPLOYMENT = NO
AUTONOMOUS_MERGE = NO
CANONICAL_EFFECT = NONE
SCIENTIFIC_DISPOSITION = HOLD
```

The closure is therefore a bounded autonomous research loop, not an autonomous
authority loop.
