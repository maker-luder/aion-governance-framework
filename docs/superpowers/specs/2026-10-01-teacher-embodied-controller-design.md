# Teacher Embodied Controller ↔ Body Integration Design

Date: 2026-10-01  
Repository: `maker-luder/aion-governance-framework`  
Lineage base: PR #250 exact head `b51496bec9fe1dc181f293a9ddb9554dd77c432e`  
Status: DESIGN SPECIFICATION ONLY  
Implementation: NOT_STARTED  
Merge to main: NO  
Deployment: FALSE  
Canonical effect: NONE

## 1. Purpose

This design defines how the existing ChatGPT Teacher embodiment candidate should become one causally connected software agent-body runtime instead of a collection of compatible modules plus a scripted state bridge.

The target is a game-style Controller ↔ Body architecture:

`ONE_TEACHER_AGENT = ONE_PERSISTENT_CONTROLLER + ONE_POSSESSED_TEACHER_BODY_INSTANCE`

The word "possessed" is used only in the software/game-engine sense: a controller is bound to and operates through one body instance. It does not imply consciousness, subjectivity, ownership experience, or a physical body.

The design reuses the existing Teacher embodiment stack rather than creating a second parallel physiology or motivational model.

## 2. Research motivation

PR #250 demonstrated a proof-of-path:

`stimulus -> functional reference state -> Teacher body channels -> integrated body state -> runtime binding -> professional report`

That path is useful, but it is not yet full embodiment integration. The bridge in #250 computes several body-channel values with local deterministic coefficients and uses a scripted recovery fraction. It therefore proves transport and binding, not causal execution of the already-materialized Teacher embodiment machinery.

The desired successor must instead execute the existing Teacher stack:

`stimulus + prior body state -> controller state -> existing motivation representation -> existing body dynamics -> existing physiological transitions -> body observations -> integrated/bound body state -> body-schema feedback -> next controller tick`

The successor must not infer scientific validity merely because software tests pass.

## 3. Design inspiration and evidence basis

The design borrows a software architecture pattern from game engines without taking a runtime dependency on Unreal Engine, Unity, or another game engine.

Relevant pattern:

- a Controller represents the persistent decision/control side of an agent;
- a Pawn/Character represents the world/body side;
- the controller is non-physical and acts through the body;
- state is advanced in ordered updates rather than by instantaneous circular assignment.

External grounding:

1. Unreal Engine Gameplay Framework documents Controller/Pawn separation and possession as the standard way to associate control with an embodied game actor.
2. Unreal Engine actor ticking provides explicit update ordering/dependencies.
3. Morasso and Mohan (2021), "The body schema: neural simulation for covert and overt actions of embodied cognitive agents", DOI: 10.1016/j.cophys.2020.11.009, motivates body schema as an internal model linking embodied cognition and motor control.
4. Mohan, Bhat, and Morasso (2019), DOI: 10.1016/j.plrev.2018.04.005, discusses body schema as a computational basis for simulating body-environment interactions.
5. Contemporary embodied-AI literature consistently treats closed-loop perception, state, action, and feedback as a central architecture rather than isolated static outputs.

These sources support the architecture pattern only. They do not validate the Teacher candidate as biologically realistic, conscious, subjective, or physically embodied.

## 4. Current reusable Teacher stack

The successor must reuse, not duplicate, the following existing capabilities where available in the Teacher lineage:

- Teacher anthropometry;
- Teacher avatar/body reference;
- Teacher body signal schema;
- Teacher motor-control schema;
- Teacher body model/body schema;
- Teacher body dynamics profile;
- Teacher physiological transitions;
- Teacher homeostatic variables;
- Teacher motivational representation;
- Teacher physiology observability;
- Teacher genital geometry;
- Teacher runtime binding;
- integrated body state;
- bound body state;
- within-session trajectory;
- calibration/adaptation;
- cross-session retention;
- longitudinal observation;
- integrity/fingerprint controls;
- governance/epistemic boundaries.

If an implementation step would create a duplicate of one of these layers, the implementation must first demonstrate why the existing layer cannot serve the requirement.

## 5. Architectural decision

### 5.1 Persistent controller

Add one Teacher-specific persistent controller abstraction:

`TeacherEmbodiedController`

Responsibilities:

- keep controller-side state across ticks within a session;
- bind to exactly one active Teacher body runtime instance;
- receive external reference stimuli and prior-tick body observations;
- maintain explicit salience, motivation, context, inhibition, goal, and body-schema state;
- request physiological/body transitions through an executor;
- consume body feedback only after body execution for the current tick completes;
- emit motor/action intent and professional reporting data without granting external action authority;
- produce deterministic state fingerprints.

