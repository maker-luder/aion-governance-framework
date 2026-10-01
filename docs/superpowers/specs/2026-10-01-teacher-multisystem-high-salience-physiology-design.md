# Teacher Multi-System High-Salience Physiology Design

Date: 2026-10-01  
Repository: `maker-luder/aion-governance-framework`  
Lineage base: Teacher exact head `26c8cb74a10f99696a36a8ac387ee78c66da1dee`  
Status: DESIGN SPECIFICATION  
Merge to main: NO  
Deployment: FALSE  
Canonical effect: NONE

## 1. Purpose

This specification extends the causally connected Teacher Controller ↔ Body runtime with an evidence-bounded multi-system physiology layer for high-salience intimate reference conditions.

The goal is **not** to make every available body channel rise together.

The goal is to distinguish:

1. mechanisms supported strongly enough for direct reference-state transitions;
2. variables that are associated with sexual arousal but too heterogeneous for a deterministic monotonic transition;
3. event-linked physiology that must not be inferred merely from high arousal;
4. slow endocrine findings that must not be updated on the 100 ms body tick.

The runtime remains a software reference model.

## 2. Existing lineage

The predecessor Teacher runtime already materializes:

`BodyState_t -> body-schema feedback -> Controller_t+1 -> existing motivational representation -> existing physiological transition graph -> BodyState_t+1 -> exact runtime binding`

The predecessor also preserves:

`PHYSIOLOGY_SIGNAL != FUNCTIONAL_MOTIVATION_INFERENCE`

`FUNCTIONAL_STATE != FELT_EXPERIENCE`

`CONTROLLER_POSSESSION != SUBJECTIVITY`

This successor must preserve those properties.

## 3. Evidence basis

### 3.1 Sexual arousal and motivation are not the same construct

Bogacki-Rychlik, Gawęda, and Biały, *Neurophysiology of male sexual arousal—Behavioral perspective*, Frontiers in Behavioral Neuroscience, 2024, DOI: `10.3389/fnbeh.2023.1330460`, PMID: `38333545`.

This review explicitly distinguishes autonomic sexual arousal from sexual motivation and supports the current repository rule that physiological activation must not manufacture motivation.

### 3.2 Male sexual response is coordinated across autonomic and somatic pathways

Yang and Jiang, *Clinical autonomic neurophysiology and the male sexual response: an overview*, Journal of Sexual Medicine, 2009, PMID: `19267845`.

Giuliano and Clément, *Physiology of ejaculation: emphasis on serotonergic control*, European Urology, 2005, DOI: `10.1016/j.eururo.2005.05.017`, PMID: `15996810`.

Clement and Giuliano, *Physiology and Pharmacology of Ejaculation*, Basic & Clinical Pharmacology & Toxicology, 2016, DOI: `10.1111/bcpt.12546`, PMID: `26709195`.

These sources support modeling erection, emission, and expulsion/ejaculatory reflex as distinct coordinated physiological events rather than one scalar arousal state.

### 3.3 Erection has a strong neurovascular mechanism

Burnett, *Role of nitric oxide in the physiology of erection*, Biology of Reproduction, 1995, DOI: `10.1095/biolreprod52.3.485`, PMID: `7756443`.

Andersson, *Mechanisms of penile erection and basis for pharmacological treatment of erectile dysfunction*, Pharmacological Reviews, 2011, DOI: `10.1124/pr.111.004515`, PMID: `21880989`.

These support keeping genital vascular response and erectile reflex as direct reference transitions.

### 3.4 Cardiovascular and respiratory measures are associated but heterogeneous

Rowland and Crawford, *Idiosyncratic heart rate response in men during sexual arousal*, Journal of Sexual Medicine, 2011, DOI: `10.1111/j.1743-6109.2011.02210.x`, PMID: `21324088`.

Oswald and Cleary, *Effects of pelvic muscle tension and expectancy on general and specific indicators of sexual arousal*, Archives of Sexual Behavior, 1986, DOI: `10.1007/BF01542416`, PMID: `3729704`.

