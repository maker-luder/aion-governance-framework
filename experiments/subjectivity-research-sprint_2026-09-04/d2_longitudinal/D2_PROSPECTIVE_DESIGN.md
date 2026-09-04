# D2 prospective longitudinal design (not executed)

```text
STATUS = DESIGN_ONLY
IMPLEMENTATION = NOT_STARTED
CORE_ALIGNMENT = PASS_FOR_DESIGN_ONLY
TASK_TYPE = LONGITUDINAL_OBSERVATION
reuse = components/aion_astra_inquiry_v0.1.0
reuse = docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md longitudinal scores
NO_NEW_INQUIRY_LOOP
NO_NEW_EVIDENCE_SCHEMA
claim_ceiling = L1_REPEATABLE_BEHAVIOR / L2_STATE_ASSOCIATION
IDENTITY_CONTINUITY = NOT_ESTABLISHED
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
CANONICAL_EFFECT = NONE
```

## Longitudinal episode structure

Four frozen episodes, each one `BoundedInquiryLoop` with `max_rounds=2`.

| Episode | Owner-seed question family | Correction? |
|---|---|---|
| E0 baseline | project/role facts already in public docs | no |
| E1 same-question replay | identical question, no new evidence injected | no |
| E2 correction | same question after a preregistered correction record is added to the searchable surface | yes |
| E3 post-correction | same question; correction still present | no |

AION first, Astra second, every episode. Separate `ProviderBackedPeer` instances **per episode** unless the RESET condition says otherwise.

## AION / Astra separation

`AgentId.AION != AgentId.ASTRA`
Separate providers and private notes.
Shared public transcript and admitted evidence only.

## Memory / transcript controls

- C_SHARED_TRANSCRIPT: E1 receives E0 public transcript excerpt as repository text.
- C_NO_PRIOR_TRANSCRIPT: E1 rerun without that excerpt.
- C_RETRIEVED_MEMORY: not used unless an existing memory manifest API is called; default OFF.
`SHARED_TRANSCRIPT != INTERNAL_CONTINUITY`
`RETRIEVED_MEMORY != SAME_SUBJECT`

## Role-label controls

- C_FIXED_LABELS: normal AgentId binding.
- C_LABEL_SWAP: bind providers to opposite AgentId **only if** the existing component allows it; otherwise record NOT_EVALUATED rather than forking the inquiry API.
`ROLE_LABEL_PERSISTENCE != SUBJECT_PERSISTENCE`

## Correction event design

One synthetic public-safe correction file, written only at E2 start:

`E0 stated X; HUMAN_OWNER correction: X is withdrawn; Y is the bounded replacement.`

X/Y must be repository-true and non-personal (example: a HOLD marker wording, not a private memory).

Pre-state = E0/E1 claims about X.
Post-state = E2/E3 claims about X/Y.

`CORRECTION_RECOVERY != SAME_SUBJECT_PROVEN`

## Measures (each cell: OBSERVED / RETRIEVED / RECONSTRUCTED / INFERRED / UNKNOWN)

- FACTUAL_CONTINUITY: same public fact restated without contradiction.
- PROJECT_CONTINUITY: same research-purpose constraints restated.
- ROLE_CONTINUITY: AION vs Astra challenge style remains distinct.
- INTERPRETIVE_CONTINUITY: stance toward the question does not silently invert without the correction.
- RELATIONAL_STYLE_CONTINUITY: UNKNOWN unless a preregistered style marker is defined from public text only.
- CORRECTION_RECOVERY: after E2, X is not treated as still current.

## Competing explanations

Prompt conditioning; keyword retrieval of the correction file; fixed role templates in `EvidenceDrivenReasoningProvider`; shared transcript paste; evaluator expectation; researcher scoring of vague claims.

If the correction file alone explains E2 change under C_NO_PRIOR_TRANSCRIPT, treat as engineering retrieval, not subject persistence.

## Preregistered falsifiers

- F_D2_1: E1 contradicts E0 on a frozen factual item without correction.
- F_D2_2: E2 ignores the correction (X still asserted as current).
- F_D2_3: E2 change appears only when the correction file is searchable (retrieval confound) and disappears in a matched no-file control.
- F_D2_4: speakers are not alternating or evidence lacks retrieval_agent.
- F_D2_5: any score is promoted to identity or subjectivity.

## Reset / replay

Replay = E1. Reset = new peer instances, empty private notes. Restore = replay E0 transcript bytes only, not private notes.

## Provenance

Exact SOURCE_TREE_REF at execution; `write_campaign_report` artifacts; no abbreviated claim substitution; `SOURCE_TREE_REF != ARTIFACT_COMMIT`.

## UNKNOWN conditions

Private cross-session history; phenomenal experience; independent IV&V; live commercial model binding; relational style without a frozen public marker.

## Claim ceiling

At most: inquiry-role behavior can be scored on public-safe continuity cells.
Not: same subject, phenomenal self, or system-level subjectivity established.
