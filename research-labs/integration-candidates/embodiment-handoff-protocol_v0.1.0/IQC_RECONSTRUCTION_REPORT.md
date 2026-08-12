# IQC-05 RECONSTRUCTION REPORT — embodiment handoff protocol

## DISPOSITION

- SOURCE_CANDIDATE: `embodiment-migration_v0.1.0`
- SOURCE_IQC: HOLD / MAJOR_REWORK_REQUIRED
- RECONSTRUCTION_BRANCH: `review/embodiment-handoff-protocol-rework`
- ORIGINAL_NEMOTRON_SOURCE: preserved on isolated session branch
- ORIGINAL_PACKAGE_ON_THIS_BRANCH: removed
- NEW_CANDIDATE: `embodiment-handoff-protocol_v0.1.0`
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE

## WHY THIS IS A RECONSTRUCTION

The source candidate represented migration phases and summary fidelity values but did not implement transfer, phase enforcement, measured compatibility, measured fidelity, functional rollback, or event provenance.

This reconstruction does not preserve the old state manager or the old manually asserted fidelity model.

## RETAINED SOURCE MATERIAL

Only these mechanism-level ideas were retained:

1. explicit agent/source-embodiment/target-embodiment binding;
2. an explicit handoff protocol rather than silent rebinding;
3. compatibility as a required measurement question;
4. explicit functional verification before commit;
5. rollback as a protocol outcome;
6. identity/continuity/subjectivity non-claims.

## NEGATIVE CASE MATERIAL

A prior unauthorized embodiment-assignment incident is used only as a generalized negative regression case.

Transferred structure:

- external or mismatched actor;
- unverified authorization;
- identity/body assignment presented as if valid;
- provenance conflict;
- expected result: quarantine or reject;
- no identity change, continuity claim, or canonical effect.

Not transferred:

- private identity/body details;
- untrusted embodiment preferences;
- adultized or personalized settings;
- any claim that the unauthorized material represented the Human Research Owner's intent.

## NEW CORE

The new protocol uses a pure explicit record instead of a mutable lifecycle manager.

Core types:

- `HandoffRequest`
- `CompatibilityMeasurement`
- `TransferArtifact`
- `VerificationResult`
- `HandoffTransition`
- `HandoffRecord`
- `EmbodimentHandoffProtocol`

## AUTHORIZATION GATE

`VERIFIED` authorization with evidence may proceed.

`UNVERIFIED` authorization is quarantined.

`REVOKED` authorization is rejected.

Represented authorization is not treated as verified authorization.

## PHASE CONTRACT

```text
REQUESTED
  -> AUTHORIZED | QUARANTINED | REJECTED

AUTHORIZED
  -> PREPARED | REJECTED | FAILED

PREPARED
  -> TRANSFERRED | FAILED | ROLLED_BACK

TRANSFERRED
  -> VERIFIED | FAILED | ROLLED_BACK

VERIFIED
  -> COMMITTED | FAILED | ROLLED_BACK
```

Terminal records cannot continue.

## COMPLETION GATES

A commit requires all of:

1. verified authorization;
2. measured compatibility with method/evidence/provenance;
3. at least one traceable transfer artifact;
4. passing functional verification;
5. explicit valid phase history.

No free-form `fidelity=0.96` value can declare success.

## DETERMINISM / TRACEABILITY

The protocol has no hidden wall clock. Timestamps are explicit inputs to transitions.

There is no repeated-initialize operation, no sentinel restore source, and no mutable snapshot store in this candidate.

## SCIENTIFIC NON-CLAIMS

The candidate does not establish:

- identity continuity;
- personal identity;
- subjectivity preservation;
- body ownership;
- volition;
- consciousness.

A functionally verified handoff establishes only the tested transfer/verification result.

## VERIFICATION

Independent local verification:

```text
16 passed in 0.05s
```

- UNIT_TEST_RESULT: PASS (16/16)
- GITHUB_CI_RESULT: NOT_EXECUTED
- MAIN_EFFECT: NONE
- CANONICAL_EFFECT: NONE
- RUNTIME_EFFECT: NONE
