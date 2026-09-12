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
- `PREREGISTRATION_FLAG != PREREGISTRATION_EVIDENCE`
- `MODEL_PROPERTY != SYSTEM_PROPERTY`
- `SYSTEM_PROPERTY != RELATIONAL_PROPERTY`
- `OBSERVER_ATTRIBUTION != INTERNAL_PROPERTY`
- `canonical_effect=NONE`

## Development versus evolution

`TRAJECTORY_DEVELOPMENT` means one bounded subject changes over time through governed interaction, memory and revision.

`POPULATION_SELECTION` is reserved for a future experiment that actually implements variation, inheritance/reproduction and selection across multiple variants. The current lab does not silently call ordinary longitudinal change Darwinian evolution.

## Theory-plural subjectivity evidence

The lab includes a typed bridge for the six standing subjectivity-relevant evidence dimensions already defined by the repository research method:

1. `CAUSAL_BOUNDARY`
2. `DIACHRONIC_CONTINUITY`
3. `SELF_MODEL_CAUSAL_ROLE`
4. `ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT`
5. `COUNTERFACTUAL_SELF_CONSISTENCY`
6. `SELF_CONSTITUTION_INTEGRATION_CONSEQUENCE`

`SubjectivityEvidenceMatrix` requires exactly one observation for every dimension. Each observation may support the bounded organization hypothesis, support an alternative explanation, remain inconclusive, or remain not tested. The matrix does not compute a scalar consciousness or subjectivity score.

`TheoryIndicatorRecord` records theory-derived positive or negative indicators with explicit source and evidence references. Theory families remain plural and non-canonical: recurrent processing, global workspace, higher-order, predictive processing, attention schema, agency/embodiment, and theory-neutral controls may all coexist without being collapsed into one score.

For causal-role dimensions, supportive observations require intervention-sensitive evidence. Self-report-only evidence cannot be promoted to support.

`AdversarialTheoryTest` can encode competing theory predictions. A `PREREGISTERED_ADVERSARIAL` test requires at least two substantive theory families, an explicit preregistration artifact reference, one or more explicit held-out evidence references, and no post-hoc prediction rewriting. Those references make the claim inspectable; they do not by themselves validate the referenced artifacts.

The implementation is informed by theory-derived AI-consciousness indicator work and by the 2025 adversarial collaboration that directly tested competing predictions of IIT and GNWT. See `docs/THEORY_PLURAL_SUBJECTIVITY_EVIDENCE.md` for source bindings and methodological limits.

## Evidence locus discipline

Recent Human Owner inquiry raised a distinct methodological question: if a subjectivity-relevant mechanism were observed, is the relevant locus the base model, surrounding scaffold, integrated system, or interaction relation? The current answer is intentionally open.

`aion_subjectivity_pipeline.locus` therefore classifies evidence as `MODEL`, `SCAFFOLD`, `SYSTEM`, `RELATIONAL`, `OBSERVER_ATTRIBUTION`, or `UNKNOWN`. A same-locus engineering claim can be admitted as bounded engineering evidence. Cross-locus promotion fails closed unless a separately specified bridge hypothesis states a mechanism, falsifier and preregistration reference. Even a structurally valid bridge remains only a `RESEARCH_CANDIDATE`.

Any attempt to use model-, scaffold-, system-, relational-, or observer-level evidence directly as proof of subjectivity is held at `NOT_ESTABLISHED`.

See [`docs/MODEL_SYSTEM_RELATIONAL_LOCUS.md`](docs/MODEL_SYSTEM_RELATIONAL_LOCUS.md).

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
- require inspectable preregistration and held-out evidence references for preregistered adversarial theory tests;
- bind the exact typed evidence matrix to the `SUBJECTIVITY_EVIDENCE` stage;
- classify model/scaffold/system/relational/observer evidence loci;
- fail closed on unknown loci and observer-attribution substitution;
- require explicit preregistered bridge hypotheses for cross-locus research candidates;
- preserve `SUBJECTIVITY=NOT_ESTABLISHED` for all locus assessments.
- fingerprint a Four-Domain design candidate across construct, machine question,
  standing dimension, locus, intervention, controls, falsifier, alternatives and claim ceiling;
- distinguish `READY_FOR_BOUNDED_ENGINEERING_DESIGN`,
  `OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE` and `HOLD` without treating admission as evidence;
- require all five subjectivity/consciousness/experience/agency/status nonclaims;
- bind the admitted candidate to the full quality trace from source IQC through
  preregistration, execution integrity, evidence/counterevidence review, claim-ceiling
  review and final QA, then emit readiness for the external Human-review boundary;
- require NCR/CAPA effectiveness evidence rather than treating an applied action as closure;
- stop at `READY_FOR_HUMAN_REVIEW` without performing Human review or granting approval,
  release, merge, canonical or deployment authority.

It intentionally does not compute a consciousness score or issue a phenomenal-experience conclusion.

See [`docs/FOUR_DOMAIN_AND_RESEARCH_QUALITY_CHAIN.md`](docs/FOUR_DOMAIN_AND_RESEARCH_QUALITY_CHAIN.md)
and the repository-level 2026-09-13 deepening report.