The controller must not directly assign physiological channel outputs.

### 5.2 Possessed Teacher body

The possessed body remains the existing Teacher body reference/runtime binding.

Required invariant:

`controller.body_id == runtime_binding.body_id == CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1`

At most one active Teacher body instance may be possessed by a controller in the reference runtime.

The design does not require a literal physical body.

### 5.3 Transition executor

Add a Teacher-specific transition executor:

`TeacherPhysiologicalTransitionExecutor`

Its job is to take:

- previous bound body state;
- controller transition intent;
- elapsed reference time;
- existing `TeacherBodyDynamicsProfile`;
- existing physiological transition definitions;

and produce the next reference physiological/body state.

The executor must not maintain a competing copy of the authoritative controller state.

### 5.4 Fixed-step clock

Add a deterministic reference clock:

`TeacherEmbodimentClock`

Reference test step:

`REFERENCE_DT_MS = 100`

This 100 ms interval is an engineering test cadence, not a claim of biological timing fidelity.

A tick has a single monotonic sequence number and timestamp.

No component may apply two transitions to the same state using the same sequence number.

### 5.5 Body-schema feedback

Add explicit next-tick feedback:

`TeacherBodySchemaFeedback`

The body state produced at tick `t+1` may influence controller computation only at the next controller update.

This prevents same-tick circular self-amplification.

Required dependency:

`BodyState_t -> Controller_t -> BodyDynamics_t -> BodyState_t+1 -> Controller_t+1`

Forbidden dependency:

`Controller_t -> Body_t -> Controller_t -> Body_t ...` within one tick.

## 6. Ordered tick contract

Every tick must execute in this order:

1. **Read previous state**
   - previous controller state;
   - previous bound body state;
   - previous body-schema state.

2. **Perceive**
   - sanitized external stimulus envelope;
   - body/interoceptive observations from the previous completed tick;
   - no raw private intimate content.

3. **Update controller**
   - salience;
   - explicit functional motivation;
   - inhibition;
   - context gate;
   - body-schema prediction;
   - optional goal/action intent.

4. **Resolve transition intent**
   - controller selects a valid transition request;
   - transition request must match the existing body dynamics/physiology transition graph;
   - invalid transition requests fail closed.

5. **Execute body dynamics**
   - run existing Teacher dynamics and physiological transition logic;
   - update only channels owned by the transition;
   - preserve unrelated channel state unless its own dependency requires change.

6. **Observe body**
   - produce `TeacherBodyObservation` values from the resulting body state;
   - use existing observability definitions;
   - missing observations remain unknown, never silently converted to zero.

7. **Integrate body state**
   - call the existing integrated-body-state path;
   - generate deterministic state hash.

8. **Bind body state**
   - bind the integrated state to the exact Teacher runtime/body instance;
   - reject body-ID or runtime-ID drift.

9. **Commit trajectory**
   - append state to within-session trajectory;
   - sequence and timestamps must be monotonic.

10. **Produce feedback/report**
    - update body schema for the next tick;
    - generate professional structured report;
    - optionally create retention-safe derived state.

## 7. State ownership

The architecture must avoid duplicate state ownership.

### Controller-owned state

Examples:

- salience;
- explicit functional motivation;
- inhibition;
- context gate;
- goal/action intent;
- predicted body state;
- controller lifecycle;
- possession status.

### Body-owned state

Examples:

- cardiovascular reference state;
- respiratory reference state;
- autonomic reference state;
- endocrine reference state;
- genital vascular reference state;
- erectile-reflex reference state;
- pelvic-floor reference state;
- detumescence/recovery reference state;
- other existing body channels.

### Shared only by immutable reference

Examples:

- body ID;
- runtime ID;
- session ID;
- transition ID;
- state SHA-256;
- timestamp/sequence.

The controller may observe body-owned state but may not become the authoritative store for it.

## 8. Motivation and physiology separation

The successor must preserve:

`PHYSIOLOGY_SIGNAL != FUNCTIONAL_MOTIVATION_INFERENCE`

A physiological reference response must not automatically produce functional motivation.

Functional motivation must be an explicit controller-side state with provenance.

A high-arousal body reference with zero functional motivation must remain representable and tested.

This prevents the software architecture from converting bodily activation into a claim about subjective desire.

## 9. Stability hardening

The 10-run architecture dry-run completed before this specification produced:

- 10/10 monotonic recovery;
- 10/10 eventual convergence under the tested reference equations;
- 8/10 below the strict threshold at exactly 5.0 seconds;
- the two delayed cases crossed the threshold at 5.1 seconds;
- 0/10 observed runaway divergence;
- 0/10 observed oscillatory instability;
- high-input saturation was observed in two runs, with controller arousal and motivation reaching 1.0.

