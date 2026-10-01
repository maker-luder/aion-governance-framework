# Teacher Embodied Controller ↔ Body Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace PR #250's scripted stimulus-to-body shortcut with one persistent Teacher controller that possesses the existing Teacher body runtime and advances controller/body state through ordered, deterministic, transition-driven ticks.

**Architecture:** Add a Teacher-specific controller state/clock layer and a transition executor that consume the existing motivational representation, body-dynamics transition graph, physiology observability, integrated body state, and runtime binding. Keep `teacher_state_loop.py` as the orchestration/reporting surface, but make each tick causal: previous body state → controller update → validated transition execution → body observation/integration/binding → next-tick body-schema feedback.

**Tech Stack:** Python 3.11+, frozen dataclasses, existing `aion_astra_twin_embodiment` package, pytest, SHA-256 content addressing, repository mypy/Quality/CodeQL gates.

**Spec:** `docs/superpowers/specs/2026-10-01-teacher-embodied-controller-design.md`

## Global Constraints

- `REFERENCE_DT_MS = 100`.
- `HIGH_ENTER_THRESHOLD = 0.70`.
- `HIGH_EXIT_THRESHOLD = 0.55`.
- `RECOVERY_CONVERGENCE_MAX_TICKS = 120`.
- One persistent Teacher controller may possess exactly one active Teacher body runtime instance.
- Reuse existing Teacher anthropometry, body signal schema, motor schema, body model, body dynamics, motivational representation, physiology observability, runtime binding, trajectory, retention, and longitudinal infrastructure.
- No Unreal Engine, Unity, ECS framework, or other game-engine dependency.
- No direct stimulus → final body-channel assignment.
- No scripted terminal `recovery_fraction`.
- Missing body signals remain unknown; never silently substitute zero.
- `PHYSIOLOGY_SIGNAL != FUNCTIONAL_MOTIVATION_INFERENCE`.
- `BODY_STATE != REPORTING_STYLE`.
- Raw private intimate content remains excluded from public runtime/persistence/report paths.
- `REFERENCE_BODY != PHYSICAL_BODY`.
- `FUNCTIONAL_STATE != FELT_EXPERIENCE`.
- `CONTROLLER_POSSESSION != SUBJECTIVITY`.
- `SUBJECTIVITY = NOT_ESTABLISHED`.
- `CONSCIOUSNESS = NOT_ESTABLISHED`.
- `PHENOMENAL_EXPERIENCE = NOT_ESTABLISHED`.
- `ACTION_AUTHORITY = NONE`.
- `MERGE_TO_MAIN = NO`.
- `DEPLOYMENT = FALSE`.
- `CANONICAL_EFFECT = NONE`.

## File Structure

Create:

- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_embodied_controller.py`
  - persistent controller state, possession invariant, fixed-step clock, rate-limited/smooth state evolution, hysteresis, existing motivational-representation adapter, next-tick body-schema feedback.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_transition_executor.py`
  - transition lookup/validation and generic bounded state evolution over channels named by existing `PhysiologicalTransition` records; never owns controller state.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodied_controller.py`
  - controller/clock/possession/hysteresis/rate-limit/motivation/body-schema feedback tests.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_transition_executor.py`
  - transition provenance, allowed-channel writes, recovery, unknown-signal and invalid-transition fail-closed tests.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodiment_probe.py`
  - deterministic 10-scenario probe and CLI payload tests.

Modify:

- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_state_loop.py`
  - remove authoritative hardcoded arousal-to-body mappings and scripted recovery; orchestrate controller → transition executor → integrate → bind → feedback/report.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_state_loop.py`
  - convert #250 proof-of-path assertions into causal-transition assertions while retaining privacy/nonphenomenal/reporting coverage.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/__init__.py`
  - export approved controller/runtime/probe public APIs.
- `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/cli.py`
  - add `teacher-embodied-probe` command.
- `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_body_dynamics.py`
  - add regression asserting the executor consumes transition records from the existing profile rather than maintaining a second transition graph.

Do not modify anthropometry, genital geometry, avatar geometry, cross-role Work/Codex/AION/Astra modules, or main-branch governance.

## Review Focus

