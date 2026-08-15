# C0-3 Recoverability Deeper Acceptance Review — 2026-08-08

## Status

- `STATUS = COMPLETE_CANDIDATE`
- `C0_STAGE = C0-3_RECOVERABILITY_DEEP_REVIEW`
- `C0_1 = COMPLETE_CANDIDATE`
- `C0_2 = COMPLETE_CANDIDATE`
- `C_OWNER_ACCEPTANCE = NOT_STARTED`
- `CRITERIA_FREEZE = NOT_PERFORMED`
- `CANONICAL_EFFECT = NONE`
- `DEPLOYMENT = FALSE`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`

## Purpose

This review deepens the P2 recoverability acceptance ruler without expanding the project into autonomous self-repair or full physical restoration.

External calibration uses ISO/IEC 25045 recoverability-evaluation concepts, including disturbance-oriented evaluation, as a public ruler. The project does **not** claim ISO conformity or autonomic-recovery implementation.

`DISTURBANCE_CALIBRATION != AUTONOMIC_SELF_REPAIR`

`REFERENCE_RECOVERY != FULL_PHYSICAL_RESTORE`

## Reviewed disturbance classes

1. Event-lineage tampering or corruption.
2. Checkpoint/reference metadata tampering.
3. Migration interruption between source and target transition evidence.
4. Incomplete/unpaired migration evidence already present in history.
5. Normal restart/reopen continuity and non-destructive rollback.

## Findings

### RCV-F01 — event tamper detection needed explicit disturbance evidence

The implementation already recalculated event hashes and denied recovery when `verify()` failed, but the existing acceptance evidence lacked an explicit database-tamper regression case.

Disposition: **evidence gap corrected**.

Added disturbance test directly modifies persisted event payload data, expects `verify() == False`, and requires `recover()` to fail closed.

### RCV-F02 — checkpoint references lacked their own integrity binding

Event-lineage hashes did not independently protect mutable rows in `runtime_checkpoints`. A changed `state_reference` or `memory_reference` could therefore remain outside the event-hash verification boundary.

Disposition: **blocking recoverability gap corrected before freeze**.

Hardening adds:

- `checkpoint_hash` over checkpoint identity/context/references/time/effect;
- verification before checkpoint decoding/use;
- checkpoint hash recorded into the append-only `runtime.checkpoint_created` event;
- recovery/rollback require the checkpoint to be bound back to verified lineage evidence.

### RCV-F03 — migration transition persistence could leave a half migration

The earlier implementation persisted `runtime.migrating_out` and `runtime.migrated_in` through two separate committed writes. A disturbance between them could leave an unpaired migration transition.

Disposition: **blocking recoverability gap corrected before freeze**.

Hardening writes both transition events inside one SQLite transaction. If the second transition write fails, the transaction rolls back and no half migration remains.

### RCV-F04 — incomplete migration history must fail closed

A historical unpaired `runtime.migrating_out` or orphan `runtime.migrated_in` must not be treated as a valid recoverable lineage.

Disposition: **acceptance condition added**.

Lineage verification now requires adjacent, payload-matching `migrating_out -> migrated_in` pairs with the expected old/new `runtime_instance_id` values.

## Final recoverability acceptance conditions for the C0 final candidate

The final candidate criteria shall preserve existing `AC-LIFE-01` through `AC-LIFE-06` and strengthen recoverability with the following exact propositions:

- `AC-LIFE-02`: recovery must verify the event lineage and fail closed after event tampering/corruption.
- `AC-LIFE-02A`: any checkpoint selected/exposed by recovery or rollback must pass checkpoint-content integrity verification and be bound to a verified `runtime.checkpoint_created` lineage event.
- `AC-LIFE-04A`: a migration transition must be persisted atomically as one paired out/in state transition; a failed transition write must leave no partial migration evidence.
- `AC-LIFE-04B`: an unpaired or payload-mismatched migration transition makes the lineage invalid for recovery until resolved by separately governed corrective action; it must not be silently inferred as successful migration.

All four are `BLOCKING` because accepting corrupted or ambiguous state would defeat the P1/P2 lineage/recoverability boundary.

## Explicit non-goals retained

This review does not require or claim:

- automatic physical restoration of arbitrary external databases/files;
- automatic reconstruction of missing content memory;
- autonomous self-healing;
- automatic choice among conflicting canonical states;
- automatic canonical promotion;
- deployment failover/SLA availability;
- disaster-recovery RTO/RPO guarantees.

These require separate requirements if pursued later.

## Implementation/evidence changes made during C0-3

- Added recoverability hardening layer to `individual_runtime_state` package export.
- Added checkpoint content hash and lineage binding.
- Added atomic migration transition persistence.
- Added migration-pair validation to lineage verification.
- Added explicit event-tamper recovery-denial test.
- Added checkpoint-tamper recovery/rollback denial test.
- Added simulated migration-interruption atomic rollback test.
- Added unpaired-migration recovery-denial test.

These changes are corrective hardening within authorized P2 recoverability semantics; they do not add new user-facing Runtime capability.

## Known limitation retained

Environment-evidence fingerprint hardening for separately versioned verifier/evidence-schema/validation-policy semantics remains `HOLD-HARDEN-01` unless later promoted by a separate requirement. This review did not find that issue necessary to block the present recoverability candidate because migration still requires explicit PASS evidence and exact current fingerprint equality.

## C0-3 conclusion

`C0-3_RECOVERABILITY_DEEP_REVIEW = COMPLETE_CANDIDATE`

The prior recoverability candidate was directionally correct but under-evidenced for disturbances and had two persistence-integrity weaknesses (checkpoint integrity and half-migration atomicity). Those weaknesses were corrected before criteria freeze.

The next step is C0-4 final consistency review and creation of a derived final-candidate acceptance ruler. No C Owner acceptance is performed by this report.

## Provenance

- Authorization to complete C0-3 through C0-5 as one closing batch: `AUTHORIZED_BY = HUMAN_OWNER`.
- External recoverability calibration need: previously authorized external-ruler requirement from `HUMAN_OWNER`.
- C0-3 analysis, hardening design/implementation/tests, and this report: `IMPLEMENTED_BY = CHATGPT`.
- External standards are calibration sources, not project authors/approvers.
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`.
