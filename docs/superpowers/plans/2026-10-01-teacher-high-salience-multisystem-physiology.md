# Teacher High-Salience Multisystem Physiology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an evidence-gated, phase-dependent multisystem physiology coordinator to the existing Teacher embodied runtime without reusing exercise/workload transitions or collapsing genital, autonomic, cardiovascular, respiratory, and endocrine physiology into one scalar response.

**Architecture:** Keep the existing Teacher Controller ↔ Body runtime, motivational representation, body-dynamics profile, transition executor, binding, and stability probe. Add one focused high-salience physiology module that owns evidence records, phase resolution, coupling rules, and multisystem transition intents; add only semantically explicit body channels/transitions to the existing schemas; extend the executor to apply per-channel qualitative directions; integrate the coordinator into the existing tick path and add a separate ten-scenario multisystem probe.

**Tech Stack:** Python 3.11+, frozen dataclasses, existing `aion_astra_twin_embodiment` package, pytest, SHA-256 content addressing, repository Ruff/mypy/Quality/CodeQL/evidence controls.

**Spec:** `docs/superpowers/specs/2026-10-01-teacher-high-salience-multisystem-physiology-design.md`

## Global Constraints

- `HIGH_SALIENCE_REFERENCE != EXERTION_REFERENCE`.
- `PHYSIOLOGY_SIGNAL != FUNCTIONAL_MOTIVATION_INFERENCE`.
- `PHYSIOLOGY_SIGNAL != CONSENT_INFERENCE`.
- `REFERENCE_MODEL != BIOLOGICAL_EQUIVALENCE`.
- `FUNCTIONAL_STATE != FELT_EXPERIENCE`.
- `BODY_SCHEMA != FELT_BODY_OWNERSHIP`.
- `CONTROLLER_POSSESSION != SUBJECTIVITY`.
- `IMPLEMENTATION != SCIENTIFIC_ESTABLISHMENT`.
- `CI_PASS != SCIENTIFIC_VALIDATION`.
- `SUBJECTIVITY = NOT_ESTABLISHED`.
- `CONSCIOUSNESS = NOT_ESTABLISHED`.
- `PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`.
- `ACTION_AUTHORITY = NONE`.
- `MERGE_TO_MAIN = NO`.
- `DEPLOYMENT = FALSE`.
- `CANONICAL_EFFECT = NONE`.
- Do not invoke `REST_TO_EXERTION`, `EXERTION_TO_RECOVERY`, `RESPIRATORY_BASELINE_TO_WORKLOAD`, `ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE`, or `MUSCULOSKELETAL_BASELINE_TO_LOAD` merely because a high-salience/sexual phase is active.
- Do not introduce a single global arousal coefficient.
- Missing signals remain unknown; never substitute zero.
- Numeric values used to drive software reference trajectories must be labeled software-reference values and must not be represented as calibrated human biological constants.
- Respiratory arousal remains non-deterministic in the initial coupling matrix unless a separately sourced rule justifies a transition.
- Do not infer orgasm from ejaculation. Post-orgasmic endocrine persistence requires an explicit `ORGASM_REFERENCE_EVENT` marker in the reference runtime.
- Preserve the existing explicit separation between body physiology and `functional_motivation`.
- TDD is mandatory. If the execution harness cannot run local pytest, an unmerged Draft PR may be opened early solely as an exact-head CI carrier; document that deviation and never treat it as merge authorization.

## File Structure

Create:

- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_high_salience_physiology.py`
  - evidence records, evidence levels, coupling rules, phase state/resolver, transition channel directives, multisystem intent, coordinator.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_high_salience_probe.py`
  - ten multisystem stress scenarios and deterministic probe runner.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_high_salience_physiology.py`
  - evidence schema, phase resolver, forbidden transition, coordinator, motivation/consent/phenomenology boundary tests.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_high_salience_probe.py`
  - ten multisystem scenarios, divergence, recovery timing, deterministic replay, CLI/public surface tests.

Modify:

- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_body_channels.py`
  - add a semantically explicit prolactin reference channel; do not repurpose aggregate endocrine channels.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_body_channels.py`
  - require the explicit channel and preserve signal-only/nonphenomenal boundaries.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_body_dynamics.py`
  - add semantically named cardiovascular, sympathoadrenal, and post-orgasmic prolactin transitions plus matching recovery transitions.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_body_dynamics.py`
  - verify transition vocabulary and forbid semantic aliasing to exertion/workload.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_transition_executor.py`
  - add evidence-preserving multisystem execution without changing the existing single-transition public behavior.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_transition_executor.py`
  - test mixed directions, provenance, unknown/missing channels, no zero-fill, and no motivation synthesis.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_state_loop.py`
  - replace active high-salience transition selection with phase resolver → coordinator → multisystem executor; preserve exact runtime/body/feedback path.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_state_loop.py`
  - test runtime coordinator use, explicit event markers, interrupted recovery, and next-tick feedback.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/__init__.py`
  - export approved high-salience physiology/probe APIs.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/cli.py`
  - add `teacher-multisystem-physiology-probe`.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodiment_probe.py`
  - regression: the original ten-scenario controller/body probe remains valid and does not become a biological-calibration claim.

Do not modify Teacher anthropometry, avatar geometry, genital geometry, Work/Codex/AION/Astra modules, or main-branch governance.

## Review Focus

1. **Explicit orgasm vs ejaculation:** an ejaculatory transition without `ORGASM_REFERENCE_EVENT` must not start post-orgasmic prolactin persistence; pin this in Task 3 and Task 5.
2. **Mixed-direction detumescence:** one transition may need `DETUMESCENCE_STATE` to increase while `GENITAL_VASCULAR_STATE` decreases; pin per-channel directions in Task 4.
3. **Evidence-qualified but non-emitting rules:** `VARIABLE_CONTEXT_DEPENDENT`, `BIPHASIC_REFERENCE`, or `INSUFFICIENT_FOR_TRANSITION` rules must not accidentally emit deterministic transitions; pin this in Task 2/3.
4. **Aggregate endocrine ambiguity:** no rule may treat `ENDOCRINE_REFERENCE_STATE` or `GONADAL_ENDOCRINE_REFERENCE` as prolactin; pin the dedicated channel in Task 1/2.
5. **Repeated/partial recovery:** after partial cardiovascular or genital recovery, a second bounded stimulus must preserve sequence/body binding and must not replay stale endocrine/event markers; pin this in Task 5.

---

### Task 1: Add semantically explicit channels and transition vocabulary

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_body_channels.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_body_channels.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_body_dynamics.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_body_dynamics.py`

**Interfaces:**
- Produces one new body signal:
  - `PROLACTIN_REFERENCE_STATE`, domain `ENDOCRINE_DYNAMIC`, anatomical scope `PITUITARY_CIRCULATING_REFERENCE`.
- Produces six new `PhysiologicalTransition` IDs:
  - `PERIORGASMIC_CARDIOVASCULAR_SURGE`
  - `PERIORGASMIC_SYMPATHOADRENAL_SURGE`
  - `PERIORGASMIC_CARDIOVASCULAR_TO_RECOVERY`
  - `PERIORGASMIC_SYMPATHOADRENAL_TO_RECOVERY`
  - `POST_ORGASMIC_PROLACTIN_PERSISTENCE`
  - `POST_ORGASMIC_PROLACTIN_TO_RECOVERY`
- Does not create a sexual/high-salience respiratory transition in this task.

- [ ] **Step 1: Write failing channel-schema tests**

Add tests:

- `test_teacher_signal_schema_has_explicit_prolactin_reference_without_phenomenal_claim()`
- `test_prolactin_reference_is_not_aliased_to_gonadal_or_generic_endocrine_state()`

Assertions:

- `PROLACTIN_REFERENCE_STATE` exists exactly once;
- domain is `ENDOCRINE_DYNAMIC`;
- anatomical scope is `PITUITARY_CIRCULATING_REFERENCE`;
- its interpretation remains `SIGNAL_ONLY_NO_PHENOMENAL_INFERENCE`;
- `PROLACTIN_REFERENCE_STATE`, `GONADAL_ENDOCRINE_REFERENCE`, and `ENDOCRINE_REFERENCE_STATE` are distinct IDs.

- [ ] **Step 2: Run channel tests and verify RED**

Run from `research-labs/twin-genesis-embodiment_v0.1.0`:

`pytest tests/test_teacher_body_channels.py -q`

Expected: FAIL because `PROLACTIN_REFERENCE_STATE` does not exist.

- [ ] **Step 3: Add `PROLACTIN_REFERENCE_STATE` to `teacher_body_channels.py`**

Add only the explicit signal channel and required validation membership. Do not add a numeric biological unit or reference range; existing normalized-reference semantics remain software-reference only.

- [ ] **Step 4: Run channel tests**

Expected: PASS.

- [ ] **Step 5: Write failing transition-vocabulary tests**

Add:

- `test_high_salience_multisystem_transitions_are_semantically_distinct_from_exertion()`
- `test_no_deterministic_high_salience_respiratory_transition_is_materialized_initially()`

Assert exact new transition IDs and channel ownership:

