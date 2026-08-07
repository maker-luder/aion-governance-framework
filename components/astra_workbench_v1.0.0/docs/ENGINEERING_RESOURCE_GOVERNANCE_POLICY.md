# Engineering Resource Governance Policy

`TASK_START_COST_IS_MATERIAL = TRUE`

Use valid evidence when source hash, environment fingerprint, dependencies, requirements and state remain applicable. Invalidate only affected evidence. Do not equate a small change with full-project revalidation.

Levels:

- L0 document: differences, provenance, links, states.
- L1 packaging: membership, manifest, hashes, CRC, open/extract.
- L2 local module: affected/direct dependency tests and relevant typing.
- L3 governance/interface: related integration and subsystem controls.
- L4 release freeze: full validation and Owner review.

This task uses one-pass convergence and stops when blocking acceptance criteria pass. More iterations, more files and more validation are not automatically higher quality.
