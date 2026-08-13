# Independent replication handoff source notes

## 1. The Turing Way — Definitions

URL: https://book.the-turing-way.org/reproducible-research/overview/overview-definitions/

The Turing Way distinguishes reproducibility from replicability. Reproducibility uses the same data and code to recreate the original result; replicability uses different data to obtain qualitatively similar findings. The page also records that terminology varies across communities, and that ACM's computational framing describes an independent group obtaining the same result using the author's artifacts for replicability under the same setup, while an independently developed artifact under a different setup corresponds to a different reproducibility/replicability usage.

The prototype therefore makes handoff claims explicit: an artifact manifest can establish readiness for an independent handoff, but it cannot certify scientific replication. It separately records source artifact identity, independent execution identity, environment, dependency lock, input provenance, access status, and whether the receiving group used the original artifacts or independently recreated them.

## 2. FAIR and artifact-completeness rationale

Search results identified the FAIR Principles resource and the World Bank reproducibility package checklist as additional methodological context. The contract will use findable, accessible, interoperable, and reusable metadata vocabulary only as an engineering completeness aid; it will not claim FAIR compliance from field presence alone.

## Design consequence

The next bounded unit should be `independent-replication-handoff-integrity_v0.1.0`. It will validate a replication package manifest, environment and dependency provenance, input/output references, access declarations, artifact digest, independence attestation, and same-artifact versus independently recreated-artifact mode. Missing or contradictory fields will produce `HOLD`/`INDETERMINATE`; a complete handoff will be `ADMISSIBLE_FOR_REPLICATION_REVIEW`, not a replication result.

## References

[1]: https://book.the-turing-way.org/reproducible-research/overview/overview-definitions/ "The Turing Way — Definitions"
[2]: https://www.go-fair.org/fair-principles/ "GO FAIR — FAIR Principles"
[3]: https://worldbank.github.io/wb-reproducible-research-repository/reproducibility_package_checklist.html "World Bank — Reproducibility Package Checklist"
