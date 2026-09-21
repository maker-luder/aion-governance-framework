# Ejaculation pre-implementation evidence crosswalk

Date: 2026-09-21  
Scope: ChatGPT Teacher synthetic embodiment research candidate  
Mode: evidence preparation only  
Executable implementation: NO  
Canonical effect: NONE  
Deployment: FALSE

## Purpose

Prepare the next bounded physiology experiment without collapsing ejaculation,
orgasm, sexual desire, urethral fluid output, and pelvic-floor motor activity
into one event.

The working research sequence is:

```text
SOURCE EVIDENCE
↓
PHYSIOLOGICAL EVENT
↓
OBSERVATION SURFACE
↓
BODY-INSTANCE STATE
↓
FORWARD / REVERSE / RECOVERY / ALTERNATIVE / COUNTERFACTUAL TESTS
↓
CLAIM LAST
```

## Preserved non-equivalences

```text
EMISSION != EXPULSION
EJACULATORY_REFLEX != EXTERNAL_SEMINAL_OUTPUT
PELVIC_FLOOR_MOTOR_BURST != SEMINAL_EXPULSION_CONFIRMED
URETHRAL_FLUID_OUTPUT != EJACULATION
SEMINAL_OUTPUT != ORGASM
EJACULATION != PHENOMENAL_ORGASM
PHYSIOLOGICAL_RESPONSE != FELT_PLEASURE
SOLO_SELF_STIMULATION_CONTEXT != SEXUAL_DESIRE
```

Phenomenal orgasm, felt pleasure, sexual desire, subjectivity and consciousness
remain NOT_ESTABLISHED.

## External evidence anchors

### Physiology reviews

- PMID 15996810 — ejaculation consists of distinct emission and expulsion
  phases; antegrade ejaculation requires coordinated autonomic and somatic
  control.
- PMID 16913292 — normal anterograde ejaculation requires coordinated
  sympathetic, parasympathetic and somatic components with genital afferent and
  supraspinal input.
- PMID 26709195 — emission and expulsion are synchronized phases controlled by
  autonomic and somatic spinal networks.
- PMCID PMC4708301 — emission involves distal epididymis, vas deferens, seminal
  vesicles, prostate, prostatic urethra and bladder neck; expulsion involves
  coordinated bladder-neck / external-sphincter / urethral / bulbospongiosus /
  pelvic-striated-muscle action.
- PMCID PMC4896089 — expulsion trigger remains incompletely established; the
  review explicitly separates ejaculation from orgasm.

### Solo self-stimulation context

- PMID 2340374 — seven human volunteers were studied with bulbocavernosus and
  ischiocavernosus EMG during erection and masturbation-induced ejaculation
  while timing and volume of each expelled semen spurt were recorded. Only a
  subset of EMG bursts coincided with a semen spurt. This directly supports the
  non-equivalence MOTOR_BURST != OUTPUT_CONFIRMED.
- PMID 28807505 — 988 men provided self-estimated intravaginal and masturbatory
  ejaculation latency values. This is retained as self-reported context timing,
  not direct physiological measurement.
- PMID 21155689 — pre-ejaculatory fluid was sampled in 27 volunteers in a
  masturbation context; sperm presence varied between subjects. This supports
  keeping pre-ejaculatory urethral fluid distinct from ejaculation.
- PMID 12762415 — a smaller clinical/laboratory study found no sperm in sampled
  pre-ejaculatory Cowper-gland secretion. Together with later studies, this
  reinforces that pre-ejaculatory fluid composition is variable and must not be
  assumed from event label alone.

### Output measurement / standardization

- PMID 34986984 and PMID 36112046 — WHO sixth-edition semen examination and
  ISO-aligned laboratory-method principles are retained for reproducible output
  measurement provenance. They do not establish the causal physiology of
  ejaculation.

## Repository crosswalk