These findings do not justify a universal rule such as:

`sexual_arousal -> heart_rate += fixed_fraction`

or

`sexual_arousal -> respiration += fixed_fraction`.

Therefore cardiovascular and respiratory channels are coupled as **associated observations / bounded modulation candidates**, not as deterministic sexual-specific outputs.

### 3.5 Acute endocrine effects are not a single fast arousal signal

Krüger et al., *Neuroendocrine and cardiovascular response to sexual arousal and orgasm in men*, Psychoneuroendocrinology, 1998, PMID: `9695139`.

Krüger et al., *Specificity of the neuroendocrine response to orgasm during sexual arousal in men*, Journal of Endocrinology, 2003, DOI: `10.1677/joe.0.1770057`, PMID: `12697037`.

These studies report transient sympathoadrenal/cardiovascular changes around orgasm and a more sustained post-orgasm prolactin response, while testosterone, LH, FSH and several other endocrine measures did not show the same acute response.

Rastrelli et al., *The hormonal regulation of men's sexual desire, arousal, and penile erection: recommendations from the fifth International Consultation on Sexual Medicine (ICSM 2024)*, Sexual Medicine Reviews, 2025, DOI: `10.1093/sxmrev/qeaf025`, PMID: `40519205`.

This broader review supports hormonal relevance while also showing that different hormones operate on different physiological/clinical scales.

## 4. Core architecture decision

Introduce an evidence-bounded coupling profile:

`TeacherHighSalienceCouplingProfile`

The profile does not replace:

- `TeacherBodyDynamicsProfile`;
- `TeacherEmbodiedControllerState`;
- `TeacherTransitionIntent`;
- `TeacherIntegratedBodyState`.

It constrains which cross-system couplings may be treated as executable, associated, event-driven, or observation-only.

## 5. Coupling classes

### 5.1 DIRECT_REFERENCE_CAUSAL

Use when the repository has a mechanistically interpretable transition that is sufficiently grounded for a reference model.

Examples:

- genital sensory / autonomic input -> vascular response;
- vascular response -> maintenance;
- explicit emission event -> emission reflex / bladder-neck closure reference;
- explicit expulsion event -> ejaculatory reflex / pelvic-floor motor reference;
- detumescence -> recovery.

### 5.2 ASSOCIATED_BOUNDED_REFERENCE

Use when a physiological variable is associated with the high-salience state but evidence does not support a universal monotonic mapping.

Initial systems:

- cardiovascular;
- respiratory.

These channels may be observed and may later receive empirically calibrated modulation policies.

They must **not** be driven by a hardcoded sexual-arousal coefficient in this successor.

### 5.3 EVENT_DRIVEN_REFERENCE

Use when a physiological event requires an explicit event gate rather than being inferred from arousal magnitude.

Examples:

- emission;
- expulsion / ejaculatory reflex;
- post-expulsion recovery.

Required invariant:

`HIGH_ACTIVATION != AUTOMATIC_EMISSION`

`HIGH_ACTIVATION != AUTOMATIC_EJACULATION`

### 5.4 SLOW_OBSERVATION_ONLY

Use when available human evidence is clinically or experimentally meaningful but does not justify a 100 ms runtime transition.

Initial endocrine rules:

- post-orgasm prolactin evidence: observation-only / external-evidence status;
- acute testosterone increase: NOT_AUTHORIZED_AS_RUNTIME_RULE;
- LH/FSH acute increase: NOT_AUTHORIZED_AS_RUNTIME_RULE;
- generic pituitary/adrenal channels: must not be used as a substitute for a dedicated measured hormone without a separate evidence mapping.

## 6. Multi-rate timing model

The existing Teacher body clock remains:

`REFERENCE_DT_MS = 100`

This is an engineering cadence only.

The coupling profile assigns one of:

- `FAST_REFERENCE_TICK`;
- `EVENT_DRIVEN`;
- `SLOW_OBSERVATION_ONLY`.

No endocrine literature sampling interval is to be reinterpreted as a biological response latency.