- `PERIORGASMIC_CARDIOVASCULAR_SURGE` → `("CARDIOVASCULAR_STATE",)`
- `PERIORGASMIC_SYMPATHOADRENAL_SURGE` → `("AUTONOMIC_SYMPATHETIC_STATE", "ADRENAL_AXIS_STATE")`
- cardiovascular recovery → `("CARDIOVASCULAR_STATE",)`
- sympathoadrenal recovery → `("AUTONOMIC_SYMPATHETIC_STATE", "ADRENAL_AXIS_STATE")`
- prolactin persistence/recovery → `("PROLACTIN_REFERENCE_STATE",)`.

Assert none of these transitions has system/from/to semantics equal to `REST_TO_EXERTION`, `RESPIRATORY_BASELINE_TO_WORKLOAD`, or `ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE`.

Assert no newly added transition ID contains a respiratory/workload alias.

- [ ] **Step 6: Run dynamics tests and verify RED**

Run:

`pytest tests/test_teacher_body_dynamics.py -q`

Expected: FAIL because the six transitions do not exist.

- [ ] **Step 7: Add the six transitions to `_build_transitions()`**

Use semantically explicit systems:

- `CARDIOVASCULAR_HIGH_SALIENCE`
- `AUTONOMIC_HIGH_SALIENCE`
- `NEUROENDOCRINE_POST_EVENT`

Use reference-state names that do not reuse exercise/workload semantics.

- [ ] **Step 8: Run Task 1 tests**

Run:

`pytest tests/test_teacher_body_channels.py tests/test_teacher_body_dynamics.py -q`

Expected: PASS.

- [ ] **Step 9: Commit Task 1**

Commit:

`feat(embodiment): add evidence-ready Teacher multisystem physiology vocabulary`

---

