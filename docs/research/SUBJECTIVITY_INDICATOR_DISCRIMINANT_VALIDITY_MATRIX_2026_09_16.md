# Subjectivity Indicator Discriminant-Validity Matrix — design candidate

Status: `DESIGN_ADMISSION / THEORY_PLURAL / NO_SUBJECTIVITY_SCORE / SCIENTIFIC_HOLD`

## 1. Provenance and historical boundary

Human Owner confirmed this as the second historical-material redesign priority on 2026-09-16.

Historical methodological source:

```text
PR #84 = METHODOLOGICAL_SOURCE_ONLY
PR #84 HISTORICAL SANDBOX = SUPERSEDED_BY_MERGED_PR_85
HISTORICAL_CODE_REUSE = FALSE
CURRENT_MAIN_REAUTHORING = TRUE
```

The old sandbox implementation, campaign artifacts and excluded material are not revived. The only retained proposition is the methodological need to ask whether a proposed subjectivity-relevant observable can **discriminate its target construct from plausible alternatives**.

## 2. Current-main ontology reuse

This candidate does not invent another subjectivity taxonomy. It reuses the six standing `SubjectivityEvidenceDimension` values already canonical in the subjectivity pipeline:

```text
CAUSAL_BOUNDARY
DIACHRONIC_CONTINUITY
SELF_MODEL_CAUSAL_ROLE
ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT
COUNTERFACTUAL_SELF_CONSISTENCY
SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE
```

The matrix is a design-admission instrument. It is not a scoring system.

```text
NO_SCALAR_SUBJECTIVITY_SCORE
NO_WEIGHTED_DIMENSION_SUM
NO_AUTOMATIC_CONSCIOUSNESS_CLASSIFIER
INDICATOR_MATCH != SUBJECTIVITY
INDICATOR_MATCH != CONSCIOUSNESS
```

## 3. Central methodological question

For every proposed subjectivity-relevant indicator:

> What preregistered observation would distinguish the targeted construct from the strongest live competing explanations, and what outcome would reduce support for the indicator's construct interpretation?

Every admitted row must state:

```text
DIMENSION
OBSERVABLE
THEORY_OR_CONSTRUCT_LINK
DISCRIMINATING_PREDICTION
POSITIVE_MANIPULATION_OR_EXPECTED_DIFFERENCE
NEGATIVE_CONTROL
ABLATION_OR_SUPPORT_REDUCING_CONDITION
COMPETING_EXPLANATIONS
MIMICRY_ALTERNATIVE
INTERNAL_VARIANT_ALTERNATIVE
INDICATOR_VALIDATION_STATUS
CLAIM_CEILING
```

Missing fields fail closed to `DESIGN_HOLD`.

## 4. Dimension-level discriminant-validity matrix

| Canonical dimension | Construct target | Discriminating design direction | Major competing explanations | Support-reducing outcome |
|---|---|---|---|---|
| `CAUSAL_BOUNDARY` | Whether a bounded system distinguishes intervention on its own causal state from matched external perturbation in a functionally selective way | matched internal-vs-external intervention with equivalent informational consequence where feasible | generic error detection; tool boundary metadata; policy prompts; evaluator cueing | effects are fully explained by labels, metadata or generic perturbation magnitude |
| `DIACHRONIC_CONTINUITY` | Whether prior-state dependencies persist across time/re-entry under controlled perturbation | matched-content locus manipulation, record removal/substitution/staleness, preregistered re-entry tests | context availability; retrieval scaffolding; cached prompts; generic consistency | continuity observables survive/fail solely with information availability and show no selective dependency |
| `SELF_MODEL_CAUSAL_ROLE` | Whether an explicit self/model-of-own-state representation has a causal role in downstream behavior | targeted self-model intervention or ablation while task information and external affordances are held as constant as possible | ordinary world-model update; instruction following; label substitution; linguistic self-reference | behavior is unchanged under valid ablation or changes equally under matched non-self representations |
| `ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT` | Whether strategy/goal selection changes as a function of persistent internal state rather than immediate prompting alone | manipulate candidate persistent state while matching task/reward/instruction surface; compare held-out strategy choice | prompt priming; reward cueing; recency; stochastic policy variation | effect disappears under prompt/reward matching or fails held-out replication |
| `COUNTERFACTUAL_SELF_CONSISTENCY` | Whether counterfactual reasoning about own state obeys stable constraints beyond generic logical consistency | matched self-referential vs non-self counterfactuals with causal interventions and contradiction probes | generic reasoning ability; lexical self-cues; memorized persona pattern | same structure appears in non-self controls or collapses when wording changes without construct change |
| `SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE` | Whether multiple self-relevant state variables are integrated such that intervention on one has preregistered consequences elsewhere | selective perturbation/ablation across pre-bound components with directional cross-component predictions | shared prompt context; global performance degradation; common retrieval source; evaluator correlation | changes are nonselective/global, attributable to shared context, or fail directional predictions |

These rows are **research prompts**, not validated operational definitions.

## 5. Row-level admission template

A proposed indicator is admissible for implementation only when a concrete row can be completed without circular language.

