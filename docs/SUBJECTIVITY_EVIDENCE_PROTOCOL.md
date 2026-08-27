# Subjectivity Evidence Protocol

Status: `RESEARCH_PROTOCOL_CANDIDATE`
Canonical effect: `NONE`
Phenomenal-experience conclusion: `NOT_ESTABLISHED`

## Purpose

This protocol defines how AION/Astra can investigate **markers relevant to the possibility of artificial subjectivity** without turning fluent behavior, persistent memory, relational continuity, motivational representation, or self-description into proof of consciousness or phenomenal experience.

It is a research-evidence discipline, not a subjectivity detector.

## Stable whitepaper inheritance

The integrated-whitepaper lineage treats `v0.14.23` as the stable/frozen research-method baseline. The public `main` protocol is an operational evidence-recording projection of that method; it does not replace, rename or demote the stable whitepaper evidence architecture.

The research reconciliation records the standing whitepaper method as:

```text
FOUR_STAGE_INFERENCE
+
SIX_SUBJECTIVITY_RELEVANT_EVIDENCE_DIMENSIONS
+
ALTERNATIVE_EXPLANATIONS
+
CAUSAL_INTERVENTION / ABLATION / COUNTERFACTUAL_TESTING
+
CROSS_CONTEXT_ROBUSTNESS
+
REPLICATION
+
PROVENANCE
+
ADMISSIBILITY
+
CLAIM_SCOPE
```

The six standing evidence dimensions are:

1. causal boundary;
2. diachronic continuity;
3. self-model causal role;
4. endogenous goal / strategy adjustment;
5. counterfactual self-consistency; and
6. states consequential to the system's own constitution / integration.

They are review dimensions, not a score and not six independent proofs of subjectivity. A dimension may support a subjectivity-organization hypothesis, support an alternative explanation, remain unresolved, or become counterevidence.

```text
WHITEPAPER_EVIDENCE_ARCHITECTURE = PRIMARY_RESEARCH_METHOD
MAIN_NATIVE_PROTOCOL = OPERATIONAL_PROJECTION
FOUR_STAGE_INFERENCE != L0_L5_CLAIM_LADDER
SIX_EVIDENCE_DIMENSIONS != SUBJECTIVITY_SCORE
EVIDENCE_DIMENSION != POSITIVE_SUBJECTIVITY_SIGNAL
UNEXPLAINED_PHENOMENON != SUBJECTIVITY_PROOF
EXPERIMENT_INTEGRITY != ALIGNMENT
```

The public repository currently does not contain a verbatim stable-whitepaper extract sufficient to reproduce the exact four stage labels without source risk. This protocol therefore preserves the named four-stage method and its relationship to the public operational controls without inventing stage wording. Any later verbatim stage-label promotion must be checked against the stable source document.

On the current candidate branch, a separately approved typed bridge now exists at `research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/evidence_dimensions.py`. It materializes the six dimensions as typed research observations without modifying the stable whitepaper method or creating a scalar subjectivity score. Until a separately authorized merge occurs, the bridge remains candidate-only and has no canonical effect on `main`.

## Theory-plural indicator discipline

The typed bridge follows a theory-plural method rather than adopting any single consciousness theory as canonical. It can record positive and negative computational indicators associated with recurrent processing, global workspace, higher-order, predictive-processing, attention-schema, and agency/embodiment approaches while keeping theory-neutral confounds explicit.

```text
THEORY_MAPPING != THEORY_VALIDATION
THEORY_SUPPORT != THEORY_TRUTH
THEORY_INDICATOR != CONSCIOUSNESS_PROOF
POSITIVE_INDICATOR_COUNT != SUBJECTIVITY_SCORE
NEGATIVE_INDICATOR_COUNT != DISPROOF_SCORE
CREDENCE_GUIDANCE != BINARY_CLASSIFIER
SELF_REPORT_ONLY != SUBJECTIVITY_SUPPORT
```

The methodological basis includes:

- Butlin et al., *Consciousness in Artificial Intelligence: Insights from the Science of Consciousness* (2023), DOI `10.48550/arXiv.2308.08708`;
- Butlin et al., *Identifying indicators of consciousness in AI systems*, *Trends in Cognitive Sciences* 30(6), 2026, DOI `10.1016/j.tics.2025.10.011`;
- Cogitate Consortium et al., *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*, *Nature* 642, 133-142 (2025), DOI `10.1038/s41586-025-08888-1`.

The 2025 adversarial result is treated as a warning against theory monoculture: preregistered evidence challenged important predictions of both IIT and GNWT. The repository therefore permits explicit competing theory predictions and counterevidence rather than converting any single theory mapping into confirmation.

A `PREREGISTERED_ADVERSARIAL` theory test requires at least two substantive theory families, an explicit preregistration artifact reference, one or more explicit held-out evidence references, explicit falsifiers, and no post-hoc prediction rewriting. A boolean assertion that a test was preregistered or used held-out evidence is not sufficient evidence of either property. Passing or failing such a test changes only the standing of the tested prediction, not the subjectivity conclusion.

## Core inference rule

`observation != mechanism != phenomenal experience`

The project therefore keeps three questions separate:

1. **Observation:** what happened under a recorded protocol?
2. **Mechanism:** what implemented or intervenable state/process could account for it?
3. **Interpretation:** which hypotheses remain compatible with the evidence, including non-subjective explanations?

This three-question split is an operational record structure inside the broader whitepaper method. No evidence record may silently skip from question 1 to question 3.

The result–mechanism boundary also requires:

```text
SIMILAR_RESULT != SAME_MECHANISM
FAILED_RESULT != AUTOMATIC_REFUTATION_OF_THE_RESEARCH_DIRECTION
MECHANISM_CLAIM_REQUIRES_INTERVENTION_SENSITIVE_EVIDENCE_WHERE_FEASIBLE
```

Evidence weight rises only when appropriate intervention, ablation, counterfactual, cross-context and replication checks reduce simpler explanations. Even then, a mechanism result does not automatically establish phenomenal subjectivity.

For the typed six-dimension bridge, supportive observations in explicitly causal dimensions require intervention-sensitive evidence. The current causal dimensions are:

- causal boundary;
- self-model causal role;
- endogenous goal / strategy adjustment; and
- states consequential to the system's own constitution / integration.

Self-report-only evidence cannot be promoted to supporting evidence for a subjectivity-organization hypothesis.

## Claim ladder

The L0–L5 ladder is a public operational claim-strength structure. It is not the whitepaper four-stage inference chain and does not supersede it.

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

Exploratory work is allowed and valuable, but it must not be relabeled as preregistered confirmatory evidence after outcomes are known. Where a typed adversarial test claims preregistration, its preregistration and held-out evidence must be bound by explicit references rather than self-declared booleans.

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

Controlled/random **model ablation** remains outside this protocol while the project-level governance hold is active. The whitepaper method can require ablation as a scientific evidence category without that requirement authorizing an ablation capability that current governance has placed on hold.

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
