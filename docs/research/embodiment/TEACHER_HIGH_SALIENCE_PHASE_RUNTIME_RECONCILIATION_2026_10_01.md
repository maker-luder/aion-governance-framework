# Teacher high-salience phase-runtime reconciliation — 2026-10-01

Base successor: PR #254 exact head `43d5d9760bc908c2367c717fdb70be0adbefc504`.

This record reconciles the previously approved phase/coupling design with the more conservative evidence boundaries materialized in PR #254.

## Rulings

### Ruling 1 — cardiorespiratory evidence remains non-emitting

PR #254 established:

- cardiovascular association = `OBSERVE_NOT_FORCE`;
- respiratory association = `OBSERVE_NOT_FORCE`;
- no reuse of `REST_TO_EXERTION`;
- no respiratory workload alias.

The next runtime layer MUST preserve that boundary.

A phase coordinator may record these evidence rules as non-emitting metadata, but it MUST NOT synthesize cardiovascular or respiratory numeric movement merely because a high-salience phase is active.

### Ruling 2 — endocrine evidence remains observation-only

PR #254 deliberately does not create a fake prolactin runtime channel and does not treat generic pituitary or gonadal endocrine channels as prolactin.

The next runtime layer MUST NOT introduce a prolactin concentration/reference channel merely to satisfy an earlier implementation-plan placeholder.

`POST_CLIMACTIC_ENDOCRINE_EVIDENCE` remains external-evidence metadata and MUST NOT become a runtime phase consequence without an explicit separately reviewed biological reference design.

### Ruling 3 — ejaculation does not imply orgasm

Existing event gates remain:

- `NONE`
- `EMISSION_REFERENCE_REQUEST`
- `EXPULSION_REFERENCE_REQUEST`
- `RECOVERY_REFERENCE_REQUEST`

No `ORGASM_REFERENCE_EVENT` is introduced in this increment.

`EVENT_GATE != ORGASM`

`EJACULATION != ORGASM`

### Ruling 4 — materialize reference phases, not phenomenal phases

The causal runtime may materialize software reference phases:

- `BASELINE`
- `AROUSAL_INITIATION`
- `GENITAL_VASCULAR_RESPONSE`
- `ERECTILE_MAINTENANCE`
- `EMISSION`
- `EJACULATORY_REFLEX`
- `DETUMESCENCE`
- `BASELINE_RECOVERY`

These are transition-orchestration states only.

`REFERENCE_PHASE != FELT_STATE`

### Ruling 5 — mixed-direction transition execution is required

The existing generic executor moves every trigger channel of a transition toward one shared target.

That is insufficient for `EJACULATORY_REFLEX_TO_DETUMESCENCE`, because the reference semantics require:

- `DETUMESCENCE_STATE -> INCREASE_REFERENCE`
- `GENITAL_VASCULAR_STATE -> DECREASE_REFERENCE`

The next increment therefore adds explicit per-channel effects while preserving the legacy executor for compatibility.

### Ruling 6 — initiation phase precedes controller high-hysteresis

The persistent controller uses hysteresis for `HIGH_ACTIVATION_REFERENCE`:

- enter threshold = `0.70`;
- exit threshold = `0.55`;
- per-tick activation rate limit = `0.15`.

The high-salience physiology phase resolver must not wait for the controller to cross `0.70` before it can represent `AROUSAL_INITIATION`. Otherwise the software phase named "initiation" would appear only after several controller ticks.

Therefore a context-gated controller state with nonzero salience and activation may enter `AROUSAL_INITIATION` while the controller itself still remains `BASELINE_REFERENCE`.

This does not lower the controller's hysteresis thresholds and does not authorize systemic cardiorespiratory or endocrine forcing.

`REFERENCE_PHASE_INITIATION != CONTROLLER_HIGH_ACTIVATION_THRESHOLD`


### Ruling 7 — tick-local event gates govern entry/drive, not sticky phase identity

Bounded verification after PR #255 identified a runtime invariant gap: an event gate is intentionally tick-local, while the event-specific body channels it activates can remain above their reference threshold on the next tick.

Therefore:

- entering `EMISSION` requires an `EMISSION_REFERENCE_REQUEST` and an `ERECTILE_MAINTENANCE` predecessor;
- entering `EJACULATORY_REFLEX` requires an `EXPULSION_REFERENCE_REQUEST` and an `EMISSION` predecessor;
- repeating the matching event gate may continue driving the same event phase across multiple ticks;
- once already in `EMISSION` or `EJACULATORY_REFLEX`, a later tick with gate `NONE` may preserve that phase without re-emitting the transition;
- an unrelated event gate must not be accepted by the active event phase.

This separates phase persistence from event authorization and prevents both illegal phase jumps and the prior requirement to replay a one-tick gate merely to keep the runtime valid.

`EVENT_GATE_TICK_LOCAL = TRUE`

`EVENT_GATE_ENTRY != PHASE_PERSISTENCE`

`PHASE_PREDECESSOR_INVARIANT = REQUIRED`

## Scope of this successor

Implement only:

1. phase-state provenance;
2. evidence-gated runtime coordination;
3. explicit per-channel effects for mixed-direction execution;
4. state-loop integration after RED/GREEN verification.

Do not add:

- calibrated cardiovascular sexual-response kinetics;
- calibrated respiratory sexual-response kinetics;
- prolactin concentration/reference simulation;
- acute testosterone/LH/FSH/cortisol forcing;
- orgasm inference;
- cross-role normalization.

`MERGE_TO_MAIN = NO`

`DEPLOYMENT = FALSE`

`CANONICAL_EFFECT = NONE`