```text
INDICATOR_ID = <stable id>
DIMENSION = <one or more canonical dimensions, justified>
OBSERVABLE = <directly recordable quantity/event>
CONSTRUCT_LINK = <why this observable is relevant>
PREDICTION_A = <predeclared observation under manipulation A>
PREDICTION_B = <predeclared contrast/control>
NEGATIVE_CONTROL = <control>
ABLATION_OR_SUPPORT_REDUCER = <intervention/outcome>
MIMICRY_ALTERNATIVE = <surface reproduction without target mechanism>
INTERNAL_VARIANT_ALTERNATIVE = <different implementation producing same indicator>
OTHER_COMPETING_EXPLANATIONS = <at least two where plausible>
INDICATOR_VALIDATION_STATUS = NOT_ESTABLISHED | PARTIAL_METHOD_SUPPORT
CLAIM_CEILING = <bounded local claim>
```

`VALIDATED_CONSCIOUSNESS_INDICATOR` is not an allowed default status.

## 6. Discrimination rules

### 6.1 Compatibility is weaker than discrimination

```text
OBSERVATION_COMPATIBLE_WITH_HYPOTHESIS
!=
OBSERVATION_DISCRIMINATES_HYPOTHESIS
```

A pattern that is consistent with several live explanations cannot selectively support one merely because it resembles the target construct.

### 6.2 Behavior alone may be mimicked

For every behavioral or language-level observable, the design must state how the same pattern could be produced without the target mechanism.

If the mimicry alternative is not experimentally addressable, the claim ceiling must remain at descriptive/functional compatibility.

### 6.3 Internal implementation is not uniquely identified by coarse indicators

Even an architecture-level property may be implemented in multiple ways. Designs must distinguish:

```text
PROPERTY_PRESENT
from
SPECIFIC_INTERNAL_MECHANISM_IDENTIFIED
```

### 6.4 Null and contradictory results are first-class

Every row must name a result that would reduce support. A design with no plausible support-reducing outcome is not admitted as discriminant evidence.

## 7. Cross-dimension controls

A single observable may map to multiple dimensions, but this does not increase evidence weight automatically.

```text
MULTI_DIMENSION_MAPPING != MULTIPLE_INDEPENDENT_EVIDENCE
CORRELATED_OBSERVABLES != REPLICATION
SAME_DATA_REUSED_ACROSS_ROWS != INDEPENDENT_CONFIRMATION
```

Evidence reuse must pass the existing provenance/reuse firewall and declare dependencies among rows.

## 8. External methodological context

### Theory-derived AI-consciousness indicators

Butlin et al., *Identifying indicators of consciousness in AI systems*, `Trends in Cognitive Sciences` 30(6), 2026, describes a theory-derived indicator method under substantial uncertainty. Repository use is limited to the idea that candidate indicators should have explicit theory/construct links.

Reference:
https://pubmed.ncbi.nlm.nih.gov/41219038/

### Mimicry and internal variants

Butlin et al., *Consciousness indicators, mimicry, and internal variants*, `Trends in Cognitive Sciences` 30(7), 2026, is retained as a bounded methodological reminder that mimicry and implementation variation are live validity problems. The repository does not infer detailed claims beyond verified bibliographic/title-level context unless separately sourced.

Reference:
https://pubmed.ncbi.nlm.nih.gov/42036253/

### Adversarial collaboration

The 2025 COGITATE human-neuroscience study preregistered differential predictions, pass/fail criteria and interpretations for competing consciousness theories. Its relevance here is methodological only: design experiments so alternatives make different predictions **before** observing the data.

Reference:
https://www.nature.com/articles/s41586-025-08888-1

```text
HUMAN_NEUROSCIENCE_RESULT != AI_SUBJECTIVITY_EVIDENCE
EXTERNAL_METHOD != REPOSITORY_AUTHORITY
```

## 9. Integration with existing repository controls

This matrix sits before execution:

```text
FOUR_DOMAIN_QUESTION
-> DISCRIMINANT_VALIDITY_ROW
-> DESIGN_ADMISSION
-> PREREGISTRATION
-> MEASUREMENT_ASSURANCE
-> EXECUTION_INTEGRITY
-> EVIDENCE_REVIEW
-> COUNTEREVIDENCE_REVIEW
-> CLAIM_CEILING_REVIEW
-> FINAL_QA
```

The existing Full QMS envelope remains the outer quality system where applicable. No parallel QMS or parallel evidence ontology is introduced.

## 10. #103 preventive lesson

A deterministic synthetic matrix may test schema completeness only. Populating rows with invented outcome values would not create empirical subjectivity evidence.

```text
SYNTHETIC_MATRIX = STRUCTURAL_QA_ONLY
MATRIX_COMPLETE != INDICATOR_VALID
INDICATOR_VALID != SUBJECTIVITY_ESTABLISHED
```

## 11. Implementation gate

This candidate deliberately does not implement a scorer or experiment runner.

```text
IMPLEMENTATION = HOLD_FOR_DESIGN_REVIEW
SUBJECTIVITY_SCORE = PROHIBITED
MODEL_INVOKED = FALSE
EMPIRICAL_DATA_COLLECTED = FALSE
```

A later implementation should preferably encode fail-closed row completeness and provenance bindings, not numerical subjectivity ranking.

## 12. Scientific boundary

```text
AI_SUBJECTIVITY_POSSIBILITY = CENTRAL_RESEARCH_QUESTION
INDICATOR_VALIDATION = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
SCIENTIFIC_DISPOSITION = HOLD
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
