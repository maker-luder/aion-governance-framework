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
- TEVV objective, intended use, and lifecycle stage;
- declared AI-risk references and metric-to-risk linkage;
- test-set and data-quality references;
- contamination and leakage checks;
- explicit oracle strategy for the AI test-oracle problem;
- metrics, methods, uncertainty references, and acceptance criteria;
- stochasticity / repetition / aggregation policy;
- evaluator identity, version, and independence;
- target context and similarity limitations;
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