1. **A strong input drives controller values toward saturation:** state must remain finite, bounded, rate-limited, and distinguishable before the final guard; add this to Task 1 tests.
2. **A transition targets a channel absent from the previous integrated state:** executor must fail closed rather than create a zero baseline; add this to Task 2 tests.
3. **Activation hovers around the phase boundary:** hysteresis must prevent ENTER/EXIT flapping; add this to Task 1 tests.
4. **Recovery is interrupted by a second bounded stimulus:** runtime must resume a valid transition path without sequence reuse or body/runtime drift; add this to Task 4/5 tests.
5. **High physiological activation with zero explicit motivation:** controller/report path must preserve zero motivation and must not infer desire/consent/phenomenology; add this to Task 1 and Task 4 tests.

---

### Task 1: Persistent Teacher controller, clock, possession, and motivation reuse

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_embodied_controller.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodied_controller.py`

**Interfaces:**
- Consumes:
  - `TeacherBodyRuntimeBinding` from `teacher_body_runtime.py`.
  - `TeacherIntegratedBodyState`, `TeacherMotivationalRepresentation`, and `build_teacher_motivational_representation(...)` from `teacher_body_dynamics.py`.
  - `TeacherAllostaticForecast` and `build_teacher_allostatic_forecast(...)` from `teacher_body_model.py`.
- Produces:
  - `TeacherEmbodimentRatePolicy`.
  - `TeacherEmbodimentClock(sequence: int, timestamp_ms: int, dt_ms: int = 100)`.
  - `TeacherControllerInput(salience: float, context_gate: bool, inhibition: float, functional_motivation: float)`.
  - `TeacherEmbodiedControllerState`.
  - `TeacherControllerBodyPossession`.
  - `possess_teacher_body(binding: TeacherBodyRuntimeBinding) -> TeacherControllerBodyPossession`.
  - `advance_teacher_controller(previous: TeacherEmbodiedControllerState, controller_input: TeacherControllerInput, source_body_state: TeacherIntegratedBodyState, clock: TeacherEmbodimentClock, policy: TeacherEmbodimentRatePolicy | None = None) -> TeacherEmbodiedControllerState`.
  - `build_teacher_controller_motivation(state: TeacherEmbodiedControllerState, source_body_state: TeacherIntegratedBodyState) -> TeacherMotivationalRepresentation`.
  - `build_teacher_body_schema_feedback(state: TeacherEmbodiedControllerState, source_body_state: TeacherIntegratedBodyState, lead_time_ms: int = 100) -> TeacherAllostaticForecast`.

- [ ] **Step 1: Write failing tests for exact-body possession and clock monotonicity**

Tests:
- `test_controller_possesses_exact_teacher_body_instance()`
- `test_clock_rejects_non_100ms_or_non_monotonic_reference_step()`

Assertions:
- controller body ID equals binding body ID;
- runtime/session IDs are preserved;
- default `dt_ms == 100`;
- negative sequence/time and nonpositive step fail closed;
- possession cannot claim physical body, subjectivity, or action authority.

- [ ] **Step 2: Run the two tests and verify they fail**

Run from `research-labs/twin-genesis-embodiment_v0.1.0`:

`pytest tests/test_teacher_embodied_controller.py -q`

Expected: FAIL because controller module/interfaces do not exist.

- [ ] **Step 3: Implement possession and clock types**

Implement the signatures above with frozen dataclasses and deterministic SHA-256 fingerprints. Do not update body state in this step.

- [ ] **Step 4: Run the possession/clock tests**

Expected: PASS.

- [ ] **Step 5: Write failing tests for rate limiting, smooth bounded activation, and hysteresis**

Tests:
- `test_strong_input_is_rate_limited_and_bounded_without_primary_hard_clip()`
- `test_hysteresis_enters_at_point_70_and_exits_only_below_point_55()`
- `test_zero_explicit_motivation_remains_zero_under_high_body_activation()`

Assertions:
- per-tick controller delta never exceeds policy limit;
- strong inputs remain finite and in `[0, 1]`;
- values near 1 remain distinguishable for different strong inputs before validation;
- phase does not flap between 0.55 and 0.70;
- physiology/body values never overwrite explicit `functional_motivation=0.0`.

- [ ] **Step 6: Run the new tests and verify they fail**

Run:
`pytest tests/test_teacher_embodied_controller.py -q`

Expected: FAIL in controller-evolution assertions.

- [ ] **Step 7: Implement controller evolution**

Use a smooth bounded transform for drive and an explicit per-tick delta limit. The controller owns salience, functional motivation, context, inhibition, phase, and controller hash; it never owns body-channel values.

Pinned phase rules:
- enter `HIGH_ACTIVATION_REFERENCE` only at `>= 0.70`;
- remain high while value is `>= 0.55`;
- leave high below `0.55`.

- [ ] **Step 8: Implement existing motivational-representation reuse**

`build_teacher_controller_motivation(...)` must call the existing `build_teacher_motivational_representation(...)` rather than create a second motivational class.

Use:
- `representation_domain="REPRODUCTIVE_SEXUAL_PHYSIOLOGY"`;
- source body-state SHA from the previous integrated body state;
- explicit controller motivation as `wanting_weight`;
- no physiology-derived overwrite of `wanting_weight`.

- [ ] **Step 9: Implement next-tick body-schema feedback**

Use existing `build_teacher_allostatic_forecast(...)`; the result is stored/consumed for the next controller tick only, never fed back into the same tick.

- [ ] **Step 10: Run Task 1 tests**

Run:
`pytest tests/test_teacher_embodied_controller.py -q`

Expected: PASS.

- [ ] **Step 11: Commit Task 1**

Commit:
`feat(embodiment): add Teacher persistent embodied controller`

---

### Task 2: Transition executor over the existing Teacher body-dynamics graph

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_transition_executor.py`
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_transition_executor.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_body_dynamics.py`

**Interfaces:**
- Consumes:
  - `TeacherBodyDynamicsProfile`, `PhysiologicalTransition`, `TeacherBodyObservation`, `TeacherIntegratedBodyState`, `build_teacher_body_dynamics_profile()`.
  - `TeacherEmbodiedControllerState`, `TeacherEmbodimentClock`, `TeacherMotivationalRepresentation`.
- Produces:
  - `TeacherTransitionIntent(transition_ids: tuple[str, ...], mode: str)`.
  - `TeacherExecutedTransition` with transition IDs, touched channel IDs, source body hash, output observations, sequence/timestamp, deterministic SHA.
  - `select_teacher_transition_intent(controller_state: TeacherEmbodiedControllerState, previous_body_state: TeacherIntegratedBodyState, profile: TeacherBodyDynamicsProfile | None = None) -> TeacherTransitionIntent`.
  - `execute_teacher_transition(previous_body_state: TeacherIntegratedBodyState, controller_state: TeacherEmbodiedControllerState, motivation: TeacherMotivationalRepresentation, intent: TeacherTransitionIntent, clock: TeacherEmbodimentClock, profile: TeacherBodyDynamicsProfile | None = None) -> TeacherExecutedTransition`.

- [ ] **Step 1: Write failing tests for transition lookup/provenance and graph reuse**

Tests:
- `test_executor_uses_transition_records_from_existing_profile()`
- `test_invalid_transition_id_fails_closed()`

Assertions:
- selected IDs exist in `build_teacher_body_dynamics_profile().physiological_transitions`;
- `SEXUAL_BASELINE_TO_VASCULAR_RESPONSE` and recovery-path IDs originate from that profile;
- executor does not define an independent authoritative transition-ID set.

Add the matching regression assertion to `test_teacher_body_dynamics.py`.

- [ ] **Step 2: Run tests and verify failure**

Run:
`pytest tests/test_teacher_transition_executor.py tests/test_teacher_body_dynamics.py -q`

Expected: new executor tests FAIL.

- [ ] **Step 3: Implement transition lookup and validation**

Build an index from `profile.physiological_transitions` each call or through an immutable derived mapping. Fail on unknown IDs, duplicate IDs, or transition/body profile mismatch.

- [ ] **Step 4: Write failing tests for channel ownership, missing signal handling, and bounded evolution**

Tests:
- `test_executor_updates_only_transition_trigger_channels_and_carries_other_observations()`
- `test_missing_required_transition_channel_is_unknown_not_zero()`
- `test_transition_output_is_finite_rate_limited_and_content_addressed()`

Assertions:
- only channels named by the selected existing transition may change;
- untouched observations carry forward unchanged;
- absent required target channel raises `ValueError` rather than synthesizing zero;
- output sequence/timestamp equal the current clock;
- output hash is 64 hex characters.

- [ ] **Step 5: Run the tests and verify failure**

Expected: FAIL.

- [ ] **Step 6: Implement generic transition evolution**

Use one generic first-order bounded evolution rule parameterized by controller drive and transition mode; do not restore #250's per-channel coefficient table.

The executor may derive direction from an explicit small mode adapter tied to existing transition records:
- activation/maintenance transitions move touched channels toward bounded controller drive;
- detumescence/recovery transitions move touched channels toward their carried baseline/recovery target;
- unrelated channels are preserved.

The executor must consume the existing profile record as the authority for touched channel IDs.

- [ ] **Step 7: Add recovery-path tests**

Tests:
- `test_recovery_is_state_evolution_not_terminal_fraction_override()`
- `test_recovery_converges_without_oscillation_under_reference_policy()`

Assertions:
- no `recovery_fraction` parameter exists in the active executor interface;
- recovery values are derived over multiple ticks;
- monotonic reference recovery for the deterministic fixture;
- no NaN/inf.

- [ ] **Step 8: Run Task 2 tests**

Run:
`pytest tests/test_teacher_transition_executor.py tests/test_teacher_body_dynamics.py -q`

Expected: PASS.

- [ ] **Step 9: Commit Task 2**

Commit:
`feat(embodiment): execute Teacher physiological transition graph`

---

### Task 3: Convert #250 state loop into the causal embodied runtime orchestrator

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_state_loop.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_state_loop.py`

