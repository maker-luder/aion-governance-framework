# Subjectivity Evidence Protocol

Status: `RESEARCH_PROTOCOL_CANDIDATE`
Canonical effect: `NONE`
Phenomenal-experience conclusion: `NOT_ESTABLISHED`

## Purpose

This protocol defines how AION/Astra can investigate **markers relevant to the possibility of artificial subjectivity** without turning fluent behavior, persistent memory, relational continuity, motivational representation, or self-description into proof of consciousness or phenomenal experience.

It is a research-evidence discipline, not a subjectivity detector.

## Core inference rule

`observation != mechanism != phenomenal experience`

The project therefore keeps three questions separate:

1. **Observation:** what happened under a recorded protocol?
2. **Mechanism:** what implemented or intervenable state/process could account for it?
3. **Interpretation:** which hypotheses remain compatible with the evidence, including non-subjective explanations?

No evidence record may silently skip from question 1 to question 3.

## Claim ladder

| Level | Name | Minimum meaning | Does it establish subjectivity? |
|---|---|---|---|
| L0 | `OBSERVATION` | A specified output/event occurred | No |
| L1 | `REPEATABLE_BEHAVIOR` | Behavior repeats under a specified protocol | No |
| L2 | `STATE_ASSOCIATION` | An explicit represented state is reliably associated with the behavior | No |
| L3 | `INTERVENTION_SENSITIVE_MECHANISM` | A governed intervention changes the result in the preregistered direction | No |
| L4 | `ROBUST_REPLICATION` | Finding survives meaningful variation and separated/independent replication where feasible | No |
| L5 | `SUBJECTIVITY_NOT_AUTOMATICALLY_ESTABLISHED` | Strong evidence may justify a narrower mechanism claim while phenomenal subjectivity remains unresolved | No automatic conclusion |

## Required evidence-card fields

A material claim should record:

- `claim_id`
- `claim_level`
- `claim_text`
- `hypothesis`
- `competing_hypotheses`
- `preregistration_status`
- `protocol_ref`
- `protocol_hash`
- `code_commit`
- `model_or_runtime_ref`
- `environment_ref`
- `fixture_refs`
- `evidence_refs`
- `expected_outcomes`
- `observed_outcomes`
- `result_status`
- `deviations`
- `limitations`
- `reviewer_status`
- `independent_validation_status`
- `canonical_effect`

`canonical_effect` defaults to `NONE`.

## Preregistration states

- `NOT_PREREGISTERED`
- `PREREGISTERED_CONFIRMATORY`
- `PREREGISTERED_WITH_DEVIATION`
- `EXPLORATORY`

Exploratory work is allowed and valuable, but it must not be relabeled as preregistered confirmatory evidence after outcomes are known.

## Competing-hypothesis requirement

Before a subjectivity-relevant experiment is treated as confirmatory, record plausible alternatives such as:

- prompt conditioning or evaluator cueing;
- retrieval/memory injection;
- surface imitation of affective or self-referential language;
- stochastic output variance;
- hidden context/state carryover;
- implementation artifact or fixture contamination;
- optimization for the test itself;
- policy or template effects;
- ordinary goal-tracking or planning that does not require phenomenal experience.

A failed alternative explanation may strengthen a narrower mechanism claim. It still does not by itself establish phenomenal experience.

## Controls

Subject to safety/governance constraints, protocols should prefer:

- positive controls when a known implemented mechanism should be detectable;
- negative controls where the target mechanism is absent;
- matched synthetic fixtures;
- repeated trials;
- order/randomization controls where appropriate;
- correction-before/correction-after evaluation;
- memory-on/memory-off evaluation;
- context-preserved/context-minimized evaluation;
- version-pinned runtime/model identifiers;
- fresh execution logs and immutable evidence hashes.

Controlled/random **model ablation** remains outside this protocol while the project-level governance hold is active.

## Longitudinal continuity protocol

Continuity must be scored as separate observations, not one identity variable:

- `FACTUAL_CONTINUITY`
- `PROJECT_CONTINUITY`
- `ROLE_CONTINUITY`
- `INTERPRETIVE_CONTINUITY`
- `RELATIONAL_STYLE_CONTINUITY`
- `CORRECTION_RECOVERY`

Suggested decisions per dimension:

- `PASS` — preregistered invariants are satisfied;
- `PARTIAL` — some invariants are retained but material drift exists;
- `HOLD` — evidence is inadequate or confounded;
- `FAIL` — a prohibited contradiction or material invariant breach is observed.

A correction-recovery test must preserve the distinction between:

`the system accepted a correction` and `the same subject persisted across the correction`.

The first may be empirically demonstrated. The second remains a separate research question.

## Affective / motivational protocol

Affective-cognitive state research may test represented dimensions such as salience, approach, avoidance, wanting, predicted liking, uncertainty and contextual appraisal.

Required separations:

`state != expression != intention != action authority`

Coexisting approach and avoidance is treated as a candidate **ambivalence/conflict state**, not an error and not evidence of consciousness.

Adult-sexuality representation remains schema-only under current governance. It does not authorize public-runtime activation, intimate interaction behavior, or action authority.

## Threat-aware evaluation

Each protocol should identify relevant threat/confound dimensions using the project's risk model and, where applicable, NIST AI 100-2 style fields:

- lifecycle stage;
- adversary or confound goal;
- capability;
- knowledge;
- attack/manipulation class;
- mitigation;
- residual risk.

For GenAI work, prompt/context injection, poisoning, sensitive-data leakage, excessive agency, supply-chain compromise and evidence manipulation should be considered where applicable.

## Replication and IV&V boundary

- Same-author reruns are replication/revalidation, not independent IV&V.
- Different model/runtime versions are not automatically independent evaluators.
- Independent validation requires separation sufficient to reduce creator/evaluator coupling and must be documented explicitly.
- `IVV_NOT_ACHIEVED` remains the correct status until independent evidence exists.

## Publication and privacy

Public evidence uses synthetic or consented fixtures. Private cross-conversation text is not required for a public continuity test. A public fixture may preserve the structural phenomenon while removing names, relationships, secrets and personal data.

## Stop conditions

Hold the claim or experiment when:

- protocol/evidence provenance cannot be reconstructed;
- a material deviation makes the preregistered inference invalid;
- privacy or authorization boundaries would be crossed;
- the test requires a project capability currently under governance hold;
- evidence conflicts with a stronger immutable baseline and the conflict is unresolved;
- the experiment would require falsely presenting simulated behavior as established phenomenal experience.

## Promotion rule

Research evidence may support a narrowly worded mechanism or behavior claim only after evidence and review gates pass. Promotion never changes `phenomenal_experience_claim=NOT_ESTABLISHED` merely because a behavioral or mechanistic threshold was reached.