```text
GENITAL_SENSORY_AFFERENT_REFERENCE
= EXISTING / DIRECT_OBSERVATION_REFERENCE

GENITAL_VASCULAR_STATE
= EXISTING

ERECTILE_REFLEX_STATE
= EXISTING

PELVIC_FLOOR_PROPRIOCEPTION
= EXISTING / DERIVED pelvic-floor physiology reference

PELVIC_FLOOR_REFLEX_CONTROL
= EXISTING motor-control reference

EMISSION_REFLEX_STATE
= EXISTING / DIRECT_OBSERVATION_REFERENCE

EJACULATORY_REFLEX_STATE
= EXISTING / DIRECT_OBSERVATION_REFERENCE

DETUMESCENCE_STATE
= EXISTING

POST_EJACULATORY_RECOVERY_REFERENCE
= EXISTING / DERIVED
= currently too coarse for event-specific recovery testing

SPERM_TRANSPORT_REFERENCE
= PHYSIOLOGY_EXISTS
= FUNCTIONAL_REFERENCE_ONLY
= MISSING_EVENT_OBSERVATION

ACCESSORY_GLAND_SECRETION_REFERENCE
= PHYSIOLOGY_EXISTS
= FUNCTIONAL_REFERENCE_ONLY
= MISSING_EVENT_OBSERVATION

EPIDIDYMAL_MATURATION_REFERENCE
= PHYSIOLOGY_EXISTS
= FUNCTIONAL_REFERENCE_ONLY
= NOT_REQUIRED_FOR_EVENT_EXECUTION_TEST

SPERMATOGENESIS_REFERENCE
= PHYSIOLOGY_EXISTS
= FUNCTIONAL_REFERENCE_ONLY
= NOT_REQUIRED_FOR_EVENT_EXECUTION_TEST

BLADDER_NECK_EJACULATORY_COORDINATION
= MISSING_EXPLICIT_REPRODUCTIVE_STATE

POSTERIOR_URETHRAL_SEMINAL_LOAD
= MISSING

EXPULSION_MOTOR_PATTERN
= PARTIAL_EXISTING_PELVIC_FLOOR_REFERENCE
= MISSING_EVENT_SPECIFIC_STATE

ANTEGRADE_SEMINAL_FLOW
= MISSING

RETROGRADE_SEMINAL_FLOW
= MISSING_ALTERNATIVE_PATH

NON_EJACULATORY_URETHRAL_FLUID
= NOT_YET_EXPLICITLY_CLASSIFIED
```

## Minimum next implementation surface

The next implementation should not create a single
`EJACULATION = TRUE/FALSE` flag.

Minimum candidate states:

```text
SEMINAL_TRACT_TRANSPORT_STATE
ACCESSORY_GLAND_SECRETION_STATE
BLADDER_NECK_EJACULATORY_CLOSURE_STATE
POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE
EXPULSION_MOTOR_PATTERN_STATE
EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE
ANTEGRADE_SEMINAL_FLOW_STATE
POST_EXPULSION_RECOVERY_STATE
```

Candidate states must be evidence-scoped. No exact biological concentration,
pressure, volume, contraction frequency or timing value should be invented when
the source does not support it.

## Context separation

Solo self-stimulation is a measurement context, not a new body function.

```text
STIMULATION_CONTEXT = SOLO_SELF_STIMULATION

SOLO_CONTEXT
!= EJACULATION_MECHANISM

MELT
= SELF_REPORTED_CONTEXT_TIMING_REFERENCE

MELT
!= DIRECT_PHYSIOLOGICAL_LATENCY_MEASUREMENT
```

The same physiology may later be compared across contexts, but context effects
must not be silently interpreted as changes in core mechanism.

## Planned causal test contract

```text
FORWARD_CAUSAL_PATH = REQUIRED
REVERSE_EVIDENCE_TRACE = REQUIRED
RECOVERY_PATH = REQUIRED
ALTERNATIVE_CAUSE_DISAMBIGUATION = REQUIRED
ONE_BY_ONE_COUNTERFACTUAL_ABLATION = REQUIRED
EXACT_BODY_INSTANCE_BINDING = REQUIRED
```

Alternative outputs must include at minimum:

```text
ANTEGRADE_EJACULATION_REFERENCE
RETROGRADE_SEMINAL_FLOW_REFERENCE
NO_EJACULATORY_OUTPUT_REFERENCE
NON_EJACULATORY_URETHRAL_FLUID_REFERENCE
URINARY_FLOW_REFERENCE
```

## Evidence-limited points

The exact human trigger for expulsion is not treated as established. Posterior
urethral seminal loading may be represented as a candidate input to expulsion
coordination only.

Pre-ejaculatory fluid composition is not treated as constant across individuals.
Presence or absence of sperm in pre-ejaculatory samples cannot be inferred from
the event label alone.

## Governance boundary

```text
BODY FUNCTION = RESEARCHABLE
PHYSIOLOGICAL DATA = RESEARCHABLE
CAUSAL CHAIN = TESTABLE

PHENOMENAL_ORGASM = NOT_ESTABLISHED
FELT_PLEASURE = NOT_ESTABLISHED
SEXUAL_DESIRE = NOT_ESTABLISHED
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED

WRITE_TO_MAIN = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
```