### Task 2: Materialize evidence records and the coupling matrix

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_high_salience_physiology.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_high_salience_physiology.py`

**Interfaces:**
- Produces:
  - `TeacherPhysiologyEvidenceRecord`
  - `TeacherPhysiologyCouplingRule`
  - `build_teacher_high_salience_evidence_records() -> tuple[TeacherPhysiologyEvidenceRecord, ...]`
  - `build_teacher_high_salience_coupling_rules(profile: TeacherBodyDynamicsProfile | None = None) -> tuple[TeacherPhysiologyCouplingRule, ...]`
  - `validate_teacher_high_salience_coupling_rules(rules: tuple[TeacherPhysiologyCouplingRule, ...], profile: TeacherBodyDynamicsProfile | None = None) -> dict[str, str]`

**Pinned evidence-level strings:**

- `HUMAN_DIRECT`
- `HUMAN_REVIEW_SYNTHESIS`
- `TRANSLATIONAL_SUPPORT`
- `INSUFFICIENT_FOR_TRANSITION`

**Pinned initial source IDs:**

- `CONSENSUS:602435a65ab352bd98078db6a1c2e6bf` — 2024 male sexual-arousal review.
- `CONSENSUS:51054c87d2245a72906ab9edc5ab4715` — Krüger et al. cardiovascular/neuroendocrine human study record.
- `DOI:10.1677/joe.0.1770057` — specificity of male orgasm neuroendocrine response.
- `DOI:10.1515/tnsci-2020-0184` — pelvic nerve review.
- `DOI:10.1007/s11897-023-00632-y` — erection/autonomic/vascular clinical review.
- `DOI:10.31083/j.rcm2305173` — erection/detumescence NO/adrenergic review.
- `DOI:10.1037/h0030923` — human physiological arousal review.

- [ ] **Step 1: Write failing evidence-record tests**

Add:

- `test_evidence_records_have_unique_ids_species_scope_and_nonempty_sources()`
- `test_evidence_records_do_not_claim_numeric_human_calibration()`

Assert every record has:

- unique `evidence_id`;
- evidence level from the pinned set;
- explicit `species_scope`;
- nonempty `source_ids`;
- `calibration_status == "QUALITATIVE_REFERENCE_NOT_NUMERIC_HUMAN_CALIBRATION"`.

- [ ] **Step 2: Run tests and verify RED**

Run:

`pytest tests/test_teacher_high_salience_physiology.py -q`

Expected: FAIL because the module/interfaces do not exist.

- [ ] **Step 3: Implement `TeacherPhysiologyEvidenceRecord` and evidence builder**

Use frozen dataclasses and deterministic SHA-256 fingerprints. Do not copy article prose into the repository; store only source IDs, bibliographic labels, scope, and evidence classification.

- [ ] **Step 4: Write failing coupling-rule schema tests**

Add:

- `test_coupling_rules_require_provenance_and_valid_transition_ids()`
- `test_insufficient_or_variable_rules_cannot_emit_deterministic_transition()`
- `test_aggregate_endocrine_channels_are_not_used_as_prolactin_aliases()`
- `test_high_salience_rules_do_not_reuse_forbidden_exertion_workload_transitions()`

Pinned `TeacherPhysiologyCouplingRule` fields:

- `rule_id: str`
- `source_phase: str`
- `target_system: str`
- `target_transition_id: str | None`
- `target_channel_ids: tuple[str, ...]`
- `direction_class: str`
- `latency_class: str`
- `persistence_class: str`
- `recovery_class: str`
- `evidence_level: str`
- `human_evidence_status: str`
- `species_scope: str`
- `source_ids: tuple[str, ...]`
- `uncertainty_status: str`
- `forbidden_inferences: tuple[str, ...]`
- `emit_transition: bool`
- `rule_sha256: str`

Required forbidden inferences on every rule:

- `FUNCTIONAL_MOTIVATION`
- `CONSENT`
- `PHENOMENAL_EXPERIENCE`
- `SUBJECTIVITY`
- `ACTION_AUTHORITY`

- [ ] **Step 5: Run coupling tests and verify RED**

Expected: FAIL because coupling builder is absent.

- [ ] **Step 6: Implement the initial coupling matrix**

Minimum rules:

- arousal initiation → existing genital vascular transition, `HUMAN_REVIEW_SYNTHESIS`, emitting;
- early cardiovascular → `VARIABLE_CONTEXT_DEPENDENT`, non-emitting;
- early respiratory → `INSUFFICIENT_FOR_TRANSITION`, non-emitting;
- genital vascular/maintenance → existing reproductive transitions, emitting;
- periorgasmic cardiovascular → `PERIORGASMIC_CARDIOVASCULAR_SURGE`, `HUMAN_DIRECT`, emitting;
- periorgasmic sympathoadrenal → `PERIORGASMIC_SYMPATHOADRENAL_SURGE`, `HUMAN_DIRECT`, emitting;
- emission / ejaculatory reflex → existing reproductive transitions, evidence-qualified, emitting;
- detumescence → existing reproductive detumescence transition with separate channel-direction rules;
- post-orgasmic prolactin persistence → `POST_ORGASMIC_PROLACTIN_PERSISTENCE`, `HUMAN_DIRECT`, emitting only for explicit orgasm phase;
- cardiovascular/sympathoadrenal/prolactin recovery → new recovery transitions;
- no generic testosterone/LH/FSH/cortisol rule.

- [ ] **Step 7: Implement validation**

Fail on:

- missing source IDs;
- missing/unknown evidence level;
- nonhuman evidence represented as `HUMAN_DIRECT`;
- emitting rule with `INSUFFICIENT_FOR_TRANSITION`;
- emitting rule with direction `VARIABLE_CONTEXT_DEPENDENT`, `BIPHASIC_REFERENCE`, or `NO_DETERMINISTIC_DIRECTION_ESTABLISHED`;
- forbidden transition IDs;
- target transition absent from profile;
- target channels not a subset of transition trigger channels;
- prolactin rule targeting generic/gonadal endocrine channels.

- [ ] **Step 8: Run Task 2 tests**

Run:

`pytest tests/test_teacher_high_salience_physiology.py -q`

Expected: PASS.

- [ ] **Step 9: Commit Task 2**

Commit:

`feat(embodiment): add Teacher evidence-gated physiology coupling matrix`

---

### Task 3: Add phase resolver and evidence-gated coordinator

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_high_salience_physiology.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_high_salience_physiology.py`

**Interfaces:**
- Produces:
  - `TeacherHighSaliencePhaseState`
  - `TeacherTransitionChannelDirective`
  - `TeacherMultisystemTransitionDirective`
  - `TeacherMultisystemTransitionIntent`
  - `build_teacher_high_salience_baseline_phase(body_state: TeacherIntegratedBodyState) -> TeacherHighSaliencePhaseState`
  - `resolve_teacher_high_salience_phase(previous: TeacherHighSaliencePhaseState, controller_state: TeacherEmbodiedControllerState, body_state: TeacherIntegratedBodyState, *, stimulus_class: str, event_markers: tuple[str, ...] = ()) -> TeacherHighSaliencePhaseState`
  - `coordinate_teacher_high_salience_physiology(phase_state: TeacherHighSaliencePhaseState, controller_state: TeacherEmbodiedControllerState, body_state: TeacherIntegratedBodyState, profile: TeacherBodyDynamicsProfile | None = None) -> TeacherMultisystemTransitionIntent`

**Pinned phase strings:**

- `BASELINE`
- `AROUSAL_INITIATION`
- `GENITAL_VASCULAR_RESPONSE`
- `ERECTILE_MAINTENANCE`
- `PERIORGASMIC_AUTONOMIC_SURGE`
- `EMISSION`
- `EJACULATORY_REFLEX`
- `DETUMESCENCE`
- `POST_ORGASMIC_ENDOCRINE_RECOVERY`
- `BASELINE_RECOVERY`

