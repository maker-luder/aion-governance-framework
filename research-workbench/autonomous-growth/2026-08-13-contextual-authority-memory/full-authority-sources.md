# Full-authority semantics source notes

## 1. W3C PROV-XML — Delegation and provenance

URL: https://www.w3.org/TR/prov-xml/

W3C PROV represents delegation through `prov:Delegation` / `prov:actedOnBehalfOf` as part of agents, responsibility, and influence. The page frames provenance as information about entities, activities, and people involved in producing something, useful for assessing quality, reliability, or trustworthiness. A provenance delegation relation records responsibility or an asserted relationship; it is not by itself a current authorization decision or a complete access-control policy.

The prototype therefore keeps `provenance_claim`, `delegation_edge`, and `authorization_decision` as separate layers. A valid provenance edge cannot automatically grant an action, extend scope, or survive revocation without an explicit policy evaluation.

## 2. NIST SP 800-162 — ABAC definition and considerations

URL: https://www.nist.gov/publications/guide-attribute-based-access-control-abac-definition-and-considerations

NIST defines ABAC as determining authorization for operations by evaluating attributes associated with the subject, object, requested operations, and sometimes environment conditions against policies, rules, or relationships describing allowable operations. The source emphasizes policy evaluation rather than keyword or role-label matching.

The prototype uses this as a methodological vocabulary for subject/delegator, delegate, object, action, scope, time, revocation, and policy constraints. It does not claim NIST validates the AION/Astra authority model.

## Design consequence

The next bounded unit should be `full-authority-semantics_v0.1.0`. It will distinguish authority issuance, bounded delegation, scope narrowing, expiry/revocation, provenance-only claims, and authorization decisions. It will reject scope widening, self-issued authority, missing delegation provenance, revoked chains, and contradictory policy inputs with `HOLD`/`DENY` rather than producing an automatic execute decision.

## References

[1]: https://www.w3.org/TR/prov-xml/ "W3C — PROV-XML: The PROV XML Schema"
[2]: https://www.nist.gov/publications/guide-attribute-based-access-control-abac-definition-and-considerations "NIST — Guide to Attribute Based Access Control"
