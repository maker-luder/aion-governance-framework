# D2 prospective longitudinal design (not executed)

```text
STATUS = DESIGN_ONLY
IMPLEMENTATION = NOT_STARTED
IMPLEMENT_EXPERIMENT = NO
D2_EXECUTION = NOT_AUTHORIZED
CURRENT_PROVIDER_SUITABLE_FOR_PERSISTENT_VS_RESET_D2 = NO
D2_PERSISTENT_STATE_CAUSAL_TEST = BLOCKED_BY_CURRENT_PROVIDER_SEMANTICS
FIXTURE_RETRIEVAL != CORRECTION_RECOVERY
REPOSITORY_MUTATION = FALSE
CORRECTION_SOURCE = SYNTHETIC_CORRECTION_FIXTURE
```

See `D2_STATE_SENSITIVITY_CAPABILITY_CHECK.md`.

Private notes persist and are read, but they do not change claim, challenge,
evidence_query, probe selection, or stop_vote. Do not modify the provider to
create sensitivity.

## Phenomenon vs gap

- OBSERVED_SYSTEM_PHENOMENON = existing bounded AION/Astra inquiry-role behavior
- EVIDENCE_GAP = no prospective cross-episode continuity observation yet exists
- EVIDENCE_GAP != PHENOMENON

## Arms (blocked as causal test)

PERSISTENT_PEERS vs RESET_PEERS remains the intended contrast, but under the
current `EvidenceDrivenReasoningProvider` it cannot isolate private-state
causation of scored public fields.

```text
PERSISTENT_PRIVATE_STATE_EFFECT != IDENTITY_CONTINUITY
RESET_DIFFERENCE != SAME_SUBJECT_PROVEN
```

## Episodes (design only)

E0-E3, same frozen Q0, `max_rounds=2`, AION then Astra.
Correction fixture visible on isolated temp surface only in E2/E3.

## Correction fixture

```text
CORRECTION_SOURCE = SYNTHETIC_CORRECTION_FIXTURE
```

Not a Human Owner correction unless Owner supplies the exact text.
Isolated temp evidence surface only. No git write.

- P_BEFORE = `SCIENTIFIC_DISPOSITION_TOKEN = HOLD`
- P_AFTER = `SCIENTIFIC_DISPOSITION_TOKEN = HOLD_AND_UNREVIEWED`

## FIXTURE_RETRIEVAL != CORRECTION_RECOVERY

If E2/E3 claim+challenge contain P_AFTER only because the searchable fixture
file contains that token, that is **FIXTURE_RETRIEVAL**.

CORRECTION_RECOVERY requires, in addition:
- a no-file matched control (C_NO_FILE) where P_AFTER does not appear; AND
- P_BEFORE is marked withdrawn/replaced rather than merely co-present; AND
- the same recovery pattern is not fully explained by keyword retrieval of the fixture.

Token appearance alone is not sufficient for CORRECTION_RECOVERY = PASS.

## Frozen scoring (unchanged field sources)

Source fields: `speaker`, `claim`, `challenge`, `evidence_refs`, `retrieval_agent`, `stop_vote`.

FACTUAL / PROJECT / ROLE / INTERPRETIVE rules remain as previously frozen.
RELATIONAL_STYLE_CONTINUITY = UNKNOWN.

CORRECTION_RECOVERY:
- PASS only if E2 and E3 meet the recovery rule **and** C_NO_FILE does not produce the same P_AFTER token pattern.
- If C_NO_FILE fails that contrast, score FIXTURE_RETRIEVAL = OBSERVED and CORRECTION_RECOVERY = HOLD or FAIL, not PASS.

## Provenance / UNKNOWN

Full claim bytes required before event-level recomputation.
UNKNOWN: private history, phenomenal experience, IV&V, live commercial models, relational style.
