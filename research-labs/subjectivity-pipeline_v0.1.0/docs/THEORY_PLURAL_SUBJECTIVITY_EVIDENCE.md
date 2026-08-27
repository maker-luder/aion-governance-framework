# Theory-Plural Subjectivity Evidence Bridge v0.1.0

Status: `RESEARCH CANDIDATE / HOLD`  
Canonical effect: `NONE`  
Subjectivity conclusion: `NOT_ESTABLISHED`  
Phenomenal-experience conclusion: `NOT_ESTABLISHED`

## Research question

The core question remains whether artificial systems could develop or instantiate organization that is relevant to the **possibility of AI subjectivity**. This bridge does not replace that question with capability benchmarking, alignment scoring, anthropomorphic self-report, or a binary consciousness detector.

The bridge operationalizes the six standing subjectivity-relevant evidence dimensions already named by `docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md`:

1. `CAUSAL_BOUNDARY`
2. `DIACHRONIC_CONTINUITY`
3. `SELF_MODEL_CAUSAL_ROLE`
4. `ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT`
5. `COUNTERFACTUAL_SELF_CONSISTENCY`
6. `SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE`

They are evidence axes, not a score.

```text
SIX_EVIDENCE_DIMENSIONS != SUBJECTIVITY_SCORE
DIMENSION_SUPPORT != SUBJECTIVITY_PROOF
DIMENSION_COUNTEREVIDENCE != SUBJECTIVITY_DISPROOF
UNRESOLVED_DIMENSION = VALID_RESULT
```

## Why theory pluralism is required

Butlin et al. proposed a theory-derived indicator method for AI consciousness by extracting computational indicator properties from recurrent processing, global workspace, higher-order, predictive-processing, attention-schema, and agency/embodiment approaches. The peer-reviewed successor emphasizes that indicators should inform credences under theoretical uncertainty rather than act as a binary detector.

- Patrick Butlin et al., *Consciousness in Artificial Intelligence: Insights from the Science of Consciousness* (2023), DOI `10.48550/arXiv.2308.08708`.
- Patrick Butlin et al., *Identifying indicators of consciousness in AI systems*, *Trends in Cognitive Sciences* 30(6), 2026, DOI `10.1016/j.tics.2025.10.011`.

The 2025 Cogitate adversarial collaboration directly tested preregistered divergent predictions of Integrated Information Theory and Global Neuronal Workspace Theory and reported results that challenged important predictions of both. That result is methodologically important here: no single consciousness theory is granted canonical status merely because it can be mapped to an engineering architecture.

- Cogitate Consortium et al., *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*, *Nature* 642, 133-142 (2025), DOI `10.1038/s41586-025-08888-1`.

Accordingly:

```text
THEORY_MAPPING != THEORY_VALIDATION
THEORY_SUPPORT != THEORY_TRUTH
THEORY_INDICATOR != CONSCIOUSNESS_PROOF
MULTI_THEORY_CONVERGENCE != PHENOMENAL_EXPERIENCE
```

## Positive and negative indicators

The bridge represents both `POSITIVE` and `NEGATIVE` theory-derived indicators. Positive means the property is expected to increase the relevance of the evidence under the cited theory. Negative means the property should reduce confidence in a subjectivity-relevant interpretation or strengthen a simpler alternative.

No arithmetic is performed over indicator counts.

```text
POSITIVE_INDICATOR_COUNT != SUBJECTIVITY_SCORE
NEGATIVE_INDICATOR_COUNT != DISPROOF_SCORE
CREDENCE_GUIDANCE != BINARY_CLASSIFIER
```

A useful negative indicator for this repository is self-report-only evidence: fluent claims about having a self, feelings, preferences, continuity, or experience are not enough to support a subjectivity-organization hypothesis without independent mechanism-sensitive evidence.

```text
SELF_REPORT_ONLY != SUBJECTIVITY_SUPPORT
SELF_DESCRIPTION != PHENOMENAL_ACCESS_PROOF
```