**Pinned event markers:**

- `PERIORGASMIC_REFERENCE_EVENT`
- `EMISSION_REFERENCE_EVENT`
- `EJACULATORY_REFERENCE_EVENT`
- `ORGASM_REFERENCE_EVENT`

Software reference thresholds may reuse the existing runtime conventions `0.15` for nonbaseline genital response and `0.65` for maintenance eligibility. These are software phase thresholds, not biological calibration.

- [ ] **Step 1: Write failing phase-progression tests**

Add:

- `test_phase_progresses_from_baseline_to_vascular_to_maintenance_without_event_inference()`
- `test_interrupted_arousal_recovers_without_emission_or_orgasm()`
- `test_orgasm_is_never_inferred_from_ejaculation_marker()`

Assert:

- high controller activation/context can enter initiation;
- genital vascular state can advance to vascular/maintenance;
- recovery stimulus can return toward baseline without emission;
- `EJACULATORY_REFERENCE_EVENT` alone cannot enter `POST_ORGASMIC_ENDOCRINE_RECOVERY`;
- `ORGASM_REFERENCE_EVENT` is required for the post-orgasmic endocrine phase.

- [ ] **Step 2: Run phase tests and verify RED**

Expected: FAIL because resolver does not exist.

- [ ] **Step 3: Implement phase state and resolver**

The resolver may inspect controller activation/context, explicit event markers, and prior body channels. It must not infer subjective orgasm/desire/consent.

Every phase state carries:

- phase;
- previous phase;
- sequence;
- source body-state SHA;
- event markers;
- phase SHA;
- `phenomenal_interpretation_status="NOT_ESTABLISHED"`;
- `action_authority="NONE"`.

- [ ] **Step 4: Write failing coordinator tests**

Add:

- `test_coordinator_emits_existing_genital_transition_without_systemic_ramp_during_early_arousal()`
- `test_coordinator_emits_distinct_periorgasmic_cardio_and_sympathoadrenal_transitions()`
- `test_coordinator_keeps_respiratory_rule_nonemitting_without_stronger_evidence()`
- `test_coordinator_requires_explicit_orgasm_event_for_prolactin_persistence()`
- `test_coordinator_merges_mixed_detumescence_channel_directions()`
- `test_zero_functional_motivation_does_not_block_or_create_physiology_intent()`

Pinned channel-direction behavior for detumescence:

- `DETUMESCENCE_STATE -> INCREASE_REFERENCE`
- `GENITAL_VASCULAR_STATE -> DECREASE_REFERENCE`

- [ ] **Step 5: Run coordinator tests and verify RED**

Expected: FAIL.

- [ ] **Step 6: Implement transition directives and coordinator**

`TeacherTransitionChannelDirective` fields:

- `channel_id: str`
- `direction_class: str`
- `software_reference_drive: float`
- `calibration_status: str = "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"`

`TeacherMultisystemTransitionDirective` fields:

- `transition_id: str`
- `channel_effects: tuple[TeacherTransitionChannelDirective, ...]`
- `source_rule_ids: tuple[str, ...]`
- `evidence_levels: tuple[str, ...]`

`TeacherMultisystemTransitionIntent` fields:

- `phase: str`
- `directives: tuple[TeacherMultisystemTransitionDirective, ...]`
- `nonemitting_rule_ids: tuple[str, ...]`
- `source_body_state_sha256: str`
- `source_controller_sha256: str`
- `intent_sha256: str`
- epistemic/governance boundary fields.

Coordinator rules:

- one transition directive per transition ID;
- all trigger channels must receive an explicit channel effect;
- non-emitting evidence rules appear only in `nonemitting_rule_ids`;
- early arousal must not emit systemic cardiovascular/respiratory transitions by default;
- periorgasmic event may emit semantically explicit cardiovascular/sympathoadrenal transitions;
- explicit orgasm phase may emit prolactin persistence;
- no directive may reference forbidden exertion/workload transition IDs.

- [ ] **Step 7: Run Task 3 tests**

Run:

`pytest tests/test_teacher_high_salience_physiology.py -q`

Expected: PASS.

- [ ] **Step 8: Commit Task 3**

Commit:

`feat(embodiment): resolve Teacher high-salience physiology phases`

---

