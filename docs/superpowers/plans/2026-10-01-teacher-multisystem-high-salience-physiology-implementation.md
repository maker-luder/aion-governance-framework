# Teacher Multi-System High-Salience Physiology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use superpowers:test-driven-development and execute each task with a RED -> GREEN -> refactor sequence.

**Goal:** Add an evidence-bounded multi-system coupling layer to the causally connected Teacher Controller ↔ Body runtime without fabricating deterministic cardiovascular, respiratory, or endocrine dynamics.

**Spec:** `docs/superpowers/specs/2026-10-01-teacher-multisystem-high-salience-physiology-design.md`

**Lineage base:** `26c8cb74a10f99696a36a8ac387ee78c66da1dee`

**Branch:** `research/teacher-multisystem-high-salience-physiology-20261001`

**Governance:** `MERGE_TO_MAIN = NO`, `DEPLOYMENT = FALSE`, `CANONICAL_EFFECT = NONE`.

## Task 1 — Evidence-bounded coupling profile

**Create**
- `src/aion_astra_twin_embodiment/teacher_high_salience_coupling.py`
- `tests/test_teacher_high_salience_coupling.py`

Implement immutable:
- `TeacherHighSalienceCouplingRule`
- `TeacherHighSalienceCouplingProfile`
- `build_teacher_high_salience_coupling_profile()`
- `validate_teacher_high_salience_coupling_profile()`

Required coupling classes:
- `DIRECT_REFERENCE_CAUSAL`
- `ASSOCIATED_BOUNDED_REFERENCE`
- `EVENT_DRIVEN_REFERENCE`
- `SLOW_OBSERVATION_ONLY`

Required rules:
- autonomic/genital direct-reference rule;
- cardiovascular associated-only rule;
- respiratory associated-only rule;
- emission autonomic/reproductive evidence rule;
- expulsion somatic/reproductive evidence rule;
- post-climactic endocrine evidence-only rule.

RED tests must assert:
- unique coupling IDs;
- all target channels exist;
- non-empty DOI/PMID evidence IDs;
- `REST_TO_EXERTION` absent from this profile;
- cardiovascular/respiratory execution status = `OBSERVE_NOT_FORCE`;
- prolactin runtime channel = `NOT_MATERIALIZED`;
- acute gonadal endocrine automatic drive = absent;
- phenomenal/subjectivity/action-authority boundaries preserved.

Commit:
`feat(embodiment): add Teacher evidence-bounded coupling profile`

## Task 2 — Correct reproductive transition semantics

**Modify**
- `teacher_body_dynamics.py`
- `tests/test_teacher_body_dynamics.py`

RED tests:
- `MAINTENANCE_TO_EMISSION` must not include `GONADAL_ENDOCRINE_REFERENCE`;
- emission executable channels = `EMISSION_REFLEX_STATE` and `BLADDER_NECK_EJACULATORY_CLOSURE_STATE`;
- `EMISSION_TO_EJACULATORY_REFLEX` executable channels = `EJACULATORY_REFLEX_STATE` and `EXPULSION_MOTOR_PATTERN_STATE`;
- add `REPRODUCTIVE_EVENT_TO_BASELINE_RECOVERY` for the four zero-baseline event channels;
- transition IDs remain unique and all channels exist.

Keep legacy detumescence transitions unless they conflict, but do not use them as the new generic event recovery path.

Commit:
`fix(embodiment): correct Teacher reproductive transition semantics`

## Task 3 — Explicit reproductive event gates

**Modify**
- `teacher_high_salience_coupling.py`
- `teacher_transition_executor.py`

**Tests**
- `tests/test_teacher_transition_executor.py`
- `tests/test_teacher_high_salience_coupling.py`

Add:
- `TeacherReproductiveEventGate`
- allowed:
  - `NONE`
  - `EMISSION_REFERENCE_REQUEST`
  - `EXPULSION_REFERENCE_REQUEST`
  - `RECOVERY_REFERENCE_REQUEST`

Extend:
`select_teacher_transition_intent(..., reproductive_event_gate=None)`

Required behavior:
- high activation alone never selects emission;
- emission request requires vascular/maintenance readiness and selects `MAINTENANCE_TO_EMISSION`;
- expulsion request requires emission-state readiness and selects `EMISSION_TO_EJACULATORY_REFLEX`;
- recovery request after event activity may select both:
  - `VASCULAR_RESPONSE_TO_BASELINE_RECOVERY`
  - `REPRODUCTIVE_EVENT_TO_BASELINE_RECOVERY`
- event gate does not alter functional motivation;
- event gate does not imply consent, orgasm, pleasure, or action authority.

Commit:
`feat(embodiment): add explicit Teacher reproductive event gates`

## Task 4 — Runtime event-gate integration

**Modify**
- `teacher_state_loop.py`
- `tests/test_teacher_state_loop.py`

Extend:
`advance_teacher_embodied_tick(..., reproductive_event_gate=None)`

Pass the gate only to transition selection.

RED integration tests:
- same controller/body state with `NONE` vs `EMISSION_REFERENCE_REQUEST` produces different transition intent only when readiness condition holds;
- event gate does not change controller functional motivation;
- emission -> expulsion -> recovery path advances monotonically in sequence/time;
- event-specific channels recover toward baseline;
- ejaculation reference never creates orgasm/phenomenal state;
- stale body/runtime/session checks remain unchanged.

Commit:
`feat(embodiment): integrate Teacher reproductive event runtime path`

## Task 5 — Regression and public surface

**Modify if needed**
- `__init__.py`
- `tests/test_teacher_embodiment_probe.py`

Export:
- `TeacherHighSalienceCouplingRule`
- `TeacherHighSalienceCouplingProfile`
- `TeacherReproductiveEventGate`
- `build_teacher_high_salience_coupling_profile`
- `validate_teacher_high_salience_coupling_profile`

Regression:
- original ten deterministic stability scenarios still PASS with no event gate;
- zero-motivation scenario remains zero motivation;
- cardiorespiratory channels are not hard-forced by high-salience activation;
- endocrine channels are not automatically driven;
- package exports import successfully.

Commit:
`test(embodiment): verify Teacher multi-system coupling regression`

## Task 6 — Exact-head reverse review and Draft PR

Reverse-review exact head:
- no `REST_TO_EXERTION` reuse for high-salience path;
- no hardcoded cardiovascular/respiratory sexual coefficients;
- no automatic gonadal endocrine increase;
- no generic pituitary-as-prolactin mapping;
- no automatic arousal -> emission/ejaculation;
- event gate remains separate from motivation/consent;
- no cross-role normalization;
- predecessor Controller ↔ Body feedback remains intact.

Run repository CI through Draft PR.

Expected:
- Quality PASS;
- CodeQL PASS;
- Python 3.11/3.12 PASS;
- mypy 3.11/3.12 PASS;
- controls/evidence/IQC PASS;
- Main Transition Authority Gate fail-closed without fresh exact-head merge approval.

Close Draft unmerged.

Final:
`MERGE_TO_MAIN = NO`
`DEPLOYMENT = FALSE`
`CANONICAL_EFFECT = NONE`