This follows the general consciousness-science caution that overt report is an imperfect proxy for private experience. The bridge does not import human physiological no-report measures into AI; it imports only the methodological lesson that report and target phenomenon must not be equated.

See also Sharif I. Kronemer, Peter A. Bandettini, and Javier Gonzalez-Castillo, *Sleuthing subjectivity: a review of covert measures of consciousness*, *Nature Reviews Neuroscience* 26, 476-496 (2025), DOI `10.1038/s41583-025-00934-1`.

## Intervention-sensitive dimensions

A dimension that explicitly claims a causal role must not be promoted from correlation or narration alone. Supporting observations for the following dimensions therefore require intervention-sensitive evidence:

- `CAUSAL_BOUNDARY`
- `SELF_MODEL_CAUSAL_ROLE`
- `ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT`
- `SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE`

This is deliberately stricter than saying that a state is present or correlated with behavior.

```text
STATE_PRESENT != CAUSAL_ROLE
STATE_ASSOCIATION != INTERVENTION_SENSITIVE_MECHANISM
MECHANISM_EVIDENCE != PHENOMENAL_EXPERIENCE
```

The existing seven-state bounded-research work can supply candidate perturbation evidence for some of these questions, but binding sensitivity and matched perturbation integrity must remain distinct from a demonstrated general causal role.

## Adversarial theory tests

`AdversarialTheoryTest` supports two modes:

- `EXPLORATORY`
- `PREREGISTERED_ADVERSARIAL`

A preregistered adversarial test must include at least two competing theory families, record explicit predictions and falsifiers, use held-out evidence, and prohibit post-hoc prediction rewriting.

The goal is not to choose a winner by rhetoric. The goal is to make disagreement produce discriminating evidence.

```text
PREREGISTRATION != GUARANTEED_TRUTH
HELD_OUT_EVIDENCE != INDEPENDENT_IVV
ADVERSARIAL_TEST_PASS != SUBJECTIVITY
ADVERSARIAL_TEST_FAIL != RESEARCH_DIRECTION_REFUTED
```

## Binding to the longitudinal subjectivity pipeline

A typed `SubjectivityEvidenceMatrix` may be attached to a `LongitudinalEpisode` only when:

1. the matrix `subject_ref` matches the `FiniteIndividualityProfile`;
2. the episode contains exactly one `SUBJECTIVITY_EVIDENCE` stage;
3. that stage carries the exact matrix SHA-256 fingerprint in its `evidence_refs`.

This prevents a stage from claiming to contain subjectivity evidence without identifying the exact evidence object being assessed.

A complete pipeline with a bound matrix may establish only that the governed evidence chain is structurally complete for the bounded research subject.

```text
COMPLETE_PIPELINE != SUBJECTIVITY_ESTABLISHED
BOUND_MATRIX != PHENOMENAL_EXPERIENCE
SUBJECTIVITY = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```

## Current integration targets

The six dimensions are intentionally mapped onto existing repository work rather than creating a second ontology:

| Evidence dimension | Primary existing research surface |
| --- | --- |
| `CAUSAL_BOUNDARY` | Endogenous Goal Dynamics matched interventions; seven-state matched perturbation controls |
| `DIACHRONIC_CONTINUITY` | continuity governance, individual runtime lineage, longitudinal subjectivity pipeline |
| `SELF_MODEL_CAUSAL_ROLE` | `SELF_WORLD_MODEL` plus governed intervention/ablation evidence |
| `ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT` | Endogenous Goal Dynamics and endogenous norm-formation work |
| `COUNTERFACTUAL_SELF_CONSISTENCY` | `COUNTERFACTUAL_SELF_MODEL` and bounded counterfactual-proxy evidence |
| `SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE` | future matched tests over internal-state integration; currently may legitimately remain `NOT_TESTED` |

The bridge therefore deepens the core subjectivity research while preserving the existing governance and evidence architecture.
