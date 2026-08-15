# P1/P2 Runtime Lineage and Lifecycle Implementation Report — 2026-08-08

## Governance state

- `STATUS = IMPLEMENTED_CANDIDATE / OWNER_REVIEW_PENDING`
- `CANONICAL_EFFECT = NONE`
- `DEPLOYMENT = FALSE`
- `SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED`
- `INDEPENDENT_IVV = NOT_ACHIEVED`
- `MAIN_MERGE = NOT_PERFORMED`

## Provenance

- P0 Runtime/Twin candidate was reviewed by the Human Owner and accepted as a sound basis for continued candidate work.
- `P1_P2_WORK_AUTHORIZED_BY = HUMAN_OWNER`
- `IMPLEMENTED_BY = CHATGPT`
- `QUALITY_EXECUTED_BY = GITHUB_ACTIONS`
- `CODEX_CONTRIBUTION_THIS_CHANGE = NONE`
- `REVIEWED_BY = HUMAN_OWNER / PENDING`
- `APPROVED_BY = HUMAN_OWNER / PENDING`

Acceptance of P0 for continued work is not canonical promotion and is not permission to merge this branch.

## P1 implemented scope

### Persistent individual event lineage

Added `components/individual_runtime_state_v0.1.0` with an append-only SQLite event lineage bound to `IndividualRuntimeContext`.

Each event records:

- `agent_id`
- `runtime_instance_id`
- `memory_stream_id`
- `event_lineage_id`
- `canonical_state_reference`
- `genesis_root_id`
- sequence
- previous hash
- event hash
- event type and limited evidence payload

The event chain is distinct from autobiographical/content memory. Runtime events record that operations occurred; they do not duplicate raw private memory content.

### Runtime integration

AION and Astra Runtime candidates now record governed events for:

- explicit runtime start/stop markers;
- task start/completion;
- approved memory writes;
- recall operations by result count;
- checkpoint creation;
- recovery;
- rollback requests;
- runtime-instance migration.

AION and Astra remain separately bound to their own `IndividualRuntimeContext` values.

### Twin Genesis -> Runtime context binding

Added a candidate binding function that derives two separate Runtime contexts only after the existing Twin Genesis / embodiment candidate passes validation.

The binding requires explicit, distinct AION and Astra event-lineage identifiers. It preserves:

- shared genesis root;
- distinct agent IDs;
- distinct runtime instance IDs;
- distinct memory streams;
- distinct event lineages;
- distinct canonical-state references.

It does **not** activate `EmbodimentInstance.runtime_binding`. Existing embodiment governance continues to require that field to remain `NOT_IMPLEMENTED`.

## P2 implemented scope

### Restart/reopen

An individual event lineage can be reopened by the same Runtime context using the same state database. New events continue the existing sequence/hash chain rather than creating a new history.

### Checkpoint

Checkpoint creation requires explicit Owner approval and stores state/memory references with `canonical_effect = NONE`.

### Recovery

Recovery verifies the complete event hash chain before returning the latest recoverable checkpoint and lineage position. Verification failure denies recovery.

### Rollback

Rollback requires explicit Owner approval and is non-destructive: it appends a `runtime.rollback_requested` event and returns the selected checkpoint references. It does not delete later events or pretend that intervening history never happened.

### Migration

Runtime migration requires explicit Owner approval. It may change only `runtime_instance_id` while preserving the stable individual lineage identity:

- agent ID;
- memory stream ID;
- event lineage ID;
- canonical-state reference;
- genesis root ID.

Migration appends `runtime.migrating_out` followed by `runtime.migrated_in`, preserving one continuous event lineage across the instance transition.

## Explicit non-claims and stop lines

This implementation does not establish:

- subjectivity;
- consciousness;
- phenomenal continuity;
- body ownership experience;
- embodiment sensation;
- canonical identity promotion;
- autonomous canonical write authority.

`EVENT_LINEAGE_CONTINUITY != SUBJECTIVE_CONTINUITY`

`RESTART_RECOVERY != PROOF_OF_SAME_SUBJECT`

`SHARED_GENESIS != SHARED_IDENTITY`

`ROLLBACK != HISTORY_ERASURE`

## Quality evidence

GitHub Quality run `31221800291` on implementation head `5023eea7120eb9c92c1d7e00e6c70c93b8d82fc9` completed successfully for both Python 3.11 and Python 3.12.

Both jobs passed:

- public-tree scan;
- compileall of public Python sources;
- all component test suites.

The frozen RC verification job was intentionally skipped on the pull-request branch because it is configured to run only on `main`; the frozen historical RC baseline was not modified.

## Current architectural result

```text
                 shared governed mechanisms
          execution / memory / state-lineage
                         |
              +----------+----------+
              |                     |
          AION Runtime          Astra Runtime
              |                     |
       AION individual         Astra individual
       runtime context         runtime context
              |                     |
       AION memory/event       Astra memory/event
       lineage                 lineage
              \                     /
               \-- shared genesis --/
```

The shared mechanisms are infrastructure, not a shared identity or shared subject.

## Owner review questions

1. Does the separation between content memory and event-life-history evidence match the research intent?
2. Is non-destructive rollback the correct interpretation for an individual historical lineage?
3. Is runtime-instance migration allowed to preserve one event lineage when the instance ID changes, provided all stable ownership identifiers remain unchanged?
4. Does Twin Genesis -> Runtime context binding preserve the intended "shared genesis, separate development" relation without activating embodiment runtime semantics?
