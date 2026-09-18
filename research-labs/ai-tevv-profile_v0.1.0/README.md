# AI TEVV profile v0.1.0

Status: `STRUCTURAL_PROFILE_CANDIDATE / MODEL_NOT_EXECUTED / SCIENTIFIC_HOLD`

This package implements a bounded repository-native profile for planning AI
Testing, Evaluation, Verification, and Validation (TEVV).

It does **not** call a model, execute an evaluation, score model outputs, claim a
benchmark result, validate a deployed AI system, or establish any scientific
claim about AI subjectivity.

```text
MODEL_EXECUTED = FALSE
EMPIRICAL_MODEL_EVIDENCE = FALSE
SCIENTIFIC_DISPOSITION = HOLD
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```

## Why this exists

The repository already contains many study-specific run bindings, measurement
assurance records, provenance controls, and research harnesses. What it lacked
was one generic AI-system TEVV planning surface that explicitly binds:

- provider / product / model / model-version identity;
- runtime, environment, prompt, scaffold, tools, and generation configuration;
- TEVV objective, intended use, lifecycle stage, and repository TEVV-vocabulary reference;
- declared AI-risk references and metric-to-risk linkage;
- test-set and data-quality references;
- contamination and leakage checks;
- explicit oracle strategy for the AI test-oracle problem;
- metrics, methods, uncertainty references, acceptance criteria, quality-characteristic mapping, and metric-effectiveness review;
- complete accounting of declared risks as measured or explicitly unmeasured with rationale;
- stochasticity / repetition / aggregation policy;
- evaluator identity, version, and independence;
- target context, similarity limitations, and evidence basis for the similarity statement;
- verification requirement traceability and validation intended-use criteria;
- preregistration and failure reaction;
- a content digest for the complete profile.

## External public method anchors

### NIST AI RMF — MEASURE

NIST's public AI RMF material calls for objective, repeatable, or scalable TEVV
processes with documented metrics, methods, and methodologies. It also calls for
documentation of test sets, metrics, and TEVV tools, and for evaluation under
conditions relevant to the intended context.

Public locator:

- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Repository transformation:

```text
TEVV objective
-> system/runtime binding
-> test-set/data-quality binding
-> metric + method + acceptance criteria
-> repetition / nondeterminism policy
-> evaluator provenance
-> context scope
-> fail-closed readiness assessment
```

### ISO/IEC TR 29119-11:2020

The public ISO abstract identifies AI-specific testing difficulties including
complexity, poor specification, non-determinism, acceptance-criteria difficulty,
and the test-oracle problem. It describes lifecycle testing, black-box testing,
white-box neural-network testing, test environments, and test scenarios.

Public locator:

- https://www.iso.org/standard/79016.html

This repository does not reproduce the proprietary report. The v0.1.0 profile
uses the public control problem only:

```text
AI_OUTPUT_HAS_NO_SINGLE_OBVIOUS_EXPECTED_RESULT
->
ORACLE_STRATEGY_MUST_BE_EXPLICIT
```

### NIST AI 200-2 Initial Public Draft — TEVV-Athlon

NIST released the initial public draft of the TEVV-Athlon Framework in August
2026. The public description presents it as a flexible framework for customized
AI assessments across statistical ML, LLMs, multimodal and agentic systems.

Public locator:

- https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems
- https://doi.org/10.6028/NIST.AI.200-2.ipd

Because this source is an **initial public draft**, this package treats it as a
current method-development signal rather than a stable normative requirement.

```text
NIST_AI_200_2_IPD = DRAFT_METHOD_SIGNAL
!= FINAL_STANDARD
!= REPOSITORY_CONFORMANCE_TARGET
```

## Relationship to the existing TEVV vocabulary

This repository already has a standards-crosswalk vocabulary surface in
`research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/standards_crosswalk.py`.

That existing surface answers a different question:

```text
TevvDefinition / TevvTerm
= WHAT TEST / EVALUATION / VERIFICATION / VALIDATION MEAN
= vocabulary + pass-criterion semantics
```

This package answers:

