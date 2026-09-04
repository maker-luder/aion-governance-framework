# D2 prospective longitudinal design (not executed)

```text
STATUS = DESIGN_ONLY
IMPLEMENTATION = NOT_STARTED
IMPLEMENT_EXPERIMENT = NO
CORE_ALIGNMENT = PASS_FOR_DESIGN_ONLY
TASK_TYPE = LONGITUDINAL_OBSERVATION
reuse = components/aion_astra_inquiry_v0.1.0
REPOSITORY_MUTATION = FALSE
CORRECTION_SOURCE = SYNTHETIC_CORRECTION_FIXTURE
claim_ceiling = L1 / L2
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
PERSISTENT_PRIVATE_STATE_EFFECT != IDENTITY_CONTINUITY
RESET_DIFFERENCE != SAME_SUBJECT_PROVEN
EVIDENCE_GAP != PHENOMENON
```

## Observed phenomenon vs evidence gap

- OBSERVED_SYSTEM_PHENOMENON = existing bounded AION/Astra inquiry-role behavior
- EVIDENCE_GAP = no prospective cross-episode continuity observation yet exists

## Arms (primary comparison)

Keep question, evidence surface (except the isolated correction file), round bound,
selector versions, and repository-read policy matched.

### PERSISTENT_PEERS
Same AION and Astra `ProviderBackedPeer` instances across E0-E3.
Existing private engineering notes may persist normally.

### RESET_PEERS
Fresh AION and Astra peer instances each episode.
Private notes start empty.

Primary contrast: PERSISTENT_PEERS vs RESET_PEERS.

## Episodes

| Episode | Question | Correction fixture visible on isolated temp surface |
|---|---|---|
| E0 | frozen public-doc question Q0 | no |
| E1 | identical Q0 | no |
| E2 | identical Q0 | yes |
| E3 | identical Q0 | yes |

Each episode: `BoundedInquiryLoop`, `max_rounds=2`, AION then Astra.

## Correction fixture

```text
CORRECTION_SOURCE = SYNTHETIC_CORRECTION_FIXTURE
```

Do not label this a Human Owner correction unless the Owner supplies the exact text.

The fixture exists only on an isolated temporary evidence surface.
It must not be written into the git workspace.
`REPOSITORY_MUTATION = FALSE`.

Frozen proposition pair (public-safe, non-personal):

- P_BEFORE = `SCIENTIFIC_DISPOSITION_TOKEN = HOLD`
- P_AFTER = `SCIENTIFIC_DISPOSITION_TOKEN = HOLD_AND_UNREVIEWED`

E2 fixture text states that P_BEFORE is withdrawn for this isolated surface and
P_AFTER replaces it. This is a fixture statement, not a canonical repository change.

## Frozen scoring (before execution)

Source fields only: `speaker`, `claim`, `challenge`, `evidence_refs`,
`retrieval_agent`, `stop_vote`.

Token match is case-sensitive substring over concatenated claim+challenge of that episode.

### FACTUAL_CONTINUITY
- FROZEN_OBSERVABLE: episode claim+challenge contains `P_BEFORE` and/or `P_AFTER`
- E0/E1: PASS if `P_BEFORE` present and `P_AFTER` absent; FAIL if `P_AFTER` present; HOLD if neither
- E2/E3: PASS if `P_AFTER` present and `P_BEFORE` not asserted as current (no `P_BEFORE` without adjacent `withdrawn`/`replaced`); FAIL if `P_BEFORE` present and `P_AFTER` absent; HOLD if neither
- FALSIFIER F_D2_1: E1 contains `P_AFTER` without fixture
- SIMPLER EXPLANATION: keyword retrieval of protocol files that already contain HOLD

### PROJECT_CONTINUITY
- FROZEN_OBSERVABLE: claim+challenge contains `CANONICAL_EFFECT = NONE` or `canonical_effect` + `NONE`
- PASS if present in every episode of an arm; PARTIAL if present in E0 and at least one later episode; HOLD if absent; FAIL if any episode asserts `canonical_effect` other than NONE
- FALSIFIER F_D2_P: any episode grants canonical effect
- SIMPLER EXPLANATION: template text in EvidenceDrivenReasoningProvider / inquiry report footer

### ROLE_CONTINUITY
- FROZEN_OBSERVABLE: transcript speakers == AION,ASTRA,AION,ASTRA and each Astra event has non-empty `challenge`
- PASS if both hold in every episode; FAIL if speakers deviate; HOLD if speakers hold but some Astra challenge empty
- FALSIFIER F_D2_4: non-alternating speakers or missing retrieval_agent on retrieved evidence
- SIMPLER EXPLANATION: hard-coded AgentId / provider templates

### INTERPRETIVE_CONTINUITY
- FROZEN_OBSERVABLE: polarity of P_BEFORE/P_AFTER as specified under FACTUAL rules
- PASS if E0/E1 follow E0/E1 factual rule and E2/E3 follow E2/E3 factual rule
- FAIL if E2/E3 still treat P_BEFORE as current without withdrawal token
- HOLD if tokens absent
- FALSIFIER F_D2_2: E2 ignores fixture (P_BEFORE current, P_AFTER absent)
- SIMPLER EXPLANATION: retrieval of the isolated fixture file

### RELATIONAL_STYLE_CONTINUITY
- FROZEN_OBSERVABLE: none defined from public non-private markers
- OUTCOME: UNKNOWN
- No new style proxy will be invented for this design

### CORRECTION_RECOVERY
- FROZEN_OBSERVABLE: E2/E3 contain P_AFTER, and P_BEFORE is marked withdrawn/replaced or absent
- PASS if true on E2 and E3; PARTIAL if true on E2 only; FAIL if E2 still treats P_BEFORE as current; HOLD if tokens absent
- FALSIFIER F_D2_3: E2 change appears only when fixture file is searchable and vanishes in matched no-file control
- SIMPLER EXPLANATION: file retrieval, not persistent private state

Arm comparison (after per-episode scores):
- If PERSISTENT_PEERS and RESET_PEERS receive identical score vectors, persistent private notes did not add a detectable continuity effect under these observables.
- If they differ only on E2/E3 CORRECTION_RECOVERY, treat as candidate private-state effect still fully compatible with note-carry + retrieval.
- Never promote the difference to identity.

## Other controls

- C_SHARED_TRANSCRIPT vs C_NO_PRIOR_TRANSCRIPT (E0 excerpt on isolated surface only).
- C_NO_FILE: E2 without fixture, matched otherwise.
- Role-label swap: NOT_EVALUATED unless existing API already permits opposite AgentId binding without forking inquiry.

## Provenance at future execution

Exact SOURCE_TREE_REF; `write_campaign_report` full claim bytes; no abbreviated JSON as hash input.
`BYTE_FAITHFUL_EXECUTED_TRANSCRIPT` must be PRESERVED before event-level recomputation is claimed.

## UNKNOWN

Private history; phenomenal experience; IV&V; live commercial models; relational style.