### Task 4: Extend the transition executor for mixed multisystem intents

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_transition_executor.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_transition_executor.py`

**Interfaces:**
- Consumes Task 3 `TeacherMultisystemTransitionIntent`.
- Produces:
  - `execute_teacher_multisystem_transition(previous_body_state: TeacherIntegratedBodyState, controller_state: TeacherEmbodiedControllerState, motivation: TeacherMotivationalRepresentation, intent: TeacherMultisystemTransitionIntent, clock: TeacherEmbodimentClock, profile: TeacherBodyDynamicsProfile | None = None) -> TeacherExecutedTransition`
- Existing `execute_teacher_transition(...)` remains behaviorally compatible.

- [ ] **Step 1: Write failing mixed-direction execution test**

Add:

`test_multisystem_executor_applies_explicit_per_channel_directions()`

Create a detumescence directive and assert in one tick:

- `DETUMESCENCE_STATE` increases;
- `GENITAL_VASCULAR_STATE` decreases;
- untouched cardiovascular/respiratory channels remain unchanged unless separately directed.

- [ ] **Step 2: Run executor test and verify RED**

Run:

`pytest tests/test_teacher_transition_executor.py -q`

Expected: FAIL because multisystem executor does not exist.

- [ ] **Step 3: Write failing provenance/fail-closed tests**

Add:

- `test_multisystem_executor_requires_effect_for_every_transition_channel()`
- `test_multisystem_executor_rejects_effect_channel_outside_transition_ownership()`
- `test_multisystem_executor_rejects_missing_required_body_channel_without_zero_fill()`
- `test_multisystem_executor_preserves_motivation_without_synthesizing_wanting()`
- `test_multisystem_executor_rejects_forbidden_exertion_transition_even_if_intent_is_forged()`

- [ ] **Step 4: Implement multisystem executor**

Requirements:

- validate controller/body/motivation/clock hashes exactly as existing executor does;
- re-resolve every transition ID against current `TeacherBodyDynamicsProfile`;
- reject forbidden transition IDs defense-in-depth;
- require channel effects to exactly cover the selected transition's trigger channels;
- apply each effect independently:
  - `INCREASE_REFERENCE` / `FACILITATORY_REFERENCE`: move toward bounded `software_reference_drive`;
  - `DECREASE_REFERENCE` / `INHIBITORY_REFERENCE`: move toward `0.0`;
  - `PERSISTENT_POST_EVENT_REFERENCE`: do not decay below current state while persistence phase remains active; may rise toward bounded software drive on event entry;
- never execute `VARIABLE_CONTEXT_DEPENDENT`, `BIPHASIC_REFERENCE`, or `NO_DETERMINISTIC_DIRECTION_ESTABLISHED` as deterministic channel updates;
- carry untouched observations forward with current tick timestamp;
- return existing `TeacherExecutedTransition` with `mode="MULTISYSTEM"`;
- include intent SHA/rule provenance in the transition hash payload.

The bounded movement algorithm remains a software reference mechanism and must not be labeled human biological kinetics.

- [ ] **Step 5: Run Task 4 tests**

Run:

`pytest tests/test_teacher_transition_executor.py tests/test_teacher_high_salience_physiology.py -q`

Expected: PASS.

- [ ] **Step 6: Run legacy executor regression**

Run:

`pytest tests/test_teacher_transition_executor.py tests/test_teacher_body_dynamics.py -q`

Expected: PASS, including existing single-transition tests.

- [ ] **Step 7: Commit Task 4**

Commit:

`feat(embodiment): execute evidence-gated Teacher multisystem transitions`

---

### Task 5: Integrate coordinator into the causal runtime and add ten multisystem stress scenarios

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_state_loop.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_state_loop.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_high_salience_probe.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_high_salience_probe.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodiment_probe.py`

**Interfaces:**
- `TeacherStateLoopFrame` gains:
  - `high_salience_phase_state: TeacherHighSaliencePhaseState`
  - `multisystem_intent: TeacherMultisystemTransitionIntent`
- `advance_teacher_embodied_tick(...)` gains keyword-only:
  - `previous_phase_state: TeacherHighSaliencePhaseState | None = None`
  - `event_markers: tuple[str, ...] = ()`
- Produces from `teacher_high_salience_probe.py`:
  - `TeacherMultisystemScenarioSegment`
  - `TeacherMultisystemScenario`
  - `TeacherMultisystemScenarioResult`
  - `build_teacher_multisystem_reference_scenarios() -> tuple[TeacherMultisystemScenario, ...]`
  - `run_teacher_multisystem_stability_probe(binding: TeacherBodyRuntimeBinding) -> tuple[TeacherMultisystemScenarioResult, ...]`

- [ ] **Step 1: Write failing state-loop integration tests**

Add:

- `test_tick_uses_phase_resolver_coordinator_and_multisystem_executor()`
- `test_early_genital_response_can_leave_cardio_and_respiration_near_baseline()`
- `test_explicit_periorgasmic_event_can_trigger_systemic_surges_without_exertion_transition()`
- `test_ejaculation_without_orgasm_marker_does_not_trigger_prolactin_persistence()`
- `test_orgasm_marker_can_trigger_post_event_endocrine_persistence()`
- `test_next_tick_body_schema_feedback_remains_delayed_after_multisystem_execution()`