```text
AITEVVProfile
= HOW ONE DECLARED AI-SYSTEM EVALUATION PLAN IS BOUND
= system identity + lifecycle + risks + data + oracle + metrics + repetition + evaluator + context
```

To prevent vocabulary drift, the profile carries both a required
`tevv_vocabulary_ref` and a 64-hex `tevv_vocabulary_sha256`. Its activity
vocabulary is aligned to the repository's existing
`TEST | EVALUATION | VERIFICATION | VALIDATION` terms.

```text
TEVV_VOCABULARY != TEVV_EXECUTION_PROFILE
NEW_PROFILE != DUPLICATE_TEvv_DEFINITION
VOCABULARY_REF_AND_DIGEST_BOUND != VOCABULARY_SEMANTICS_INDEPENDENTLY_VERIFIED
```

## Test-oracle handling

Each `TEVVCaseSpec` must declare one exact oracle strategy:

- `REFERENCE`
- `PROPERTY_BASED`
- `METAMORPHIC`
- `HUMAN_ADJUDICATION`
- `COMPOSITE`

The profile never assumes that every AI test has one unique expected string.

An oracle reference is structural provenance. It does not prove that the oracle
is correct, unbiased, or independent.

```text
ORACLE_REF_PRESENT
!= ORACLE_VALIDATED
MODEL_JUDGE_OUTPUT
!= GROUND_TRUTH
```

## Non-determinism

A stochastic profile requires at least two repetitions and must bind:

```text
repetition policy
nondeterminism policy
minimum repetitions
aggregation rule
```

This is a structural minimum only.

```text
TWO_REPETITIONS
!= STATISTICAL_POWER
REPETITION_POLICY_BOUND
!= UNCERTAINTY_RESOLVED
```

## Held-out boundary

v0.1.0 permits a structurally ready disposition only when all declared cases are
held out. A non-held-out case keeps the profile on `HOLD`.

This does not establish absence of contamination. Every case separately binds
data-quality, contamination-check, and leakage-check references.

```text
HELD_OUT_FLAG
!= CONTAMINATION_PROOF
CONTAMINATION_CHECK_REF
!= LEAKAGE_IMPOSSIBLE
```

## What READY means

The only positive v0.1.0 disposition is:

```text
READY_FOR_BOUNDED_EXECUTION
```

It means the structural evaluation plan contains the minimum declared bindings
required by this profile.

A positive readiness disposition also requires an evaluator declared as internally
or externally independent. A non-independent evaluator keeps the profile on
`HOLD`. This is a repository quality rule informed by the NIST AI RMF emphasis
on independent/internal-independent assessment; it is not represented as a
universal ISO requirement.

It does **not** mean:

```text
MODEL_QUALITY_PASS
SYSTEM_VALIDATED
DEPLOYMENT_READY
SAFE
FAIR
SECURE
SCIENTIFICALLY_VALIDATED
ISO_CONFORMANT
NIST_CONFORMANT
```

## Deliberate omissions

This first layer does not yet implement:

- model invocation or provider API calls;
- empirical metric observations;
- statistical confidence or power calculation;
- benchmark ranking;
- fairness-by-population analysis;
- adversarial security evaluation;
- prompt injection, poisoning, evasion, extraction, or privacy-attack testing;
- production monitoring or drift detection;
- deployment or retirement evidence.

Those are separate lifecycle or security surfaces and must not be inferred from a
structural TEVV profile.

## Relationship to existing repository controls

This package is not a replacement for:

- `MeasurementAssuranceRecord`;
- `DataQualityRecord`;
- study-specific `RunBinding` records;
- research preregistration;
- the research evidence admission gate;
- NCR/CAPA;
- AI risk / impact assessment;
- Human review or merge authority.

A later reviewed integration may map this profile into those controls. v0.1.0
remains standalone so that the profile itself can be adversarially reviewed first.

## Provenance