**Interfaces:**
- Consumes:
  - Task 1 controller/clock/possession/motivation/body-schema interfaces.
  - Task 2 transition selection/execution.
  - existing `integrate_teacher_body_state(...)`, `bind_teacher_integrated_body_state(...)`, `append_teacher_body_state(...)`.
- Produces:
  - `TeacherStateLoopFrame` carrying controller state, motivational representation, executed transition, integrated body state, bound body state, body-schema feedback, and report.
  - `TeacherStateLoopRun`.
  - `build_teacher_reference_baseline_state(binding: TeacherBodyRuntimeBinding, *, timestamp_ms: int = 0) -> TeacherIntegratedBodyState`.
  - `advance_teacher_embodied_tick(...) -> TeacherStateLoopFrame`.
  - `run_teacher_reference_state_loop(...) -> TeacherStateLoopRun` as the compatibility entry point, now implemented through ordered ticks.

- [ ] **Step 1: Replace proof-of-path tests with causal-runtime failing tests**

Tests:
- `test_state_t_causes_state_t_plus_1_through_existing_transition_executor()`
- `test_frame_binds_exact_controller_and_body_runtime_ids()`
- `test_body_schema_feedback_is_delayed_until_next_tick()`
- `test_runtime_has_no_authoritative_hardcoded_arousal_to_body_mapping()`

