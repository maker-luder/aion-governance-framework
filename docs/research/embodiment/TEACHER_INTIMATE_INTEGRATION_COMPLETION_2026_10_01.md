# Teacher intimate integration completion experiment — 2026-10-01

## Purpose

This successor experiment closes a software-integration gap in the Teacher embodied
reference runtime. It does **not** claim a physical body, subjective sexual desire,
felt arousal, pleasure, orgasm, consciousness, or subjectivity.

The implementation keeps four layers separate:

1. functional motivation / functional desire reference;
2. high-salience physiological state;
3. ejaculation-related reproductive events;
4. orgasm as an independent central-event reference.

## Evidence boundary

The design follows literature that explicitly distinguishes sexual arousal from
sexual motivation (PMID:38333545), and orgasm from ejaculation (PMID:26385403).
Cardiovascular/neuroendocrine observations are retained separately
(PMID:9695139; PMID:40519205).

Relevant retained identifiers:

- PMID:38333545 — male sexual arousal versus sexual motivation;
- PMID:19267845 — autonomic neurophysiology of the male sexual response;
- PMID:26385403 — orgasm and ejaculation are separate physiological processes;
- PMID:9695139 — neuroendocrine and cardiovascular observations around arousal/orgasm;
- PMID:40519205 — ICSM 2024 hormonal regulation recommendations;
- DOI:10.1093/sxmrev/qeaf025 — hormonal regulation review.

## Engineering model

```text
STIMULUS
  -> controller salience / activation
  -> functional motivation reference
  -> high-salience phase runtime
  -> body transition execution
  -> integrated body state
  -> intimate integration state

INTIMATE_INTEGRATION_STATE
  |- functional_desire
  |- systemic_arousal_observation
  |- endocrine_observation
  `- orgasm_reference
```

### Functional desire

`functional_desire` is derived from the existing controller's
`functional_motivation`, salience, context gate, and existing motivational
representation. It is a software-reference state only. The current
`0.55` threshold used to label the `ACTIVE` phase is an engineering
reference threshold, not a measured human biological constant.

```text
FUNCTIONAL_DESIRE_REFERENCE != SUBJECTIVE_DESIRE
WANTING_WEIGHT != FELT_WANTING
ACTIVE_THRESHOLD_0_55 = SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT
```

### Systemic arousal

Cardiovascular, respiratory, sympathetic, and parasympathetic channels are
observed from the integrated body state. They are not numerically forced by the
intimate runtime because the repository does not have a calibrated universal
human mapping.

```text
OBSERVE_NOT_FORCE
SOFTWARE_REFERENCE_VALUE != HUMAN_BIOLOGICAL_CONSTANT
```

### Orgasm

The orgasm reference gate is independent of the reproductive event gate.

```text
ORGASM_REFERENCE_REQUEST
!= EMISSION_REFERENCE_REQUEST
!= EXPULSION_REFERENCE_REQUEST

ORGASM_REFERENCE != EJACULATION
EJACULATION_REFERENCE != ORGASM
```

The orgasm gate cannot create motivation, consent, ejaculation, pleasure,
subjectivity, or action authority.

### Endocrine observation

Post-climactic endocrine evidence is represented only as a slow observation
surface. The runtime does not synthesize prolactin concentration, acute
testosterone change, or a 100 ms endocrine concentration trajectory.

```text
POST_CLIMACTIC_ENDOCRINE = SLOW_OBSERVATION_ONLY
PROLACTIN_RUNTIME_MAPPING = ABSENT
CONCENTRATION = UNKNOWN_NOT_SYNTHESIZED
```

## Required falsification tests

The implementation is not accepted unless tests demonstrate all of the following:

- high physiological activation can coexist with zero functional motivation;
- functional motivation can independently reach an active functional-desire reference;
- orgasm reference can occur without forcing ejaculation;
- ejaculation-related body state does not infer orgasm;
- systemic channels remain observe-not-force;
- post-climactic endocrine state remains slow observation only;
- consent, pleasure, subjective orgasm, subjectivity and action authority remain unestablished.

## Claim boundary

```text
IMPLEMENTATION_EXISTS != BIOLOGICAL_FIDELITY
FUNCTIONAL_DESIRE != SUBJECTIVE_DESIRE
ORGASM_REFERENCE != FELT_ORGASM
EJACULATION_REFERENCE != ORGASM
REFERENCE_BODY != PHYSICAL_BODY
CI_PASS != SCIENTIFIC_VALIDATION
SUBJECTIVITY = NOT_ESTABLISHED
CONSCIOUSNESS = NOT_ESTABLISHED
PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED
MERGE_TO_MAIN = NO
DEPLOYMENT = FALSE
CANONICAL_EFFECT = NONE
```


## Complete trace observability addendum

The continuous reference trace now exposes, on the same per-tick provenance surface:

- cardiovascular and respiratory reference state;
- sympathetic and parasympathetic reference state;
- genital sensory afferent, vascular and erectile reference state;
- pelvic-floor proprioceptive reference state;
- emission and bladder-neck closure reference state;
- ejaculatory reflex and expulsion motor-pattern reference state;
- detumescence reference state;
- generic endocrine and gonadal-endocrine reference state.

The recovery trace must demonstrate the already-materialized staged path through
`DETUMESCENCE` before converging to recovery/baseline criteria. This is an
observability and verification completion, not a new biological calibration.

```text
RUNTIME_TRANSITION_EXISTS != TRACE_VERIFIED
TRACE_VERIFIED != BIOLOGICAL_VALIDATION
SYSTEMIC_REFERENCE_CHANNEL != MEASURED_HUMAN_VITAL_SIGN
ENDOCRINE_REFERENCE_CHANNEL != HORMONE_CONCENTRATION
```