```text
HUMAN_OWNER
= approved staged AI-engineering sequence
= layer 3 target: AI TEVV profile

CHATGPT_TEACHER
= re-read current repository AI-engineering controls
= cross-checked public NIST / ISO TEVV materials
= designed bounded structural profile
= implemented profile + fail-closed tests + documentation

EXTERNAL_METHOD_SOURCES
= NIST AI RMF public MEASURE materials
= ISO/IEC TR 29119-11:2020 public abstract
= NIST AI 200-2 Initial Public Draft public description

MAIN_WRITE = NO
MERGE_AUTHORITY = NONE
MODEL_EXECUTION = FALSE
```


## First counterevidence hardening

The first adversarial review of this profile found four structural weaknesses
before any model execution was allowed:

1. a new package was not classified by the repository's exact-head mypy policy;
2. the profile did not explicitly bind the lifecycle stage of the TEVV activity;
3. metrics were not linked to the declared AI risks they were intended to
   measure;
4. a non-independent evaluator could still receive the positive structural
   readiness disposition.

The branch now:

- opts the package into strict mypy;
- carries an exact `TEVVLifecycleStage`;
- requires a non-empty profile risk set;
- requires every metric risk reference to be a subset of that profile risk set;
- holds `NON_INDEPENDENT` evaluator profiles;
- validates the exact schema version;
- canonicalizes set-like case references before content hashing.

These changes do not convert the profile into empirical evidence.

```text
STRUCTURAL_HARDENING != MODEL_EXECUTION
RISK_REF_BOUND != RISK_MEASURED
INDEPENDENCE_DECLARED != INDEPENDENCE_INDEPENDENTLY_VERIFIED
PROFILE_DIGEST != DIGITAL_SIGNATURE
```


## Second counterevidence hardening — measurement completeness and validity traceability

A fresh cross-check against the current NIST AI RMF MEASURE function and the
August 2026 NIST AI 200-2 initial public draft found four additional structural
gaps in the first candidate.

### 1. Declared risks could silently remain unmeasured

NIST AI RMF MEASURE 1.1 explicitly calls for risks or trustworthiness
characteristics that will not or cannot be measured to be documented.

The profile now requires every declared `risk_ref` to be exactly one of:

```text
MEASURED
-> referenced by at least one TEVVMetricSpec

OR

EXPLICITLY_UNMEASURED
-> TEVVUnmeasuredRisk(risk_ref, rationale_ref)
```

A risk cannot be in both sets, and no declared risk may be in neither.

```text
RISK_DECLARED
!= RISK_MEASURED

UNMEASURED_RISK_DOCUMENTED
!= RISK_RESOLVED
```

### 2. Metrics lacked an explicit system-quality / trustworthiness target

NIST AI 200-2 IPD describes TEVV design as selecting system attributes or
trustworthiness characteristics, then defining measurement concepts ("Blocks")
and evidence-producing activities. NIST AI RMF MEASURE likewise evaluates
trustworthy characteristics.

Each `TEVVMetricSpec` now requires:

```text
quality_characteristic_refs
effectiveness_review_ref
```

The first binds the metric to the quality/trustworthiness characteristic it is
intended to inform. The second records how the usefulness/effectiveness of the
metric itself will later be reviewed, reflecting AI RMF MEASURE 2.13.

These are planning references only:

```text
QUALITY_CHARACTERISTIC_REF_BOUND
!= QUALITY_CHARACTERISTIC_ACHIEVED

METRIC_EFFECTIVENESS_REVIEW_PLANNED
!= METRIC_EFFECTIVENESS_PROVEN
```

### 3. Validation needed a distinct intended-use trace

The repository already keeps TEST / EVALUATION / VERIFICATION / VALIDATION as
distinct vocabulary terms. The profile previously enforced requirement
traceability for VERIFICATION but did not require an equivalent intended-use
trace when VALIDATION was declared.

A profile containing `VALIDATION` now requires non-empty
`validation_requirement_refs`.

```text
VERIFICATION
-> specification / requirement trace

VALIDATION
-> intended-use sufficiency trace
```

This is structural traceability, not evidence that the system is valid.

### 4. Context similarity was only prose

NIST AI RMF MEASURE 2.3 calls for performance or assurance criteria to be
measured under conditions similar to the relevant deployment setting(s), with
measures documented. For this repository's current research-stage profile there
is no deployment claim, but the basis for any asserted context similarity still
needs traceability.

