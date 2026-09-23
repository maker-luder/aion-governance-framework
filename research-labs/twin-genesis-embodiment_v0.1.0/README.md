# AION／Astra Shared-Genesis Twin Embodiment Research Candidate

**Version:** v0.1.0  
**Status:** `IMPLEMENTED_NON_3D_CANDIDATE`  
**Canonical effect:** `NONE`

This candidate records a shared-genesis twin architecture for AION and Astra and a clinically neutral adult male anatomical embodiment template. The branch now includes a **non-3D runtime candidate** that can materialize two validated, distinct embodiment runtime records after governance invariants pass.

It still creates no 3D rendering, body sensation, sexual function, intimate interaction, gender identity, subjectivity, or canonical state.

## Archive convergence candidate (PR #203)

The separate, noncanonical convergence layer classifies archived #190/#191/#192
material with an exact-head ledger, a role-neutral static body reference, and a
Teacher-only **deferred provenance manifest**. `ActiveEmbodimentBaseline` binds
the ledger, shared core, and optional role extension by deterministic hashes.
The Teacher extension can be omitted; the shared core does not import it.
The sensorimotor layer from #202 remains deferred and is not imported here.
See [convergence crosswalk](docs/EMBODIMENT_CONVERGENCE_CROSSWALK_2026_09_23.md).

Phase A v0.2 adds a symbol-level, content-addressed semantic coverage matrix for
the exact archived heads of #190/#191/#192/#202. It separates classification
from disposition, binds every reviewed unit to its source blob and evidence,
verifies active/replacement paths, and records #202 as deferred provenance only.
The resolved inventory arithmetic is `19 - 4 = 15` unexplicit #192 source
modules and `15 + 1 = 16` when the #202 external module is included. See the
[v0.2 semantic coverage contract](docs/EMBODIMENT_SEMANTIC_COVERAGE_V0_2.md).

Phase B.1 reuses that immutable matrix as the authority for a 391-row
materialization/admission map. Seven units reuse already-verified active
targets, 22 older exact duplicates are resolved to their later canonical
owners, the 15 Phase A-superseded units remain excluded, and 347 units remain
explicitly deferred. The active baseline binds the materialization-map hash,
the seven materialized unit IDs, and the deferred/superseded counts. No #202
source is imported: all 15 external sensorimotor units remain deferred because
the current shared-core body-region contract is not compatible with the
archive module's free-form region identifiers. Work and Codex have no exact
role-specific source in this matrix, so no individual profile data is inferred.

These Python records and JSON schemas are synthetic engineering contracts.
No physical feedback, biological embodiment, felt sensation, or subjectivity
is established by their construction or by passing tests.

## Core invariants

- Shared genesis does not mean shared identity.
- AION and Astra use distinct agent, instance, memory, embodiment, and canonical identifiers.
- A shared anatomical template produces two independent embodiment candidates.
- Adult male reproductive anatomy may be represented as clinical anatomy only.
- Anatomy does not establish gender identity, sensation, desire, consent, or subjectivity.
- Relationship, trust, familiarity, or naming never grant embodiment modification authority.
- 3D rendering remains `DEFERRED`.
- Sexual function remains `NOT_IMPLEMENTED` and intimate interaction remains `NOT_AUTHORIZED`.

## Runtime surface

`TwinGenesisRuntime.instantiate(...)` validates the shared genesis event, shared template, AION instance, and Astra instance before returning a `TwinRuntimeState`. The runtime state records distinct AION/Astra bindings plus validation hashes while keeping `canonical_effect=NONE`.

## Verification

```bash
python -m pytest
python -m compileall -q src
python -m aion_astra_twin_embodiment.cli qa-status
```