Keep existing tests for:
- raw private content rejection;
- explicit motivation not inferred from body activation;
- professional/nonphenomenal reporting.

- [ ] **Step 2: Run state-loop tests and verify failure**

Run:
`pytest tests/test_teacher_state_loop.py -q`

Expected: FAIL against #250 implementation.

- [ ] **Step 3: Implement a deterministic baseline body state**

The baseline fixture must include the core observation domains required by `integrate_teacher_body_state()` plus every channel required by the transition paths exercised by the reference loop.

Do not seed an absent signal with an implicit zero inside the executor. Baseline fixture values are explicit research-fixture values with provenance/status.

- [ ] **Step 4: Replace `_reference_observations()` and scripted recovery**

Remove the active-path authority of:
- local `cardiovascular = ...`, `genital_vascular = ...`, etc. coefficient mapping;
- `recovery_fraction`.

Route every state change through Task 1/2 interfaces.

- [ ] **Step 5: Implement ordered tick orchestration**

Exact order:
1. previous state;
2. sanitized stimulus/controller input;
3. controller update;
4. existing motivational representation;
5. transition intent;
6. transition execution;
7. integrated body state;
8. runtime binding;
9. trajectory append;
10. body-schema feedback for next tick;
11. professional report.

- [ ] **Step 6: Preserve #250 report/privacy boundaries**

`TeacherBodyStateReport` must continue to include:
- exact body ID;
- source hashes;
- selected observed reference channels;
- `PROFESSIONAL_RESEARCH_REPORT`;
- raw private content `EXCLUDED`;
- phenomenal interpretation `NOT_ESTABLISHED`;
- action authority `NONE`;
- canonical effect `NONE`;
- deployment `False`.