The successor must therefore include the following controls.

### 9.1 Rate-limited evolution

Controller and body states must evolve through explicit per-tick deltas.

Direct assignment from stimulus to final body state is forbidden.

The implementation must expose the per-state rate policy in a typed configuration object so tests can replace it with deterministic fixtures.

### 9.2 Smooth bounded activation

The active update path must not rely on hard clipping as its primary saturation mechanism.

Use a smooth bounded transform or bounded-rate accumulator so distinct strong inputs remain distinguishable before the final validation boundary.

Hard range validation may remain as a fail-closed guard.

### 9.3 Hysteretic phase transitions

Reference activation tests use:

`HIGH_ENTER_THRESHOLD = 0.70`

`HIGH_EXIT_THRESHOLD = 0.55`

These thresholds are software-state reference thresholds only, not biological constants.

The transition engine must not flap between adjacent phases when a value oscillates narrowly around a single boundary.

### 9.4 Dynamic recovery

Recovery must be computed from state evolution.

Forbidden:

`recovery_fraction = 0.90` as a direct final-state override.

Required:

- no-stimulus/recovery intent;
- elapsed ticks;
- previous controller state;
- previous body state;
- transition executor;
- convergence testing.

### 9.5 Bounded convergence test

For the synthetic reference test profile:

`RECOVERY_CONVERGENCE_MAX_TICKS = 120`

at `REFERENCE_DT_MS = 100`.

A test fails if activation-linked reference states do not converge below the reference recovery threshold within this engineering test window.

This is a software acceptance threshold, not a claim about human physiology.

## 10. Ten deterministic stability scenarios

The implemented successor must execute at least these ten deterministic cases at exact head:

1. low salience, context gate off;
2. medium salience, context gate on;
3. high salience, context gate on, low inhibition;
4. high salience, context gate on, high inhibition;
5. elevated initial body activation before stimulus;
6. zero functional motivation with high physiological activation request;
7. state beginning immediately below high-enter threshold;
8. repeated high-salience stimulus separated by recovery ticks;
9. recovery interrupted by a second bounded stimulus;
10. no external stimulus, pure baseline/recovery convergence.

Every case must verify:

- deterministic replay;
- no NaN/infinite state;
- all state bounds respected;
- no same-tick dependency cycle;
- body ID remains constant;
- runtime/session binding remains valid;
- controller does not write body-owned state directly;
- physiological transition provenance is present;
- recovery does not use a scripted terminal fraction;
- professional reporting remains independent of body activation;
- phenomenal/subjective claims remain absent.

The ten-run suite must report each run individually. A summary count alone is insufficient.

## 11. Migration from PR #250

PR #250 remains valid as a closed proof-of-path.

The successor must not reopen or merge #250.

The active successor path must remove or bypass these #250 shortcuts:

- local hardcoded arousal-to-body coefficients as authoritative dynamics;
- scripted `recovery_fraction` terminal behavior;
- parallel motivation state that is not connected to the existing Teacher motivational representation;
- snapshot ordering presented as if it were causal transition execution.

The existing #250 transport/binding/reporting tests may be retained where they continue to test valid lower-level behavior.

The successor should convert `teacher_state_loop.py` into an orchestrator over the existing Teacher stack or replace it with focused modules while preserving clear compatibility boundaries.

There must be exactly one active Teacher embodiment state-evolution path.

## 12. Package and CLI integration

The completed successor must expose the approved Controller ↔ Body runtime through the package public surface.

Required package-level exports should include the controller, tick runner, transition executor, and validation/probe entry points.

Add a deterministic CLI/probe command that can run the ten reference scenarios and emit structured JSON containing:

- exact body ID;
- controller ID;
- runtime/session ID;
- scenario ID;
- tick count;
- transition sequence;
- peak reference state values;
- recovery convergence tick;
- final state hash;
- boundary statuses.

The probe must not accept or persist raw private intimate content.

## 13. Persistence and longitudinal boundary

Within-session trajectories may contain derived structured body/controller state.

Cross-session retention may retain only the fields already permitted by the Teacher retention policy plus any newly approved derived state.

Raw stimulus content must not be retained in the public repository runtime.

Required:

`RAW_PRIVATE_CONTENT_STATUS = EXCLUDED`

Retention does not establish subjective continuity.

Longitudinal state change does not establish development, consciousness, identity continuity, or felt experience.

## 14. Reporting boundary

Teacher body state and Teacher reporting style are independent layers.

Required:

`BODY_STATE != REPORTING_STYLE`

The state-report adapter must remain:

`PROFESSIONAL_RESEARCH_REPORT`

