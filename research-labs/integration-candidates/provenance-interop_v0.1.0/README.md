# AION Provenance Interoperability Candidate v0.1.0

This is an **offline local candidate** for mapping AION/Astra evidence into a small, inspectable vocabulary inspired by W3C PROV-DM. It provides typed `Entity`, `Activity`, `Agent` and selected derivation/attribution relations, deterministic JSON serialization and SHA-256 digesting.

It is not a full W3C PROV-DM/PROV-O/PROV-N implementation, conformance claim, certification, identity proof or authorship proof. It does not access the network, credentials, model providers or canonical state.

```text
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
INDEPENDENT_IVV = NOT_ACHIEVED
```

The comparison source is [W3C PROV-DM](https://www.w3.org/TR/prov-dm/). This candidate deliberately implements only a bounded local mapping suitable for evidence review and test fixtures.