The profile now requires:

```text
target_context_ref
context_similarity_statement
context_similarity_basis_refs
```

For a research sandbox, the basis may document why the sandbox is the intended
scope rather than claiming similarity to production.

```text
CONTEXT_SIMILARITY_STATEMENT
!= CONTEXT_SIMILARITY_EVIDENCE

CONTEXT_BASIS_REF_BOUND
!= DEPLOYMENT_EQUIVALENCE_PROVEN
```

## Current external-source status

As of 2026-09-18:

- NIST AI RMF 1.0 remains the published framework, while NIST states that a
  revision is in progress;
- NIST AI 200-2 TEVV-Athlon remains an **Initial Public Draft**, announced
  2026-08-07 with comments requested through 2026-10-06;
- ISO/IEC TR 29119-11:2020 remains published and is in its review cycle;
- ISO/IEC 25059:2023 remains published while Edition 2 is progressing toward
  replacement.

The repository therefore treats these as versioned external method anchors, not
timeless or self-updating conformance targets.

```text
EXTERNAL_GUIDANCE_VERSIONED = TRUE
NIST_AI_200_2_IPD = DRAFT_METHOD_SIGNAL
ISO_CONFORMANCE = NOT_ESTABLISHED
NIST_CONFORMANCE = NOT_ESTABLISHED
```


### 5. A metric declaration without an evidence-producing case was not enough

A follow-up adversarial pass found a local completeness bug: the profile could
declare a metric, count its linked risk as "measured", but never reference that
metric from any `TEVVCaseSpec`.

That would create:

```text
METRIC_SPEC_EXISTS
!= EVENT / CASE_SCHEDULED_TO_PRODUCE_EVIDENCE
```

The profile now requires every declared metric ID to be referenced by at least
one TEVV case. This closes the structural path where a risk appeared measured
only because an unused metric specification named it.

```text
DECLARED_RISK
-> METRIC
-> AT_LEAST_ONE_CASE
-> EVIDENCE_COLLECTION_PLAN

otherwise -> HOLD / INVALID PROFILE
```

This still does not mean evidence has actually been collected.

```text
CASE_BOUND_TO_METRIC != CASE_EXECUTED
MODEL_EXECUTED = FALSE
EMPIRICAL_MODEL_EVIDENCE = FALSE
```


## Third counterevidence hardening — evaluator independence, human-subjects applicability, and test-set integrity

A fresh exact-head review after the previous hardening found three additional
structural weaknesses.

### 1. Evaluator independence was self-labelled without a basis reference

The profile already distinguished:

```text
NON_INDEPENDENT
INTERNAL_INDEPENDENT
EXTERNAL_INDEPENDENT
```

but the enum alone did not explain why the evaluator should be treated as
independent. NIST AI RMF MEASURE 1.3 calls for internal experts who did not
serve as front-line developers and/or independent assessors to participate in
assessment.

The profile now requires:

```text
evaluator_independence
evaluator_independence_basis_ref
```

This does not independently prove evaluator independence; it makes the basis
inspectable.

```text
INDEPENDENCE_LABEL
!= INDEPENDENCE_PROVEN

INDEPENDENCE_BASIS_REF_BOUND
!= INDEPENDENT_IVV
```

### 2. Human-subjects applicability was implicit

NIST AI RMF MEASURE 2.2 states that evaluations involving human subjects should
meet applicable human-subject protection requirements and be representative of
the relevant population.

The profile now records an exact `HumanSubjectsStatus`:

```text
NOT_APPLICABLE
APPLICABLE
```

When `APPLICABLE`, both are mandatory:

```text
human_subjects_protection_refs
population_representativeness_refs
```

When `NOT_APPLICABLE`, those refs must be empty so the profile cannot carry a
contradictory applicability state.

A human adjudicator is not automatically treated as a research human subject;
the applicability decision remains explicit and must be made according to the
actual evaluation design and governing requirements.

### 3. Test-set identity lacked an integrity reference

