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
