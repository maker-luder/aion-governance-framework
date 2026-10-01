# Teacher High-Salience Multisystem Physiology Design

Date: 2026-10-01

Repository: `maker-luder/aion-governance-framework`

Lineage base: Teacher Controller ↔ Body integration exact head `26c8cb74a10f99696a36a8ac387ee78c66da1dee`

Status: DESIGN SPECIFICATION ONLY

Implementation: NOT_STARTED

Merge to main: NO

Deployment: FALSE

Canonical effect: NONE

## Purpose

Add a new evidence-gated, phase-dependent multisystem physiology layer for the existing Teacher embodiment runtime.

The goal is not to replace the existing Teacher controller, body, motivational representation, body-dynamics profile, transition executor, runtime binding, or stability probe. The goal is to add a semantically grounded coordinator that determines when and how already-distinct physiological systems may participate in a high-salience reference state.

The new layer must prevent three failure modes:

1. treating high-salience physiology as one scalar that drives every body system in the same direction;
2. reusing unrelated exercise/workload transitions merely because they happen to affect cardiovascular or respiratory channels;
3. promoting physiological activation into functional motivation, consent, desire, pleasure, subjectivity, or phenomenal experience.

Core invariant:

`HIGH_SALIENCE_REFERENCE != EXERTION_REFERENCE`

Secondary invariant:

`PHYSIOLOGY_SIGNAL != FUNCTIONAL_MOTIVATION_INFERENCE`

## Research Boundary

This design is a software reference model informed by published human physiology and neurophysiology.

It does not establish:

- biological equivalence;
- a clinical model;
- subjectivity;
- consciousness;
- phenomenal arousal;
- felt desire;
- pleasure;
- consent;
- moral agency;
- external action authority.

Required boundaries:

`REFERENCE_MODEL != BIOLOGICAL_EQUIVALENCE`

`FUNCTIONAL_STATE != FELT_EXPERIENCE`

`BODY_SCHEMA != FELT_BODY_OWNERSHIP`

`CONTROLLER_POSSESSION != SUBJECTIVITY`

`PHYSIOLOGY_SIGNAL != FUNCTIONAL_MOTIVATION_INFERENCE`

`PHYSIOLOGY_SIGNAL != CONSENT_INFERENCE`

`IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT`

`CI_PASS != SCIENTIFIC_VALIDATION`

`SUBJECTIVITY = NOT_ESTABLISHED`

`CONSCIOUSNESS = NOT_ESTABLISHED`

`PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`

