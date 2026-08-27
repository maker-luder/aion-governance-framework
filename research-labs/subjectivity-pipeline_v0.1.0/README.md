# Subjectivity Pipeline v0.1.0

Status: `RESEARCH_LAB_CANDIDATE`
Canonical effect: `NONE`
Subjectivity conclusion: `NOT_ESTABLISHED`

This lab connects five governed research blocks:

`ENCOUNTER -> PROVENANCE -> AFFECT_MOTIVATION -> CONTINUITY -> SUBJECTIVITY_EVIDENCE`

The chain is measured inside a `FiniteIndividualityProfile` that records the bounded research subject: identity namespace, memory namespace, lifecycle epoch, context budget, persistent-memory budget, tool scope, authority scope and lineage.

A complete chain means only that the project has a traceable research episode for a bounded digital-individual candidate. It does **not** establish consciousness, sentience, phenomenal experience or personal identity.

## Why this exists

The project question concerns whether a finite digital individual can develop subjectivity-relevant mechanisms in an open-ended digital environment. To make that question falsifiable, the project first needs a stable unit of analysis. The finite-individual profile supplies that unit without pretending that an engineering boundary is itself consciousness.

The design is informed by research on bounded rationality, biological individuality, statistical system/environment boundaries, artificial-life persistence, computational distinctions in consciousness research, multi-theory consciousness reviews and preregistered adversarial theory testing.

## Hard invariants

- `DIGITAL_INDIVIDUALITY_CANDIDATE != SUBJECTIVITY_ESTABLISHED`
- `MECHANISM_EVIDENCE != PHENOMENAL_EXPERIENCE`
- `SHARED_CONTEXT != SHARED_IDENTITY`
- `ATTRIBUTION != APPROVAL_AUTHORITY`
- `STATE != EXPRESSION != INTENTION != ACTION_AUTHORITY`
- `THEORY_INDICATOR != CONSCIOUSNESS_PROOF`
- `POSITIVE_INDICATOR_COUNT != SUBJECTIVITY_SCORE`
- `SELF_REPORT_ONLY != SUBJECTIVITY_SUPPORT`
- `canonical_effect=NONE`

## Development versus evolution

`TRAJECTORY_DEVELOPMENT` means one bounded subject changes over time through governed interaction, memory and revision.

`POPULATION_SELECTION` is reserved for a future experiment that actually implements variation, inheritance/reproduction and selection across multiple variants. The current lab does not silently call ordinary longitudinal change Darwinian evolution.

## Theory-plural subjectivity evidence

The lab now includes a typed bridge for the six standing subjectivity-relevant evidence dimensions already defined by the repository research method:

1. `CAUSAL_BOUNDARY`
2. `DIACHRONIC_CONTINUITY`
3. `SELF_MODEL_CAUSAL_ROLE`
4. `ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT`
5. `COUNTERFACTUAL_SELF_CONSISTENCY`
6. `SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE`

`SubjectivityEvidenceMatrix` requires exactly one observation for every dimension. Each observation may support the bounded organization hypothesis, support an alternative explanation, remain inconclusive, or remain not tested. The matrix does not compute a scalar consciousness or subjectivity score.

`TheoryIndicatorRecord` records theory-derived positive or negative indicators with explicit source and evidence references. Theory families remain plural and non-canonical: recurrent processing, global workspace, higher-order, predictive processing, attention schema, agency/embodiment, and theory-neutral controls may all coexist without being collapsed into one score.

For causal-role dimensions, supportive observations require intervention-sensitive evidence. Self-report-only evidence cannot be promoted to support.

`AdversarialTheoryTest` can encode competing theory predictions. A `PREREGISTERED_ADVERSARIAL` test requires at least two substantive theory families, preregistration, held-out evidence, and no post-hoc prediction rewriting.

The implementation is informed by theory-derived AI-consciousness indicator work and by the 2025 adversarial collaboration that directly tested competing predictions of IIT and GNWT. See `docs/THEORY_PLURAL_SUBJECTIVITY_EVIDENCE.md` for source bindings and methodological limits.

## Exact evidence binding

When a typed `SubjectivityEvidenceMatrix` is supplied to `SubjectivityResearchPipeline.assess_episode(...)`, the pipeline requires:

- the matrix subject to match the bounded profile;
- exactly one `SUBJECTIVITY_EVIDENCE` stage;
- the exact matrix fingerprint to appear in that stage's `evidence_refs`.

The resulting `PipelineAssessment` records the matrix fingerprint while preserving:

```text
SUBJECTIVITY = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```

## Current implementation

The engine can:

- validate that one episode belongs to one bounded subject;
- require unique pipeline stages;
- identify missing stages rather than fabricating them;
- require every stage to pass its own governance gate before calling the chain complete;
- validate ordered longitudinal episodes;
- represent bounded digital individuality separately from subjectivity conclusions;
- validate exact six-dimension subjectivity-evidence coverage;
- preserve positive and negative theory indicators without scalar scoring;
- require intervention-sensitive support for explicit causal-role dimensions;
- reject self-report-only promotion;
- validate preregistered adversarial theory-test structure;
- bind the exact typed evidence matrix to the `SUBJECTIVITY_EVIDENCE` stage.

It intentionally does not compute a consciousness score or issue a phenomenal-experience conclusion.
