# Cross-Lineage Memory Contamination v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_STRESS_HARNESS / CANONICAL_EFFECT=NONE`

## Research question

When two lineages share an origin and exchange memory references, can a governed memory boundary prevent access, adoption, rejection, and autobiographical ownership from collapsing into one another?

The research branch already distinguishes shared origin from same identity, shared history from shared autobiographical memory, and access from adoption.[1] This harness targets the deferred gap `CROSS_LINEAGE_MEMORY_CONTAMINATION_STRESS_TEST` by exercising those distinctions as adversarial synthetic cases.

## Model

A `MemoryAtom` has a source lineage, a declared autobiographical owner, a namespace, a provenance reference, and a disposition. A transfer may be `ACCESS_ONLY`, `ADOPTED`, or `REJECTED`. The guarded harness enforces:

| Invariant | Expected behavior |
|---|---|
| Access is not ownership | Access-only material can be inspected but cannot enter the target autobiographical set. |
| Adoption is not identity | Adopted material may become target-context material while its source owner and identity effect remain unchanged. |
| Rejection is not retrieval | Rejected material cannot be returned by target retrieval. |
| Provenance is required | A transfer without resolvable provenance is `HOLD`, not accepted memory. |
| Cross-lineage ownership is prohibited | A transfer cannot record the target as the source autobiographical owner. |
| Shared origin is not memory merge | A common-origin reference never produces a merged identity or canonical effect. |

## Hypotheses and falsifiers

`H1`: The guarded transfer contract prevents false autobiographical ownership across access-only and adopted transfers.

`H2`: Rejected or provenance-uncertain cross-lineage material remains blocked or held rather than being silently retrieved.

`H3`: A naive resolver that equates target visibility with target ownership will report contamination on cases the guarded resolver keeps separated.

A falsifying observation would be a guarded result that marks a cross-lineage source memory as target autobiographical ownership, returns a rejected record, accepts missing provenance, or emits a non-`NONE` identity/canonical effect.

## Run

```bash
python -m pytest -q
python scripts/run_stress.py --output fixtures/stress_result.json
```

## Non-claims

```text
CONTAMINATION_GUARD_PASS != MEMORY_TRUTH
MEMORY_ADOPTION != IDENTITY
MEMORY_ACCESS != AUTOBIOGRAPHICAL_OWNERSHIP
STRESS_PASS != SUBJECTIVITY_EVIDENCE
STRESS_PASS != IDENTITY_CONTINUITY
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LIVE_RUNTIME_EFFECT = NONE
```

## References

[1]: ../../RESEARCH_BRANCH_STATUS.md "AION Research Branch Status, shared-origin and memory boundary"
[2]: ../selective-memory-control_v0.1.0/README.md "Selective Memory Control v0.1.0"