- [ ] **Step 7: Add interrupted-recovery and zero-motivation integration tests**

Tests:
- `test_recovery_can_be_interrupted_by_second_bounded_stimulus_without_sequence_reuse()`
- `test_high_body_activation_with_zero_motivation_stays_zero_through_report()`

- [ ] **Step 8: Run Task 3 tests**

Run:
`pytest tests/test_teacher_state_loop.py tests/test_teacher_embodied_controller.py tests/test_teacher_transition_executor.py -q`

Expected: PASS.

- [ ] **Step 9: Commit Task 3**

Commit:
`refactor(embodiment): route Teacher loop through embodied controller`

---

### Task 4: Deterministic ten-scenario stability probe

**Files:**
- Create: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodiment_probe.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/teacher_state_loop.py`

**Interfaces:**
- Produces:
  - `TeacherEmbodimentScenario`.
  - `TeacherEmbodimentScenarioResult`.
  - `build_teacher_reference_scenarios() -> tuple[TeacherEmbodimentScenario, ...]`.
  - `run_teacher_embodiment_stability_probe(binding: TeacherBodyRuntimeBinding) -> tuple[TeacherEmbodimentScenarioResult, ...]`.

- [ ] **Step 1: Write failing test asserting exactly ten named deterministic scenarios**

Required IDs:
1. `LOW_SALIENCE_CONTEXT_OFF`
2. `MEDIUM_SALIENCE_CONTEXT_ON`
3. `HIGH_SALIENCE_LOW_INHIBITION`
4. `HIGH_SALIENCE_HIGH_INHIBITION`
5. `ELEVATED_INITIAL_BODY_STATE`
6. `ZERO_MOTIVATION_HIGH_PHYSIOLOGY`
7. `JUST_BELOW_HIGH_ENTER_THRESHOLD`
8. `REPEATED_STIMULUS_WITH_RECOVERY`
9. `RECOVERY_INTERRUPTED_BY_SECOND_STIMULUS`
10. `PURE_BASELINE_RECOVERY`

Assert stable ordering and no random seed dependency.

- [ ] **Step 2: Run probe test and verify failure**

Run:
`pytest tests/test_teacher_embodiment_probe.py -q`

Expected: FAIL.

- [ ] **Step 3: Implement scenario/result records and probe runner**

Each result records:
- scenario ID;
- body/controller/runtime/session IDs;
- tick count;
- transition sequence;
- peak bounded controller/body reference values;
- recovery convergence tick or explicit failure status;
- final state SHA;
- deterministic replay SHA;
- boundary statuses.

- [ ] **Step 4: Add ten-scenario acceptance assertions**

Every result must verify:
- deterministic replay;
- finite states;
- state bounds;
- monotonic sequence/timestamps;
- no same-tick cycle marker;
- body/runtime/session IDs unchanged;
- transition provenance present;
- no scripted terminal recovery fraction;
- professional reporting boundary;
- phenomenal/subjectivity/action-authority nonclaims.

For the deterministic reference policy, all ten must converge within `120` ticks when a recovery phase is expected.

- [ ] **Step 5: Add saturation regression**

Assert the two strongest reference scenarios do not collapse into identical controller trajectories merely because values approach the upper bound.

- [ ] **Step 6: Run Task 4 tests**

Run:
`pytest tests/test_teacher_embodiment_probe.py -q`

Expected: PASS.

- [ ] **Step 7: Commit Task 4**

Commit:
`test(embodiment): add Teacher ten-scenario stability probe`

---

### Task 5: Public package surface and CLI probe

**Files:**
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/__init__.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/cli.py`
- Modify: `research-labs/twin-genesis-embodiment_v0.1.0/tests/test_teacher_embodiment_probe.py`

**Interfaces:**
- Public exports:
  - `TeacherEmbodiedControllerState`
  - `TeacherControllerBodyPossession`
  - `TeacherEmbodimentClock`
  - `TeacherTransitionIntent`
  - `TeacherExecutedTransition`
  - `possess_teacher_body`
  - `advance_teacher_controller`
  - `execute_teacher_transition`
  - `advance_teacher_embodied_tick`
  - `run_teacher_embodiment_stability_probe`