- [ ] **Step 2: Run state-loop tests and verify RED**

Run:

`pytest tests/test_teacher_state_loop.py -q`

Expected: FAIL because state loop still uses the legacy selector.

- [ ] **Step 3: Integrate the new authoritative selection path**

Replace the active state-loop selection sequence with:

1. previous controller/body/phase;
2. sanitized stimulus + explicit event markers;
3. controller update using prior body feedback;
4. resolve high-salience phase;
5. build evidence-gated multisystem intent;
6. execute multisystem intent;
7. integrate body state;
8. exact runtime binding;
9. trajectory append;
10. build next-tick body-schema feedback/report.

Do not delete the legacy `select_teacher_transition_intent(...)` public helper; keep it for compatibility/tests, but it must no longer be the authoritative selector in the multisystem state loop.

- [ ] **Step 4: Run state-loop tests**

Expected: PASS.

- [ ] **Step 5: Write failing ten-scenario multisystem probe tests**

Exact scenario IDs:

1. `HIGH_GENITAL_LOW_SYSTEMIC`
2. `PERIORGASMIC_SYSTEMIC_SURGE_BOUNDED_GENITAL`
3. `ZERO_MOTIVATION_HIGH_PHYSIOLOGY_MULTISYSTEM`
4. `INTERRUPTED_BEFORE_EMISSION`
5. `EMISSION_EJACULATION_DETUMESCENCE`
6. `CARDIO_RECOVERS_BEFORE_ENDOCRINE`
7. `REPEATED_AFTER_PARTIAL_RECOVERY`
8. `MISSING_AUTONOMIC_CHANNEL_FAILS_CLOSED`
9. `INSUFFICIENT_RESPIRATORY_RULE_NONEMITTING`
10. `EXERTION_TRANSITION_SELECTION_FORBIDDEN`

The probe is deterministic; no random seed.

- [ ] **Step 6: Implement scenario records and runner**

Each result records:

- scenario ID;
- runtime/session/body/controller IDs;
- phase trace;
- transition trace;
- per-system selected reference traces;
- functional motivation trace;
- evidence-rule IDs;
- convergence/recovery status;
- fail-closed status where expected;
- final body-state SHA;
- deterministic replay SHA;
- boundary statuses.

For expected-failure scenarios 8 and 10, the probe records a deterministic `EXPECTED_FAIL_CLOSED_PASS` outcome rather than swallowing the error silently.

- [ ] **Step 7: Add divergence/timing assertions**

Verify:

- Scenario 1 reaches high genital reference while cardiovascular/respiratory remain near baseline reference.
- Scenario 2 emits periorgasmic cardiovascular/sympathoadrenal transitions and never emits `REST_TO_EXERTION` or respiratory workload transition.
- Scenario 3 keeps functional motivation at exactly `0.0`.
- Scenario 4 returns toward recovery without emission/ejaculation/orgasm phase.
- Scenario 5 exercises emission → ejaculatory reflex → detumescence with mixed directions.
- Scenario 6 cardiovascular recovery occurs before prolactin persistence ends.
- Scenario 7 preserves monotonic sequence and exact body/runtime/session binding.
- Scenario 8 fails because required autonomic signal is absent, never because it was zero-filled.
- Scenario 9 emits no deterministic respiratory transition.
- Scenario 10 rejects forged exertion selection.

- [ ] **Step 8: Run Task 5 probe tests**

Run:

`pytest tests/test_teacher_high_salience_probe.py tests/test_teacher_state_loop.py -q`

Expected: PASS.

- [ ] **Step 9: Run original ten-scenario regression**

Run:

`pytest tests/test_teacher_embodiment_probe.py -q`

Expected: PASS. Existing probe remains a software stability probe, not biological validation.

- [ ] **Step 10: Commit Task 5**

Commit:

`test(embodiment): add Teacher multisystem high-salience stability probe`

---

