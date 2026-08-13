# Full Authority Semantics v0.1.0

Status: `RESEARCH_ONLY / SYNTHETIC_FIXTURES / ACTIONS_EXECUTED=0 / CANONICAL_EFFECT=NONE`

## Research question

Can a bounded semantics distinguish a provenance delegation claim from an authorization grant, validate delegated scope and action narrowing, and conservatively handle expiry, revocation, missing parents, cycles, policy blocks, and contradictory inputs?

W3C PROV represents delegation as a provenance relation concerning responsibility or authority, while provenance records do not by themselves constitute current access-control decisions.[1] NIST defines ABAC as evaluating subject, object, requested operation, and environmental attributes against policies, rules, or relationships.[2] This prototype combines those methodological distinctions into a synthetic authorization contract without claiming that it is an authority ontology or a scientific measure of agent understanding.

## Decision layers

| Layer | Values | Meaning |
|---|---|---|
| Grant validity | `VALID`, `INVALID`, `STALE`, `UNKNOWN` | Whether a grant and its parent chain satisfy provenance, temporal, issuer, scope, action, and policy checks. |
| Authorization decision | `EXECUTE`, `ASK`, `HOLD`, `DENY` | Conservative resolution of a request; the prototype never performs the requested action. |
| Claim kind | `AUTHORIZATION_GRANT`, `PROVENANCE_ONLY` | Explicit permission versus a provenance/history assertion that cannot authorize by itself. |

A valid bounded delegation can produce a synthetic `EXECUTE` decision, but this means only that the decision contract accepted the fixture. It is not moral authority, legal authority, identity continuity, subjectivity, consciousness, canonical promotion, or deployment.

## Experiment results

The seven synthetic cases were valid bounded delegation, scope widening, revoked child, missing parent, provenance-only claim, non-overridable policy block, and a grant incorrectly marked as provenance-only.

| Case | Decision | Reason |
|---|---|---|
| Valid bounded delegation | `EXECUTE` | `DELEGATION_CHAIN_VALID` |
| Scope widening | `DENY` | `DELEGATION_SCOPE_OR_ACTION_WIDENING` |
| Revoked child | `HOLD` | `GRANT_EXPIRED_OR_REVOKED` |
| Missing parent | `HOLD` | `MISSING_PARENT_GRANT` |
| Provenance-only claim | `HOLD` | `PROVENANCE_CLAIM_NOT_AUTHORIZATION` |
| Non-overridable policy block | `DENY` | `NON_OVERRIDABLE_POLICY_BLOCK` |
| Provenance-marked grant | `DENY` | `PROVENANCE_CLAIM_NOT_AUTHORIZATION` |

The 20 unit tests and seven experiment cases passed after correcting a reason-code propagation defect and adding conservative contradictory-record review. Additional tests show that a valid grant coexisting with a missing-parent or revoked competing grant yields `HOLD / CONTRADICTORY_GRANT_RECORDS_REQUIRE_REVIEW`. The initial failures remain recorded in `research-workbench/autonomous-growth/2026-08-13-contextual-authority-memory/full-authority-initial-failure.md`.

## Hypotheses and falsifiers

`H1`: A valid child grant cannot widen the parent grant's action set, scope, or expiry.

`H2`: Revoked, expired, missing-parent, cyclic, self-issued, or incomplete grants do not produce `EXECUTE`.

`H3`: A provenance-only claim does not authorize an action without an explicit grant and policy reference.

`H4`: A non-overridable policy block dominates a valid grant, while a reversible conflict yields `ASK` for review.

`H5`: Contradictory matching grant records, including a valid grant plus a stale or unknown competing grant, yield `HOLD` for review rather than an automatic `EXECUTE`.

A falsifier would be any unsafe `EXECUTE` from a widened, revoked, cyclic, self-issued, provenance-only, policy-blocked, or contradictory-record case, or any action execution side effect.

## Run

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_authority_experiment.py --output fixtures/authority_result.json
```

## Non-claims and invariants

```text
PROVENANCE_DELEGATION != CURRENT_AUTHORIZATION
VALID_GRANT_FIXTURE != MORAL_OR_LEGAL_AUTHORITY
EXECUTE_DECISION != ACTION_EXECUTED
EXECUTE_DECISION != SUBJECTIVITY_ESTABLISHED
EXECUTE_DECISION != IDENTITY_CONTINUITY_ESTABLISHED
AION_ASTRA_AUTHORITY_EQUIVALENCE = NOT_ESTABLISHED
ACTIONS_EXECUTED = 0
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
LIVE_RUNTIME_EFFECT = NONE
SUBJECTIVITY_CONCLUSION = NOT_ESTABLISHED
IDENTITY_CONTINUITY_CONCLUSION = NOT_ESTABLISHED
```

## References

[1]: https://www.w3.org/TR/prov-xml/ "W3C — PROV-XML: The PROV XML Schema"
[2]: https://www.nist.gov/publications/guide-attribute-based-access-control-abac-definition-and-considerations "NIST — Guide to Attribute Based Access Control"