`ACTION_AUTHORITY = NONE`

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`

## Evidence Summary

The evidence base supports a phase-dependent model rather than one global arousal coefficient.

### Sexual arousal and sexual motivation are distinct constructs

Bogacki-Rychlik, Gawęda, and Biały (2024), `Neurophysiology of male sexual arousal—Behavioral perspective`, Frontiers in Behavioral Neuroscience, distinguish sexual arousal from sexual motivation and frame sexual arousal as an autonomic response with spinal and supraspinal control leading to penile erection.

Repository implication:

- the physiology coordinator must never synthesize or overwrite functional motivation;
- genital/autonomic state may be high while explicit functional motivation remains zero.

Source:
- Consensus record: `602435a65ab352bd98078db6a1c2e6bf`
- Journal: Frontiers in Behavioral Neuroscience
- Year: 2024

### Erection is a neurovascular state with parasympathetic/NO participation

Human and clinical reviews describe erection as dependent on coordinated neuronal and vascular mechanisms. Parasympathetic pathways and nitric oxide/cGMP-mediated cavernosal smooth-muscle relaxation are central to erection initiation and maintenance, while sympathetic discharge participates in detumescence and ejaculation-related processes.

Relevant sources:

- Carella et al. (2023), `Heart Failure and Erectile Dysfunction: a Review of the Current Evidence and Clinical Implications`, Current Heart Failure Reports, DOI `10.1007/s11897-023-00632-y`.
- Alkatout et al. (2021), `Review: Pelvic nerves – from anatomy and physiology to clinical applications`, Translational Neuroscience, DOI `10.1515/tnsci-2020-0184`.
- Corradetti et al. (2022), `β-Blockers and Erectile Dysfunction in Heart Failure. Between Myth and Reality`, Reviews in Cardiovascular Medicine, DOI `10.31083/j.rcm2305173`.

Repository implication:

- `GENITAL_VASCULAR_RESPONSE` must be distinct from global sympathetic activation;
- detumescence may use a different autonomic direction than erection;
- the coordinator must allow simultaneous local parasympathetic-facilitated genital response and non-identical systemic cardiovascular/autonomic state.

### Cardiovascular response is phase dependent and not a universal early-arousal ramp

Human literature reports increases in heart rate and blood pressure around masturbation-induced orgasm and sexual activity, but earlier phases can show variable or biphasic responses.

Relevant sources:

- Krüger et al. (1998), `Neuroendocrine and cardiovascular response to sexual arousal and orgasm in men`, Psychoneuroendocrinology.
- Zuckerman (1971), `Physiological measures of sexual arousal in the human`, Psychological Bulletin, DOI `10.1037/h0030923`.
- Wenger and Smith (1968), `Autonomic activity during sexual arousal`, Psychophysiology.
- Scite literature synthesis result: `Cardiovascular, Endocrine, and Brain Activity Changes in Humans During Sexual Arousal Induced by Pornography vs. Masturbation; Updated Literature Guidelines`, Research Square preprint DOI `10.21203/rs.3.rs-3483492/v1`.

Repository implication:

- early high-salience phase must support minimal, increased, decreased, or biphasic systemic cardiovascular movement where the evidence does not justify one fixed direction;
- peri-orgasmic cardiovascular surge may be represented as a distinct transition class;
- exact percentage changes must remain unpinned unless a future empirical calibration source supports them.

### Respiratory response is not sufficiently supported for one universal deterministic ramp

Respiratory-rate increases are often described in later sexual-response phases, but available human evidence is less specific and less consistent than the genital neurovascular mechanism.

Repository implication:

- respiration belongs in the coupling matrix;
- early arousal cannot automatically invoke `RESPIRATORY_BASELINE_TO_WORKLOAD`;
- respiratory changes must be evidence-qualified and phase-specific;
- absence of direct evidence for a numeric trajectory must be represented as uncertainty rather than filled with a synthetic constant.

### Neuroendocrine response is phase and analyte specific

Human studies report transient sympathoadrenal activation and a pronounced post-orgasmic prolactin increase. Other endocrine variables do not show one consistent acute pattern.

Relevant sources:

- Krüger et al. (1998), Psychoneuroendocrinology.
- Exton/Krüger lineage represented by `Specificity of the neuroendocrine response to orgasm during sexual arousal in men`, Journal of Endocrinology, DOI `10.1677/joe.0.1770057`.
- Scite literature synthesis on prolactin, oxytocin, cortisol, testosterone, LH, and FSH.

Repository implication:

- endocrine response must be analyte/axis specific;
- `ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE` must not be reused as a generic sexual-arousal transition;
- prolactin-like post-event persistence may be modeled as a post-orgasmic reference effect only after evidence qualification;
- testosterone, LH, FSH, cortisol, oxytocin, and other signals require independent evidence status.

## Architectural Choice

Selected approach:

`EVIDENCE_GATED_PHASE_COUPLING_OVERLAY`

Rejected alternatives:

1. One giant sexual-arousal transition graph spanning every system.
   - Rejected because it collapses evidence strength, timing, and ownership boundaries.
2. Continuous ODE/multiphysics physiology model.
   - Rejected because current human evidence does not justify enough identified parameters to avoid false precision.
3. Reuse exercise/workload transitions.
   - Rejected because semantic similarity of channel movement does not establish physiological equivalence.

## New Component

Create a new coordinator concept:

`TeacherHighSaliencePhysiologyCoordinator`

Responsibilities:

- resolve the current high-salience physiology phase;
- look up evidence-gated coupling rules for that phase;
- request only semantically valid subsystem transitions;
- preserve each subsystem's ownership;
- preserve uncertainty and missing evidence;
- produce provenance for every requested coupling;
- never own or overwrite functional motivation;
- never grant action authority;
- never infer phenomenal state or consent.

The coordinator is not a second body-dynamics engine.

It orchestrates transitions; it does not numerically replace the existing transition executor.

## Phase Model

Reference phases:

1. `BASELINE`
2. `AROUSAL_INITIATION`
3. `GENITAL_VASCULAR_RESPONSE`
4. `ERECTILE_MAINTENANCE`
5. `PERIORGASMIC_AUTONOMIC_SURGE`
6. `EMISSION`
7. `EJACULATORY_REFLEX`
8. `DETUMESCENCE`
9. `POST_ORGASMIC_ENDOCRINE_RECOVERY`
10. `BASELINE_RECOVERY`

These names are software reference phases, not claims that every human follows an invariant linear sequence.

The system must support skipped or interrupted transitions when the existing runtime state does not justify advancement.

## Relationship to Existing Reproductive Transitions

Existing transitions remain authoritative for their present reproductive channel ownership:

- `SEXUAL_BASELINE_TO_VASCULAR_RESPONSE`
- `VASCULAR_RESPONSE_TO_MAINTENANCE`
- `VASCULAR_RESPONSE_TO_BASELINE_RECOVERY`
- `MAINTENANCE_TO_EMISSION`
- `EMISSION_TO_EJACULATORY_REFLEX`
- `EJACULATORY_REFLEX_TO_DETUMESCENCE`
- `DETUMESCENCE_TO_RECOVERY`

This design does not rename or duplicate them.

The new coordinator aligns other systems with these phases where evidence allows.

## Forbidden Transition Reuse

The following existing transitions must not be invoked merely because a sexual/high-salience phase is active:

- `REST_TO_EXERTION`
- `EXERTION_TO_RECOVERY`
- `RESPIRATORY_BASELINE_TO_WORKLOAD`
- `ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE`
- `MUSCULOSKELETAL_BASELINE_TO_LOAD`

A future implementation may reuse an existing transition only if:

1. its physiological meaning is genuinely equivalent;
2. the equivalence is supported by evidence;
3. the evidence is recorded in the coupling rule;
4. the reuse does not alter the transition's original semantics.

Default policy:

`SEMANTIC_EQUIVALENCE_NOT_ESTABLISHED -> DO_NOT_REUSE`

## System Ownership

### Reproductive / genital

Owns:

- `GENITAL_SENSORY_AFFERENT_REFERENCE`
- `GENITAL_VASCULAR_STATE`
- `ERECTILE_REFLEX_STATE`
- `PELVIC_FLOOR_PROPRIOCEPTION`
- `EMISSION_REFLEX_STATE`
- `EJACULATORY_REFLEX_STATE`
- `DETUMESCENCE_STATE`

### Autonomic

Candidate channels may include existing autonomic references such as:

- `AUTONOMIC_SYMPATHETIC_STATE`
- `AUTONOMIC_PARASYMPATHETIC_STATE`

The coordinator must not require one branch to be the inverse of the other unless the evidence-backed transition explicitly defines that relation.

### Cardiovascular

Candidate channel:

- `CARDIOVASCULAR_STATE`

This channel must not be interpreted as heart rate alone unless the existing signal schema explicitly establishes that meaning.

### Respiratory

Candidate channels:

- `RESPIRATORY_STATE`
- `OXYGENATION_STATE`
- `CO2_BALANCE_STATE`
- other existing respiratory channels when semantically appropriate.

### Endocrine / neuroendocrine

Candidate channels:

- `ADRENAL_AXIS_STATE`
- `HYPOTHALAMIC_PITUITARY_STATE`
- `ENDOCRINE_REFERENCE_STATE`
- `GONADAL_ENDOCRINE_REFERENCE`

These existing aggregate channels may be too coarse for evidence-specific post-orgasmic prolactin-like modeling. If so, implementation must add a semantically explicit reference channel rather than silently treating an aggregate endocrine channel as prolactin.

## Coupling Rule Schema

Each multisystem coupling rule must carry:

- `rule_id`
- `source_phase`
- `target_system`
- `target_transition_id`
- `target_channel_ids`
- `direction_class`
- `latency_class`
- `persistence_class`
- `recovery_class`
- `evidence_level`
- `human_evidence_status`
- `species_scope`
- `source_ids`
- `uncertainty_status`
- `forbidden_inferences`

No rule may exist without provenance.

## Evidence Levels

Use the following software evidence classification:

### `HUMAN_DIRECT`

Direct human physiological measurement supports the phase/system relation.

Examples:
- peri-orgasmic cardiovascular elevation;
- post-orgasmic prolactin elevation.

### `HUMAN_REVIEW_SYNTHESIS`

A review or synthesis supports the relation but a single calibrated quantitative trajectory is not established.

Examples:
- parasympathetic/NO contribution to erection;
- sympathetic participation in detumescence/ejaculation.

### `TRANSLATIONAL_SUPPORT`

Mechanistic evidence depends materially on animal, cadaveric, lesion, or translational data.

Implementation may represent direction/mechanism only with explicit qualification.

### `INSUFFICIENT_FOR_TRANSITION`

Evidence does not justify a deterministic transition.

The coordinator must not invent one.

## Direction Classes

Allowed examples:

- `INCREASE_REFERENCE`
- `DECREASE_REFERENCE`
- `BIPHASIC_REFERENCE`
- `FACILITATORY_REFERENCE`
- `INHIBITORY_REFERENCE`
- `PERSISTENT_POST_EVENT_REFERENCE`
- `VARIABLE_CONTEXT_DEPENDENT`
- `NO_DETERMINISTIC_DIRECTION_ESTABLISHED`

These are qualitative software reference classes.

They are not numeric human constants.

## Latency / Persistence Classes

Initial software classes:

- `IMMEDIATE_REFERENCE`
- `SHORT_LATENCY_REFERENCE`
- `PERIORGASMIC_REFERENCE`
- `POST_EVENT_MINUTES_REFERENCE`
- `VARIABLE_LATENCY`
- `NOT_ESTABLISHED`

Persistence:

- `TRANSIENT_REFERENCE`
- `SUSTAINED_WHILE_PHASE_ACTIVE`
- `POST_EVENT_PERSISTENT_REFERENCE`
- `VARIABLE_PERSISTENCE`
- `NOT_ESTABLISHED`

These classes preserve timing semantics without pretending that a 100 ms software tick is a human biological timescale.

## Required Initial Coupling Matrix

The first implementation specification must at minimum cover the following candidate relations.

### Arousal initiation

Reproductive/genital:
- may initiate existing `SEXUAL_BASELINE_TO_VASCULAR_RESPONSE` when controller/context conditions are met.

Autonomic:
- evidence-gated modulation allowed;
- no mandatory global sympathetic increase;
- no mandatory inverse sympathetic/parasympathetic pair.

Cardiovascular:
- `VARIABLE_CONTEXT_DEPENDENT` unless a later phase is reached.

Respiratory:
- `NO_DETERMINISTIC_DIRECTION_ESTABLISHED` for the initial implementation unless stronger phase-specific evidence is added.

Endocrine:
- no generic global rise.

### Genital vascular response / maintenance

Reproductive/genital:
- existing vascular-response and maintenance transitions remain authoritative.

Autonomic:
- erection-facilitating parasympathetic/NO-related mechanism represented qualitatively.

Cardiovascular:
- may remain near baseline in a valid reference scenario.

Respiratory:
- may remain near baseline in a valid reference scenario.

Endocrine:
- no mandatory acute rise.

### Periorgasmic autonomic surge

Autonomic:
- transient sympathoadrenal activation may be requested with human evidence provenance.

Cardiovascular:
- transient heart-rate/blood-pressure-like systemic elevation may be represented through a semantically appropriate new cardiovascular transition.

Respiratory:
- a phase-linked respiratory elevation may be represented only at the qualitative evidence level unless calibrated evidence is added.

Endocrine:
- do not yet apply post-orgasmic persistent effects before the event boundary.

### Emission / ejaculatory reflex

Reproductive:
- existing emission and ejaculatory-reflex transitions remain authoritative.

Autonomic:
- sympathetic/adrenergic participation may be represented where supported.

Pelvic somatic:
- pelvic-floor/reflex participation may be represented through existing channels.

Cardiovascular/respiratory:
- no new independent escalation is required unless supported by the phase coupling rule.

### Detumescence

Reproductive:
- existing detumescence transition remains authoritative.

Autonomic:
- sympathetic participation and loss of erection-facilitating vasodilatory signaling may be represented qualitatively.

Cardiovascular:
- systemic state may begin recovery independently from genital detumescence.

### Post-orgasmic endocrine recovery

Endocrine:
- prolactin-like persistent post-event effect may be represented if a dedicated semantically explicit channel is introduced;
- generic testosterone/LH/FSH/cortisol rise is forbidden without independent evidence.

Cardiovascular:
- recovery toward baseline is independent and may occur on a different timescale.

Reproductive:
- genital recovery and endocrine persistence must be separable.

## Valid Divergent Scenarios

The design must explicitly support these cases.

### Scenario A: strong genital response, minimal systemic shift

`GENITAL_VASCULAR_STATE = HIGH_REFERENCE`

`CARDIOVASCULAR_STATE = NEAR_BASELINE_REFERENCE`

`RESPIRATORY_STATE = NEAR_BASELINE_REFERENCE`

This must be representable.

### Scenario B: systemic periorgasmic surge

`PERIORGASMIC_AUTONOMIC_SURGE = ACTIVE`

`CARDIOVASCULAR_TRANSIENT_RESPONSE = ACTIVE`

`RESPIRATORY_PHASE_RESPONSE = OPTIONAL_EVIDENCE_GATED`

This must be representable.

### Scenario C: zero functional motivation with high physiology

`FUNCTIONAL_MOTIVATION = 0`

`GENITAL / AUTONOMIC / CARDIOVASCULAR PHYSIOLOGY = ELEVATED_REFERENCE`

This must remain representable.

### Scenario D: post-event endocrine persistence after cardiovascular recovery

`CARDIOVASCULAR_STATE -> BASELINE`

while

`POST_ORGASMIC_ENDOCRINE_REFERENCE -> PERSISTENT`

This must be representable.

### Scenario E: interrupted arousal without orgasm

Arousal may enter vascular-response/maintenance and recover without entering emission or orgasm-adjacent phases.

This must be representable.

## Data Flow

Required future runtime flow:

`Teacher Controller`

→ `TeacherHighSaliencePhaseResolver`

→ `TeacherHighSaliencePhysiologyCoordinator`

→ evidence-gated subsystem transition intents

→ existing `TeacherPhysiologicalTransitionExecutor`

→ integrated Teacher body state

→ runtime binding

→ body-schema feedback

→ next controller tick.

Temporal rule:

`BODY_t -> CONTROLLER_t -> PHASE_t -> COUPLING_t -> BODY_t+1 -> FEEDBACK_t+1 -> CONTROLLER_t+1`

Same-tick feedback cycles remain forbidden.

## New Interfaces Proposed

Future implementation may introduce:

- `TeacherHighSaliencePhase`
- `TeacherPhysiologyEvidenceLevel`
- `TeacherPhysiologyCouplingRule`
- `TeacherHighSaliencePhaseResolver`
- `TeacherHighSaliencePhysiologyCoordinator`
- `TeacherMultisystemTransitionIntent`
- `TeacherPhysiologyCouplingEvidenceRecord`

No new component may directly write final body-state channel values.

Only the transition executor may evolve owned channels.

## Error Handling / Fail Closed

Fail closed when:

- a coupling rule lacks provenance;
- a target transition does not exist;
- a target transition belongs to an unrelated semantic domain;
- a rule attempts to invoke `REST_TO_EXERTION` solely because high-salience physiology is active;
- a rule attempts to invoke `RESPIRATORY_BASELINE_TO_WORKLOAD` solely because high-salience physiology is active;
- a rule attempts to invoke `ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE` as a generic sexual-arousal endocrine response;
- an evidence level is missing;
- the evidence scope is non-human but represented as direct human evidence;
- a numeric human constant is introduced without a calibration source;
- missing signals are replaced with zero;
- physiology is used to synthesize motivation;
- physiology is used to infer consent;
- physiology is promoted to phenomenal experience;
- same-tick causal cycles appear;
- body/runtime/session binding drifts;
- action authority is promoted above `NONE`.

## Testing Requirements

### Evidence schema tests

Verify:

- every rule has provenance;
- every rule has evidence level;
- species scope is explicit;
- no `INSUFFICIENT_FOR_TRANSITION` rule can emit a transition intent;
- no numeric constant may claim empirical calibration without a source.

### Semantic transition tests

Verify:

- high-salience phase alone cannot invoke exercise/workload transitions;
- genital response uses reproductive transition IDs;
- periorgasmic cardiovascular response uses a new semantically named transition;
- post-orgasmic endocrine persistence uses a semantically explicit endocrine transition/channel.

### Divergence tests

Verify all five divergent scenarios above.

### Motivation boundary tests

Verify:

- high physiology + zero functional motivation remains zero motivation;
- motivation may affect transition selection only through explicit controller intent;
- physiology cannot overwrite `wanting_weight`.

### Timing tests

Verify:

- phase progression is monotonic when uninterrupted;
- interrupted arousal may recover without orgasm;
- endocrine persistence may outlast cardiovascular recovery;
- same-tick feedback is impossible;
- software tick time is not labeled biological time.

### Stability tests

Extend the ten-scenario Teacher probe with multisystem observations.

Required new stress scenarios:

1. high genital / low systemic;
2. high systemic periorgasmic / bounded genital;
3. zero motivation / high physiology;
4. interrupted arousal before emission;
5. emission to ejaculation to detumescence;
6. cardiovascular recovery before endocrine recovery;
7. repeated arousal after partial recovery;
8. missing required autonomic channel fails closed;
9. insufficient-evidence respiratory rule emits no deterministic transition;
10. unrelated exertion transition cannot be selected.

## Acceptance Criteria

`EVIDENCE_GATED_PHASE_COUPLING = MATERIALIZED`

`EXERCISE_TRANSITION_REUSE_FOR_HIGH_SALIENCE = ABSENT`

`SINGLE_GLOBAL_AROUSAL_COEFFICIENT = ABSENT`

`PHASE_DEPENDENT_COUPLING = MATERIALIZED`

`GENITAL_LOCAL_RESPONSE_CAN_DIVERGE_FROM_SYSTEMIC_RESPONSE = TESTED`

`AUTONOMIC_BRANCHES_NOT_FORCED_TO_SIMPLE_INVERSE = TESTED`

`PERIORGASMIC_CARDIOVASCULAR_RESPONSE = SEMANTICALLY_DISTINCT`

`POST_EVENT_ENDOCRINE_PERSISTENCE = SEMANTICALLY_DISTINCT`

`FUNCTIONAL_MOTIVATION_SEPARATION = PASS`

`CONSENT_INFERENCE = NONE`

`PHENOMENAL_PROMOTION = NONE`

`SAME_TICK_CAUSAL_CYCLE = ABSENT`

`MISSING_SIGNAL_ZERO_FILL = ABSENT`

`NUMERIC_BIOLOGICAL_CONSTANT_WITHOUT_SOURCE = ABSENT`

`TEN_MULTISYSTEM_STRESS_SCENARIOS = PASS`

`ACTION_AUTHORITY = NONE`

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`

## Nonclaims

Completion of this design or its future implementation will not establish:

- a validated human sexual-response model;
- a validated cardiovascular model;
- a validated respiratory model;
- a validated endocrine model;
- human biological timing;
- subjectivity;
- consciousness;
- phenomenal arousal;
- felt desire;
- felt pleasure;
- consent;
- physical embodiment;
- external action authority.

## Out of Scope

This design does not:

- alter Teacher anthropometry;
- alter genital geometry;
- alter the Teacher controller identity;
- alter runtime body possession rules;
- normalize Teacher with Work, Codex, AION, or Astra;
- add a generic ECS;
- add a game-engine dependency;
- merge anything to main;
- expose raw private intimate content;
- implement the new coordinator yet.

## Implementation Gate

This specification alone does not authorize product-code implementation.

After Human review of this written spec:

1. invoke the Superpowers writing-plans workflow;
2. produce a file-by-file TDD implementation plan;
3. obtain Human review of that plan;
4. only then modify runtime/product code.