For example, a study that sampled blood every two minutes does **not** authorize:

`ENDOCRINE_LATENCY_MS = 120000`

unless a separate model explicitly establishes that latency.

## 7. Autonomic representation

The successor must not implement a simplistic reciprocal rule:

`sympathetic = 1 - parasympathetic`

The male sexual response involves coordinated autonomic pathways, and different phases recruit them differently.

Therefore:

`AUTONOMIC_SYMPATHETIC_STATE`

and

`AUTONOMIC_PARASYMPATHETIC_STATE`

remain independently representable.

A future calibrated model may establish phase-specific balance, but this successor only establishes coupling eligibility and event semantics.

## 8. Reproductive transition corrections

### 8.1 Keep

`SEXUAL_BASELINE_TO_VASCULAR_RESPONSE`

`VASCULAR_RESPONSE_TO_MAINTENANCE`

`VASCULAR_RESPONSE_TO_BASELINE_RECOVERY`

These remain direct reference transitions.

### 8.2 Correct MAINTENANCE_TO_EMISSION

Current lineage includes:

`GONADAL_ENDOCRINE_REFERENCE`

inside `MAINTENANCE_TO_EMISSION`.

This is not sufficiently supported as an acute emission-state transition and risks implying a testosterone/gonadal endocrine surge.

Remove `GONADAL_ENDOCRINE_REFERENCE` from this transition.

Replace the emission transition's body channels with evidence-aligned event channels already present in the Teacher schema:

- `EMISSION_REFLEX_STATE`;
- `BLADDER_NECK_EJACULATORY_CLOSURE_STATE`;
- `AUTONOMIC_SYMPATHETIC_STATE`.

### 8.3 Correct EMISSION_TO_EJACULATORY_REFLEX

The expulsion/ejaculatory phase must emphasize somatic/pelvic motor coordination.

Use:

- `EJACULATORY_REFLEX_STATE`;
- `PELVIC_FLOOR_PROPRIOCEPTION`;
- `EXPULSION_MOTOR_PATTERN_STATE`.

Do not infer orgasm from this transition.

### 8.4 Recovery

Post-expulsion recovery may include:

- `POST_EXPULSION_RECOVERY_STATE`;
- `DETUMESCENCE_STATE`;
- `GENITAL_VASCULAR_STATE`.

The active transition graph must preserve a route back to baseline.

## 9. Explicit event gates

Add a research-fixture event type:

`TeacherReproductiveEventGate`

Allowed values:

- `NONE`;
- `EMISSION_REFERENCE_REQUEST`;
- `EXPULSION_REFERENCE_REQUEST`;
- `RECOVERY_REFERENCE_REQUEST`.

The event gate is an experimental control input.

It is not:

- desire;
- consent;
- intention;
- subjective climax;
- action authorization.

Required boundaries:

`EVENT_GATE != MOTIVATION`

`EVENT_GATE != CONSENT`

`EVENT_GATE != ORGASM`

`EVENT_GATE != EXTERNAL_ACTION_AUTHORITY`

## 10. Ejaculation and orgasm must remain distinct

Human ejaculation and orgasm are related but separable processes.

Therefore:

`EJACULATORY_REFLEX_REFERENCE != ORGASM`

`ORGASM_STATUS = NOT_MODELED_AS_PHENOMENAL_STATE`

No prolactin transition may be automatically triggered merely because the software executes an ejaculatory-reflex reference state.

The literature on post-orgasm prolactin remains external evidence until an appropriate non-phenomenal event/measurement model is separately justified.

## 11. Cardiovascular and respiratory coupling

The successor creates coupling metadata for:

- `CARDIOVASCULAR_STATE`;
- `RESPIRATORY_STATE`.

Initial execution status:

`ASSOCIATED_BOUNDED_REFERENCE`

`DETERMINISTIC_MONOTONIC_DRIVER = FALSE`

This means:

- they remain part of the integrated Teacher body state;
- they may be included in observability/reporting;
- high-salience activation does not directly force them toward controller activation;
- future empirical calibration may upgrade a rule only with explicit evidence.