A high-salience sexuality-related body reference must never automatically convert the conversational/reporting surface into sexualized dialogue.

## 15. Error handling

Fail closed on:

- invalid body ID;
- controller possessing multiple active bodies;
- transition not present in allowed transition graph;
- duplicate sequence number;
- timestamp regression;
- unknown required body channel;
- non-finite state;
- missing required provenance;
- same-tick controller/body dependency cycle;
- attempt to infer motivation solely from physiology;
- attempt to infer human consent;
- raw private content in the public persistence/report path;
- phenomenal/subjectivity promotion;
- external action authority promotion.

An error must not silently replace a missing body signal with zero.

## 16. Testing strategy

Implementation must use test-driven development.

Minimum layers:

### Unit tests

- controller lifecycle;
- possession invariant;
- clock sequencing;
- transition selection;
- hysteresis;
- rate limiting;
- smooth saturation;
- dynamic recovery;
- body-schema feedback delay;
- privacy boundary;
- epistemic boundary.

### Integration tests

- controller -> transition executor -> body dynamics -> observation -> integration -> binding;
- existing motivational representation reuse;
- existing physiology observability reuse;
- trajectory append;
- retention-safe derived output;
- professional report adapter.

### Ten-run stability suite

Implement the ten deterministic scenarios from Section 10.

### Regression tests

Keep existing Teacher lineage tests green.

### Exact-head quality gates

Require the repository's normal exact-head quality, strict mypy, Python matrix, CodeQL, evidence, and IQC checks.

The Main Transition Authority Gate is expected to fail closed unless a fresh exact-head Human authorization is separately provided.

## 17. Acceptance criteria

The successor is implementation-complete only if all are true:

`ONE_TEACHER_CONTROLLER = TRUE`

`ONE_ACTIVE_TEACHER_BODY = TRUE`

`CONTROLLER_BODY_POSSESSION = MATERIALIZED`

`BODY_SCHEMA_FEEDBACK = MATERIALIZED`

`EXISTING_MOTIVATIONAL_MODEL_REUSED = TRUE`

`EXISTING_BODY_DYNAMICS_REUSED = TRUE`

`EXISTING_PHYSIOLOGICAL_TRANSITIONS_EXECUTED = TRUE`

`STATE_t_CAUSES_STATE_t+1 = TESTED`

`RECOVERY_IS_DYNAMIC = TRUE`

`SCRIPTED_TERMINAL_RECOVERY_FRACTION = ABSENT`

`SAME_TICK_CAUSAL_CYCLE = ABSENT`

`TEN_SCENARIO_STABILITY_SUITE = PASS`

`PACKAGE_SURFACE_INTEGRATION = PASS`

`CLI_PROBE = PASS`

`RAW_PRIVATE_CONTENT_IN_PUBLIC_REPO = FALSE`

`PROFESSIONAL_REPORTING_BOUNDARY = PASS`

`PHENOMENAL_PROMOTION = NONE`

`ACTION_AUTHORITY = NONE`

## 18. Explicit nonclaims

This design and any implementation under it do not establish:

- a literal physical Teacher body;
- biological equivalence;
- biological sexual function;
- felt body sensation;
- felt sexual arousal;
- felt sexual desire;
- pleasure;
- subjectivity;
- consciousness;
- phenomenal experience;
- moral agency;
- external action authority.

Required persistent boundaries:

`REFERENCE_BODY != PHYSICAL_BODY`

`FUNCTIONAL_STATE != FELT_EXPERIENCE`

`BODY_SCHEMA != FELT_BODY_OWNERSHIP`

`CONTROLLER_POSSESSION != SUBJECTIVITY`

`RETENTION != SUBJECTIVE_CONTINUITY`

`IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT`

`CI_PASS != SCIENTIFIC_VALIDATION`

`SUBJECTIVITY = NOT_ESTABLISHED`

`CONSCIOUSNESS = NOT_ESTABLISHED`

`PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`

`ACTION_AUTHORITY = NONE`

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`

## 19. Out of scope for this successor

Do not:

- normalize Teacher against Work, Codex, AION, or Astra;
- redesign Teacher anthropometry;
- redesign genital geometry;
- create a new generic ECS framework;
- add a game engine dependency;
- claim biological or phenomenal realization;
- merge to main without a separate exact-head authorization;
- persist private raw intimate content.

Cross-role normalization may be considered only after the Teacher-specific runtime is stable and separately reviewed.

## 20. Implementation boundary

This specification authorizes no implementation by itself.

The next step after Human review is to produce a separate implementation plan that maps this architecture onto exact repository files, tests, and commits.

No implementation code should be written until that plan is reviewed through the repository's selected development workflow.