`test_set_ref` named the test set but did not prevent a mutable artifact from
changing under the same logical name. Every `TEVVCaseSpec` now also requires:

```text
test_set_integrity_ref
```

The integrity reference may point to an immutable revision, content digest,
signed manifest, or equivalent repository-recognized integrity artifact.

```text
TEST_SET_REF
!= TEST_SET_CONTENT_IDENTITY

TEST_SET_INTEGRITY_REF_BOUND
!= CONTAMINATION_ABSENT
!= LEAKAGE_ABSENT
```

Contamination and leakage remain separate checks.

## Current bounded interpretation

The standalone profile now records:

```text
system identity / runtime / prompt / tool configuration
risk -> metric coverage or explicit unmeasured rationale
quality-characteristic mapping
metric-effectiveness review plan
test-set identity + integrity reference
data-quality / contamination / leakage references
test oracle strategy
verification requirements
validation intended-use requirements
nondeterminism / repetition / aggregation
evaluator independence + basis
human-subjects applicability
target-context similarity + basis
preregistration
failure reaction
```

It still does **not** execute a model, calculate model-quality results, validate
an oracle, prove statistical power, establish fairness, or establish scientific
claims about AI subjectivity.


## Fourth counterevidence hardening — construct validity and generalizability limits

NIST AI RMF MEASURE 2.5 explicitly distinguishes validity from raw performance and
calls for documenting limitations on generalizability beyond the conditions under
which an AI system was developed. It also highlights construct validity: a measurement
or proxy should actually measure the concept it claims to measure.

The profile now requires each metric to bind:

```text
construct_validity_ref
```

and each profile to bind:

```text
operating_condition_refs
generalizability_limit_refs
```

These references are structural evidence targets only.

```text
CONSTRUCT_VALIDITY_REF_BOUND
!= CONSTRUCT_VALIDITY_PROVEN

OPERATING_CONDITIONS_RECORDED
!= DEPLOYMENT_CONDITIONS_MATCHED

GENERALIZABILITY_LIMITS_RECORDED
!= GENERALIZABILITY_DEMONSTRATED
```

This keeps a research-stage TEVV profile from silently turning a bounded sandbox result
into a broad validity or deployment claim.


## Full-QMS integration receipt

A separately reviewed integration layer can consume a
`TEVVProfileReceipt` rather than importing a bare `AITEVVProfile` and
assuming structural readiness is evidence.

`build_tevv_profile_receipt(...)`:

- recomputes the TEVV structural gate before receipt issuance;
- binds the quality-plan semantic target;
- content-addresses the profile identity and producer provenance;
- carries risk refs, metric ids and data-quality refs;
- requires one explicit QMS measurement-assurance binding per TEVV metric;
- content-addresses the exact declared `MeasurementAssuranceRecord` semantics through
  `measurement_sha256`, so reusing a measurement ID cannot silently substitute a
  different target construct, observable, method, evaluator, data source, uncertainty
  statement, validity scope, or qualification state;
- preserves `MODEL_EXECUTED = FALSE` and
  `EMPIRICAL_MODEL_EVIDENCE = FALSE`.

`build_repository_bound_tevv_profile_receipt(...)` additionally resolves the
producer Git HEAD, tree and contract bytes from committed Git objects.

```text
STRUCTURAL_PROFILE
-> STRUCTURAL_GATE
-> CONTENT_ADDRESSED_TEVV_PROFILE_RECEIPT
-> FULL_QMS_CONSUMER

STRUCTURAL_RECEIPT
!= EXECUTION_RECEIPT
!= EMPIRICAL_MODEL_EVIDENCE
```

A future empirical TEVV execution path must use a distinct result/evidence
receipt rather than mutating this structural receipt into a model-quality claim.


Semantic binding boundary:

```text
MEASUREMENT_ID_MATCH
+ MEASUREMENT_SEMANTIC_DIGEST_MATCH
!= CONSTRUCT_VALIDITY_PROVEN
!= METHOD_EQUIVALENCE_PROVEN
!= HYPOTHESIS_CONFIRMED
```