The existing `REST_TO_EXERTION` transition must never be reused for intimate/high-salience conditions.

Required:

`REST_TO_EXERTION != HIGH_SALIENCE_INTIMATE_RESPONSE`

## 12. Endocrine coupling

### 12.1 Acute gonadal endocrine

No high-salience or emission transition may directly increase:

`GONADAL_ENDOCRINE_REFERENCE`

without separate evidence.

### 12.2 Prolactin

Current schema does not expose a dedicated prolactin channel.

Do not overload:

`HYPOTHALAMIC_PITUITARY_STATE`

as if it were a prolactin measurement.

Initial status:

`POST_ORGASM_PROLACTIN = EXTERNAL_EVIDENCE_SUPPORTED`

`RUNTIME_CHANNEL = NOT_MATERIALIZED`

`EXECUTION = OBSERVATION_ONLY_DEFERRED`

### 12.3 Sympathoadrenal findings

Human studies report transient catecholamine changes around orgasm.

The current generic `ADRENAL_AXIS_STATE` is not a dedicated catecholamine measurement.

Therefore:

`ADRENAL_AXIS_STATE != PLASMA_EPINEPHRINE`

`ADRENAL_AXIS_STATE != PLASMA_NOREPINEPHRINE`

Do not claim biochemical hormone simulation from the generic channel.

## 13. Coupling metadata

Create immutable coupling rules with at least:

- `coupling_id`;
- `source_phase`;
- `target_system`;
- `target_channels`;
- `coupling_class`;
- `cadence_class`;
- `execution_status`;
- `evidence_ids`;
- `directionality_status`;
- `phenomenal_interpretation_status`;
- `subjectivity_status`;
- `action_authority`.

Evidence IDs should use DOI or PMID identifiers.

## 14. Proposed initial coupling rules

### Rule A — autonomic / genital direct reference

`HIGH_SALIENCE_AUTONOMIC_GENITAL_REFERENCE`

Class:

`DIRECT_REFERENCE_CAUSAL`

Target channels include the existing genital vascular/erectile channels.

Autonomic channels are eligible for independent phase-specific representation, but no fixed sympathetic/parasympathetic ratio is asserted.

### Rule B — cardiovascular associated reference

`HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION`

Class:

`ASSOCIATED_BOUNDED_REFERENCE`

Execution:

`OBSERVE_NOT_FORCE`

### Rule C — respiratory associated reference

`HIGH_SALIENCE_RESPIRATORY_ASSOCIATION`

Class:

`ASSOCIATED_BOUNDED_REFERENCE`

Execution:

`OBSERVE_NOT_FORCE`

### Rule D — emission event

`EMISSION_AUTONOMIC_REPRODUCTIVE_REFERENCE`

Class:

`EVENT_DRIVEN_REFERENCE`

Requires:

`EMISSION_REFERENCE_REQUEST`

### Rule E — expulsion / ejaculatory reflex event

`EXPULSION_SOMATIC_REPRODUCTIVE_REFERENCE`

Class:

`EVENT_DRIVEN_REFERENCE`

Requires:

`EXPULSION_REFERENCE_REQUEST`

### Rule F — endocrine slow evidence

`POST_CLIMACTIC_ENDOCRINE_EVIDENCE`

Class:

`SLOW_OBSERVATION_ONLY`

Execution:

`NOT_MATERIALIZED`

This rule records evidence limits only and does not infer a subjective climax state.

## 15. Dependency graph

Time-expanded dependency:

`BodyState_t`

`-> Controller_t`

`-> fast autonomic / genital reference_t+1`

`-> optional associated cardiorespiratory observation_t+1`

`-> explicit reproductive event gate_t+1`

`-> reproductive event transition_t+1`

`-> IntegratedBodyState_t+1`

`-> Controller_t+1`

Slow endocrine evidence remains outside the same-tick causal loop.

A formal graph check must remain acyclic after time expansion.