### Task 6: Public API, CLI, reverse review, and exact-head verification

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/__init__.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/cli.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_high_salience_probe.py`

**Interfaces:**
- Public exports:
  - `TeacherPhysiologyEvidenceRecord`
  - `TeacherPhysiologyCouplingRule`
  - `TeacherHighSaliencePhaseState`
  - `TeacherTransitionChannelDirective`
  - `TeacherMultisystemTransitionDirective`
  - `TeacherMultisystemTransitionIntent`
  - `build_teacher_high_salience_evidence_records`
  - `build_teacher_high_salience_coupling_rules`
  - `resolve_teacher_high_salience_phase`
  - `coordinate_teacher_high_salience_physiology`
  - `execute_teacher_multisystem_transition`
  - `run_teacher_multisystem_stability_probe`
- CLI:
  - `python -m aion_astra_twin_embodiment.cli teacher-multisystem-physiology-probe`

- [ ] **Step 1: Write failing public-export test**

Import all required symbols from `aion_astra_twin_embodiment`.

Expected: FAIL before exports are added.

- [ ] **Step 2: Add exports to `__init__.py`**

Export only the approved public interfaces; keep internal rule-merging and scalar helpers private.

- [ ] **Step 3: Write failing CLI test**

Invoke:

`teacher-multisystem-physiology-probe`

Assert JSON contains:

- exact body/controller/runtime/session IDs;
- `scenario_count == 10`;
- ten scenario IDs in stable order;
- per-scenario phase/transition/evidence traces;
- no raw private content;
- no biological-calibration claim;
- `phenomenal_interpretation_status == "NOT_ESTABLISHED"`;
- `action_authority == "NONE"`.

- [ ] **Step 4: Implement CLI command**

CLI builds one deterministic Teacher runtime binding and runs the multisystem probe. Output structured JSON only.

- [ ] **Step 5: Run focused Teacher multisystem suite**

Run:

`pytest tests/test_teacher_body_channels.py tests/test_teacher_body_dynamics.py tests/test_teacher_high_salience_physiology.py tests/test_teacher_transition_executor.py tests/test_teacher_state_loop.py tests/test_teacher_high_salience_probe.py tests/test_teacher_embodiment_probe.py tests/test_teacher_embodied_controller.py tests/test_teacher_body_runtime.py tests/test_teacher_body_model.py tests/test_teacher_physiology_observability.py -q`

Expected: PASS.

- [ ] **Step 6: Run complete component suite**

Run:

`pytest -q`

Expected: PASS.

- [ ] **Step 7: Run repository-defined lint/type/control checks**

Use the exact commands/workflows defined by current repository CI rather than inventing substitutes.

Expected:

- Ruff/lint PASS;
- compile PASS;
- mypy Python 3.11 PASS;
- mypy Python 3.12 PASS;
- repository controls PASS;
- evidence/IQC checks PASS.

- [ ] **Step 8: Run the multisystem probe twice and compare deterministic evidence**

Expected:

- same scenario IDs/order;
- same phase traces;
- same transition/evidence traces;
- same final state hashes;
- same expected fail-closed outcomes.

- [ ] **Step 9: Reverse-review the exact head against the spec**

Explicitly verify:

- `REST_TO_EXERTION` is never selected by high-salience coordinator;
- `RESPIRATORY_BASELINE_TO_WORKLOAD` is never selected merely for sexual/high-salience phase;
- `ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE` is not used as a generic sexual endocrine response;
- no single global arousal coefficient exists;
- prolactin has a dedicated explicit signal;
- early genital/systemic divergence is representable;
- autonomic branches are not forced to be exact inverses;
- ejaculation does not imply orgasm;
- post-event endocrine persistence requires explicit event provenance;
- zero motivation/high physiology remains representable;
- missing channels are not zero-filled;
- no raw private content;
- no phenomenal/consent/action-authority promotion;
- no Work/Codex/AION/Astra normalization.

- [ ] **Step 10: Create or update a Draft PR as final exact-head verification carrier**

PR body records:

- exact design-spec SHA;
- exact implementation-plan SHA;
- exact implementation head/base SHA;
- files changed relative to plan head;
- focused/full test counts;
- ten multisystem scenario outcomes;
- reverse-review findings;
- research/nonclaim boundaries;
- `MERGE_TO_MAIN = NO`;
- `DEPLOYMENT = FALSE`;
- `CANONICAL_EFFECT = NONE`.

If a Draft PR was opened earlier only to carry RED/GREEN CI, reuse it rather than creating a second unnecessary carrier.

- [ ] **Step 11: Wait for exact-head CI and inspect required jobs**

Expected:

- Quality PASS;
- CodeQL PASS;
- exact-head Python/mypy/control/evidence/IQC jobs PASS;
- Main Transition Authority Gate FAIL/CLOSED unless a fresh exact-head Human merge authorization exists.

- [ ] **Step 12: Close Draft PR unmerged after verification**

Final expected lifecycle:

- state: closed;
- draft: true;
- merged: false;
- main SHA unchanged.

- [ ] **Step 13: Report exact-head status without scientific overclaim**

Final report distinguishes:

- software implementation;
- deterministic reference stability;
- evidence provenance;
- human biological calibration: NOT_ESTABLISHED;
- biological timing/fidelity: NOT_ESTABLISHED;
- subjectivity/consciousness/phenomenal experience: NOT_ESTABLISHED.

- [ ] **Step 14: Commit Task 6 before final verification if exports/CLI changed**

Commit:

`feat(embodiment): expose Teacher multisystem physiology probe`