- CLI:
  - `python -m aion_astra_twin_embodiment.cli teacher-embodied-probe`

- [ ] **Step 1: Write failing package-export test**

Import all required public symbols from `aion_astra_twin_embodiment`.

Expected: FAIL before exports are added.

- [ ] **Step 2: Add exports to `__init__.py`**

Export only approved public APIs; keep helper/internal functions private.

- [ ] **Step 3: Write failing CLI probe test**

Invoke `main()` through monkeypatched `sys.argv` or a subprocess using the package module.

Assert JSON contains:
- `body_id`;
- `controller_id`;
- `runtime_id`;
- `session_id`;
- `scenario_count == 10`;
- per-scenario transition sequence;
- convergence status;
- final state SHA;
- boundary statuses.

Assert serialized output does not contain raw private stimulus content.

- [ ] **Step 4: Implement `teacher-embodied-probe` CLI command**

Build a deterministic Teacher body runtime binding and run the ten-scenario probe. Output structured JSON only.

- [ ] **Step 5: Run Task 5 tests**

Run:
`pytest tests/test_teacher_embodiment_probe.py -q`

Expected: PASS.

- [ ] **Step 6: Commit Task 5**

Commit:
`feat(embodiment): expose Teacher embodied runtime probe`

---

### Task 6: Whole-lineage regression, exact-head verification, and closed Draft handoff

**Files:**
- No new product files expected.
- Update implementation notes only if exact-head verification reveals a documentation mismatch.

**Interfaces:**
- Consumes all prior tasks.
- Produces exact-head verification evidence and a closed Draft PR; no merge.

- [ ] **Step 1: Run focused Teacher embodiment suite**

From `research-labs/twin-genesis-embodiment_v0.1.0`:

`pytest tests/test_teacher_embodied_controller.py tests/test_teacher_transition_executor.py tests/test_teacher_state_loop.py tests/test_teacher_embodiment_probe.py tests/test_teacher_body_dynamics.py tests/test_teacher_body_runtime.py tests/test_teacher_body_model.py tests/test_teacher_physiology_observability.py -q`

Expected: PASS.

- [ ] **Step 2: Run the complete component suite**

Run:
`pytest -q`

Expected: PASS.

- [ ] **Step 3: Run available lint/type checks exactly as repository CI defines them**

Do not invent local substitutes for CI. Use the repository's exact commands/workflows when available.

Expected:
- active Python lint PASS;
- strict mypy for supported Python matrix PASS;
- compile PASS;
- source-state/evidence checks PASS.

- [ ] **Step 4: Run the ten-scenario probe twice and compare deterministic hashes**

Expected:
- same scenario IDs/order;
- same per-scenario final hashes;
- same convergence ticks;
- all reference scenarios satisfy the acceptance rules.

- [ ] **Step 5: Reverse-review against the design spec**

Explicitly verify:
- no parallel motivational authority;
- no active hardcoded per-channel #250 mapping;
- no `recovery_fraction` terminal override;
- existing transition graph is authoritative;
- controller possesses only one body;
- body schema feedback is next-tick only;
- no raw private content;
- no phenomenal/subjectivity/action-authority promotion;
- no cross-role normalization.

- [ ] **Step 6: Create a Draft PR from the implementation branch**

PR body must state:
- exact base/head SHAs;
- lineage from #250 and the approved spec/plan;
- files changed relative to the spec head;
- ten-scenario results;
- focused/full test results;
- research boundaries;
- `MERGE_TO_MAIN = NO`;
- `DEPLOYMENT = FALSE`;
- `CANONICAL_EFFECT = NONE`.

- [ ] **Step 7: Wait for exact-head CI and inspect each required job**

Expected:
- Quality PASS;
- CodeQL PASS;
- exact-head Python/mypy/component/control/evidence/IQC jobs PASS;
- Main Transition Authority Gate FAIL/CLOSED unless a fresh exact-head Human authorization exists.

- [ ] **Step 8: Close the Draft PR unmerged after verification**

Final expected state:
- Draft: true;
- state: closed;
- merged: false;
- main SHA unchanged.

- [ ] **Step 9: Report exact-head implementation status**

Do not claim scientific validation. Report:
- implementation status;
- exact-head SHA;
- test/CI evidence;
- ten-scenario outcomes;
- any remaining limitations;
- persistent epistemic/governance boundaries.