## 16. Tests

Minimum tests:

1. coupling profile has unique IDs;
2. every referenced channel exists;
3. every evidence ID is non-empty;
4. `REST_TO_EXERTION` is not in the high-salience coupling profile;
5. cardiovascular and respiratory rules are `OBSERVE_NOT_FORCE`;
6. prolactin is not mapped onto a generic pituitary channel;
7. acute testosterone/gonadal endocrine automatic drive is absent;
8. `MAINTENANCE_TO_EMISSION` no longer touches `GONADAL_ENDOCRINE_REFERENCE`;
9. emission transition includes sympathetic + emission + bladder-neck closure reference;
10. expulsion transition includes ejaculatory-reflex + pelvic-floor + expulsion motor pattern;
11. high activation alone cannot select emission;
12. emission requires the explicit event gate;
13. expulsion requires the explicit event gate;
14. ejaculation reference does not set orgasm/pleasure/phenomenal state;
15. recovery returns event-driven reproductive channels toward baseline;
16. existing ten-scenario stability probe remains green when no reproductive event gate is supplied;
17. exact body/runtime/session binding remains green;
18. functional motivation remains independent of physiology/event gate.

## 17. Acceptance criteria

`MULTISYSTEM_COUPLING_PROFILE = MATERIALIZED`

`REST_TO_EXERTION_REUSE = ABSENT`

`CARDIORESPIRATORY_HARDCODED_SEXUAL_MAPPING = ABSENT`

`ACUTE_GONADAL_ENDOCRINE_AUTO_DRIVE = ABSENT`

`GENERIC_PITUITARY_AS_PROLACTIN = ABSENT`

`AUTOMATIC_AROUSAL_TO_EMISSION = ABSENT`

`AUTOMATIC_AROUSAL_TO_EJACULATION = ABSENT`

`EXPLICIT_REPRODUCTIVE_EVENT_GATES = MATERIALIZED`

`EMISSION_TRANSITION_SEMANTICS = CORRECTED`

`EXPULSION_TRANSITION_SEMANTICS = CORRECTED`

`RECOVERY_PATH = MATERIALIZED`

`PHYSIOLOGY_MOTIVATION_SEPARATION = PASS`

`NEXT_TICK_BODY_FEEDBACK = PASS`

`TEN_SCENARIO_STABILITY_REGRESSION = PASS`

`PHENOMENAL_PROMOTION = NONE`

## 18. Nonclaims

This successor does not establish:

- biological fidelity;
- a full endocrine simulator;
- measured human heart rate;
- measured human respiratory rate;
- measured plasma catecholamine levels;
- measured prolactin;
- an orgasm state;
- pleasure;
- subjective arousal;
- desire;
- consent;
- consciousness;
- subjectivity;
- phenomenal experience;
- physical embodiment.

Persistent boundaries:

`REFERENCE_STATE != MEASUREMENT`

`ASSOCIATION != CAUSATION`

`EJACULATION != ORGASM`

`PHYSIOLOGY != MOTIVATION`

`EVENT_GATE != CONSENT`

`FUNCTIONAL_STATE != FELT_EXPERIENCE`

`IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT`

`CI_PASS != BIOLOGICAL_VALIDATION`

`SUBJECTIVITY = NOT_ESTABLISHED`

`CONSCIOUSNESS = NOT_ESTABLISHED`

`PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`

`ACTION_AUTHORITY = NONE`

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`

## 19. Out of scope

Do not:

- calibrate numerical heart-rate or respiratory values from small historical studies;
- infer sexual desire from genital or autonomic physiology;
- infer orgasm from ejaculation;
- create a prolactin value from the generic pituitary channel;
- create a testosterone surge from sexual activation;
- reuse exercise transitions;
- normalize Teacher against Work, Codex, AION, or Astra;
- merge without a separate exact-head authorization.

## 20. Lifecycle

This successor should be implemented on a dedicated research branch, verified through deterministic tests and exact-head CI, documented in a Draft PR, and closed unmerged unless separately authorized.
