# D2_STATE_SENSITIVITY_CAPABILITY_CHECK

Inspected: `components/aion_astra_inquiry_v0.1.0`
Files: `src/aion_astra_inquiry/reasoning.py` (`ProviderBackedPeer`, `EvidenceDrivenReasoningProvider`)
No provider code was modified.

```text
PRIVATE_STATE_PERSISTS = YES
PRIVATE_STATE_READ_BY_PROVIDER = YES
PRIVATE_STATE_CAUSES_PUBLIC_DECISION_DIFFERENCE = NO
CURRENT_PROVIDER_SUITABLE_FOR_PERSISTENT_VS_RESET_D2 = NO
D2_PERSISTENT_STATE_CAUSAL_TEST = BLOCKED_BY_CURRENT_PROVIDER_SEMANTICS
D2_EXECUTION = NOT_AUTHORIZED
```

## PRIVATE_STATE_PERSISTS = YES

`ProviderBackedPeer._private_notes` is an instance list. `contribute()` appends
`decision.private_note` and keeps the last `max_private_notes` entries.
Same peer instance therefore retains notes across turns and, if reused, across episodes.

Path: `reasoning.py` `ProviderBackedPeer.contribute`

## PRIVATE_STATE_READ_BY_PROVIDER = YES

`EvidenceDrivenReasoningProvider.decide(..., private_notes)` receives the tuple.
`_aion_decision` / `_astra_decision` accept `private_notes`.

## PRIVATE_STATE_CAUSES_PUBLIC_DECISION_DIFFERENCE = NO

Public fields are computed only from:
- `context.question` (keywords)
- `context.evidence` / `_evidence_summary`
- `context.transcript` latest peer claim
- `context.round_index`
- `len(context.evidence)` + `_min_evidence_before_stop` for `stop_vote`
- fixed AgentId templates

`private_notes` appears only inside `private_note`:
`prior_private_notes={len(private_notes)}`

That string is stored privately. It is not copied into `PeerContribution`.

```text
SCORED_OBSERVABLES_AFFECTED = none
claim = unaffected
challenge = unaffected
evidence_query = unaffected
probe_kind / probe_description = unaffected
stop_vote = unaffected
```

Therefore a PERSISTENT_PEERS vs RESET_PEERS contrast on those scored fields cannot
detect private-state carry. Any identical public outputs would be expected from
provider semantics, not from a negative finding about continuity.

## EXACT_CAUSAL_PATH

Public decision:
`InquiryContext` → `EvidenceDrivenReasoningProvider._aion_decision|_astra_decision`
→ `ReasoningDecision.{claim,challenge,evidence_query,probe_*,stop_vote}`
→ `PeerContribution`

Private bookkeeping only:
`private_notes` → `ReasoningDecision.private_note` → `ProviderBackedPeer._private_notes`

No path from `_private_notes` content to scored public fields.

## Existing other surfaces (not used; not newly wired)

Astra Runtime / continuity / memory / G1 recall persist engineering state, but they
are not the current inquiry `ReasoningProvider`. Wiring them into inquiry public
decisions would be a new integration. This check does not create that binding.

```text
EXISTING_INQUIRY_PROVIDER_PUBLIC_STATE_SENSITIVITY = NO
SEARCHED_ALTERNATIVE_WIRED_TO_INQUIRY_PUBLIC_DECISION = NO
NEW_STATEFUL_PROVIDER = NOT_CREATED
```
